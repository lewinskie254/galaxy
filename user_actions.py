def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.current_speed_x = self.SPEED_X
        elif keycode[1] == 'right':
            self.current_speed_x = -self.SPEED_X
        return True

def on_keyboard_up(self, keyboard, keycode):
    self.current_speed_x = 0 
    return True

def on_touch_down(self, touch):
    i = 0 
    if touch.x < self.width/2:
        self.current_speed_x = self.SPEED_X
    else: 
        i -= 5
        self.current_speed_x = -self.SPEED_X
    
def on_touch_up(self, touch):
        self.current_speed_x = 0 