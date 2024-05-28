from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, Clock 
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad, Triangle
from kivy.core.window import Window
import random 




class MainWidget(Widget):
    from transforms import transform, transform_2d, transform_perspective
    from user_actions import on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 8
    V_LINES_SPACING = .25 #percentage of screen width
    vertical_lines = []

    H_NB_LINES = 10
    H_LINES_SPACING = .1 #percentage of screen width
    horizontal_lines = []

    current_offset_y = 0 
    current_offset_x = 0 
    current_speed_x = 0
    current_y_loop = 0

    SPEED = .004
    SPEED_X = .012

    NB_TILES = 12
    tiles = []
    tiles_coordinates = []

    SHIP_WIDTH = .1
    SHIP_HEIGHT = 0.035
    SHIP_BASE_Y = 0.04
    ship = None 
    ship_coordinates = [(0,0), (0,0), (0,0)]

    #Initialize All Functions 
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()
        self.pre_fill_tiles_coordinates()
        self.generate_tile_coordinates()

        if self.is_desktop():
            self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self.keyboard.bind(on_key_down=self.on_keyboard_down)
            self.keyboard.bind(on_key_up=self.on_keyboard_up)
        
        Clock.schedule_interval(self.update, 1.0/60.0)

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self._on_keyboard_down)
        self.keyboard.unbind(on_key_up=self._on_keyboard_up)
        self.keyboard = None


    #Vertical Lines 
    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            #self.line = Line(points=(100, 0, 100, 400), width= 5)
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())
        
    def get_line_y_from_index(self, index): 
        spacing_y = self.H_LINES_SPACING * self.height
        line_y = int(index * spacing_y - self.current_offset_y)

        return line_y 

    def update_vertical_lines(self):
        central_line_x = int(self.width/2)
        spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NB_LINES/2) + 0.5
        self.perspective_point_x = self.width/2 
        self.perspective_point_y = self.height * 0.75
        #self.line.points = [center_x, 0, center_x, center_y]
        for i in range(0, self.V_NB_LINES):
            line_x = int(central_line_x + offset * spacing + self.current_offset_x)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1
    

    #Horizontal Lines

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            #self.line = Line(points=(100, 0, 100, 400), width= 5)
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())
    
    def get_line_x_from_index(self, index): 
        central_line_x = int(self.width/2)
        spacing = self.V_LINES_SPACING * self.width
        offset = index - 0.5
        line_x = int(central_line_x + offset * spacing + self.current_offset_x)
        return line_x 


    def update_horizontal_lines(self):
        start_index = -int(self.V_NB_LINES/2) + 1
        end_index = start_index + self.V_NB_LINES - 1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)
        

        for i in range(0, self.H_NB_LINES):
            line_y = self.get_line_y_from_index(i)

            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]
    

    #Tiles Coordinates 
    def init_tiles(self): 
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.NB_TILES):
                self.tiles.append(Quad())
    
    def pre_fill_tiles_coordinates(self):
        for i in range(0, 10):
            self.tiles_coordinates.append((0, i))

    def generate_tile_coordinates(self): 
        start_index = -int(self.V_NB_LINES/2) + 1
        end_index = start_index + self.V_NB_LINES - 1
        
        last_x = 0 
        last_y = 0 

        #clean the coordinates 
        for i in range(len(self.tiles_coordinates)-1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop: 
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0: 
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1

        for i in range(len(self.tiles_coordinates), self.NB_TILES):
            r = random.randint(0, 2)
            # 0 is straight 
            # 1 is right 
            #2 is left 
            if last_x <= start_index:
                r = 1
            elif last_x >= end_index:
                r = 2
            
            self.tiles_coordinates.append((last_x, last_y))
            if r == 1: 
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            if r == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
    
    
    def get_tile_coordinates(self, ti_x, ti_y): 
        ti_y = ti_y - self.current_y_loop - 1

        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)

        return x, y 
    
    def update_tiles(self): 
        for i in range(0, self.NB_TILES):
            tile_coordinates = self.tiles_coordinates[i]
            xmin, ymin = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            xmax, ymax = self.get_tile_coordinates(tile_coordinates[0]+1, tile_coordinates[0]+1)
            #   2       3
            #
            #
            #   1       4
            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)
            
            self.tiles[i].points = [x1, y1, x2, y2, x3, y3, x4, y4]
    
    #Ship Coordinates & Canvas 
    def init_ship(self):
        with self.canvas:
            Color(0, 0, 0)
            self.ship = Triangle()

    def update_ship(self):
        center_x = self.width/2
        base_y = self.SHIP_BASE_Y * self.height
        ship_half_width = (self.SHIP_WIDTH * self.width) / 2
        ship_height = self.SHIP_HEIGHT * self.height

        self.ship_coordinates[0] = (center_x - ship_half_width , base_y)
        self.ship_coordinates[1] = (center_x, ship_height + base_y)
        self.ship_coordinates[2] = (center_x + ship_half_width, base_y)

        x1, y1 = self.transform(*self.ship_coordinates[0])
        x2, y2 = self.transform(*self.ship_coordinates[1])
        x3, y3 = self.transform(*self.ship_coordinates[2])

        self.ship.points = [x1, y1, x2, y2, x3, y3]


    #Ship Collision 
    def check_ship_collision_with_tile(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinates(ti_x + 1, ti_y + 1)

        for i in range(0, 3):
            px, py = self.ship_coordinates[i]
            if xmin <= px <= xmax and ymin <= py <= ymax:
                print("To this... ")
                return True
        return False
    
    def check_ship_collision(self):
        for i in range(0, len(self.tiles_coordinates)):
            ti_x, ti_y = self.tiles_coordinates[i]
           
            if ti_y >self.current_y_loop + 1: 
                return False
            if self.check_ship_collision_with_tile(ti_x, ti_y):
                return True 
        return False

    #Overall Game Functions    
    def update(self, dt):
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()
        

        speed_y = self.SPEED * self.height
        self.current_offset_y += speed_y * time_factor
        spacing_y = self.H_LINES_SPACING * self.height


        if self.current_offset_y >= spacing_y:
            self.current_offset_y = 0
            self.current_y_loop += 1
            self.generate_tile_coordinates()
        
        speed_x_new = self.current_speed_x  * self.width
        self.current_offset_x += speed_x_new * time_factor
        self.check_ship_collision()

    
    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True 
        return False

    
        
            


        
class GalaxyApp(App):
    pass


GalaxyApp().run()