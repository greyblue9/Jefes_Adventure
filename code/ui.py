import pygame as pg
from support import import_folder

class Button:
    def __init__(self, pos, path, name, state):
        self.pos = pos
        self.name = name
        
        # images
        self.frames = import_folder(path, "image")
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # conditions
        self.hover = False
        self.state = state
        self.clicked = False

    def update(self, event_info):
        if self.state == 'locked':
            tint_surface = self.image.copy()
            tint_surface.fill((200,200,200),None,pg.BLEND_RGB_MAX)
            self.image.blit(tint_surface,(0,0))
        else:
            self.hover = self.rect.collidepoint(event_info["mouse pos"])
            for event in event_info["events"]:
                if self.hover and event.type == pg.MOUSEBUTTONDOWN:
                    self.clicked = True

    def draw(self, display_screen):
        display_screen.blit(self.image,self.pos)

class AnimatedButton(Button):
    def __init__(self,pos,path,name,state):
        super().__init__(pos,path,name,state)
        self.animation_speed = 0.05
        self.always_on = False

    def update(self, event_info):
        super().update(event_info)
        if self.state == 'unlocked' and (self.always_on or self.hover):
            self.animate()
        else:
            self.frame_index = 0
            self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index = (self.frame_index + self.animation_speed) % len(self.frames)
        self.image = self.frames[int(self.frame_index)]

class SwitchButton(Button):
    def update(self, event_info):
        super().update(event_info)
        self.frame_index = int(self.hover)
        self.image = self.frames[self.frame_index]

class AnimatedUI(AnimatedButton):
    def __init__(self,pos,path):
        super().__init__(pos,path,'','unlocked')
        self.hover = True

class Indicator:
    def __init__(self, pos, path):
        self.pos = pos
        self.indicator = AnimatedUI(pos,path+'/indicator')

    def update(self, event_info):
        self.indicator.update(event_info)

    def draw(self,display_screen):
        self.indicator.draw(display_screen)

class Bar(Indicator):
    def __init__(self, pos, path):
        super().__init__(pos,path)
        self.bar = pg.image.load(path + '/bar.png').convert_alpha()
        self.gel = pg.image.load(path + '/gel.png').convert_alpha()
        self.current = 1
        self.indicator.always_on = True

    def update(self, event_info, current):
        super().update(event_info)
        self.current = current/100

    def draw(self, display_screen):
        bar_position = self.pos + pg.math.Vector2(15,8)
        gel_fill = min(self.gel.get_width(),int(self.gel.get_width() * self.current))
        display_screen.blit(self.bar, bar_position)
        subsurface = self.gel.subsurface((0,0,gel_fill,self.gel.get_height()))
        display_screen.blit(subsurface, bar_position)
        self.indicator.draw(display_screen)

class BoneIndicator(Indicator):
    def __init__(self, pos, path):
        super().__init__(pos,path)
        self.num_bones = 0
        self.font = pg.font.Font('../img/ui/bars/bubblebutt.ttf', 50)

    def update(self, event_info, num):
        super().update(event_info)
        self.num_bones = num
        if self.num_bones >= 10:
            self.indicator.always_on = True

    def draw(self,display_screen):
        super().draw(display_screen)
        if self.num_bones >= 10:
            color = '#11d113'
        else:
            color = '#d68232'
        bone_amount_surface = self.font.render(str(self.num_bones), True, color)
        bone_amount_rect = bone_amount_surface.get_rect(topleft = self.indicator.rect.topright)
        bone_amount_rect.center += pg.math.Vector2(8,-12)
        display_screen.blit(bone_amount_surface,bone_amount_rect)
