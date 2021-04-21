import pygame
from support.color import Color
from support.client import Client
from support.buttons import verticalButtonsDisplay

class HomePage:
    client  = Client()
    def __init__(self,screen, screen_size):
        self.screen, self.screen_size = screen, screen_size
        self.font = pygame.font.SysFont("arial", 40)
        self.font1 = pygame.font.SysFont("arial", 12)
        self.surface = pygame.Surface((500,200))
        self.surface1 = pygame.Surface((520,240))
        self.surface.fill(Color.grey1.value)
        self.surface1.fill(Color.grey1.value)
        self.components = ["Vote"]
        self.active = ''
        self.events = None
        self.response = None
        self.mouse_pos = None
        self.voteChoice = None
        self.choice = ()

    def run(self,events):
        self.events = events
        self.mouse_pos = pygame.mouse.get_pos()
        # draw the tittle
        size = pygame.font.Font.size(self.font, 'Voterpy')
        line = self.font.render('Voterpy', True, Color.white3.value)
        self.screen.blit(line, (self.screen_size[0]/2-size[0]/2, 20))
        # draw the sub tittle
        size = pygame.font.Font.size(self.font1, 'Voter App')
        line = self.font1.render('Voter App', True, Color.white.value)
        self.screen.blit(line, (self.screen_size[0]/2-size[0]/2, 60))

        # Draw all the candidates on the screen
        self.viewCandidatesOnRegister()

        # Called Method that draw the button on the screen
        self.active = verticalButtonsDisplay(self.screen, self.components,400,(225, 417),(250, 60), self.mouse_pos,self.active,\
                                                pygame.font.SysFont("arial", 25))
        # Drawing the surface on the screen
        self.screen.blit(self.surface1,(self.screen_size[0]/2-260, self.screen_size[1]/2-120))
        self.screen.blit(self.surface,(self.screen_size[0]/2-250, self.screen_size[1]/2-100))
        return "homePage"
    
    # Method that show all the candidates
    def viewCandidatesOnRegister(self):
        # to get connect whit server just one time 
        if type(self.response) != list or len(self.response)==0 or self.response == None:
            self.connectionSent = self.sendToServer("candidates/get")
        y, x =0,0
        count = 0
        
        if self.connectionSent:
            for element in self.response: # this will display the candidates on the screen according to the list
                y1,x1=y,x
                click = pygame.mouse.get_pressed(3)
                pygame.draw.rect(self.surface, Color.green.value, pygame.Rect(self.screen_size[0]/2-325, y1, 450, 40))
                pygame.draw.rect(self.surface, Color.grey2.value, pygame.Rect(self.screen_size[0]/2-325, y1, 450, 40),2)
                pygame.draw.rect(self.surface, Color.black1.value, pygame.Rect(self.screen_size[0]/2+75, y1+10, 20, 20),2)
                
                if self.voteChoice:
                    self.choice = pygame.draw.line(self.surface, Color.red1.value, ((self.screen_size[0]/2+100+75),int(self.screen_size[1]/2-100)+y1+10),\
                            (int(self.screen_size[0]/2+100+75+20),(int(self.screen_size[1]/2-100)+y1+30)), 2)
                    self.voteChoice = False

                if self.mouse_pos[0] in range(int(self.screen_size[0]/2+100+75),int(self.screen_size[0]/2+100+75+20)) and\
                    self.mouse_pos[1] in range(int(self.screen_size[1]/2-100)+y1+10, int(self.screen_size[1]/2-100)+y1+30)\
                    and click[0]==1:
                    self.voteChoice = True

                for key, value in element.items():
                    if key != "id" and key != "color" and key != "voterCounts"and key != "age":
                        if key == "age":
                            text_surface = pygame.font.SysFont("arial", 15).render(str(value)+" years old", True, Color.black1.value)
                            size = pygame.font.Font.size(pygame.font.SysFont("arial", 15), str(value)+" years old")
                        else:
                            text_surface = pygame.font.SysFont("arial", 15).render(str(value), True, Color.black1.value)
                            size = pygame.font.Font.size(pygame.font.SysFont("arial", 15), str(value))
                        self.surface.blit(text_surface, (x1+150/2-size[0]/2,y1+size[1]))
                        x1 +=5+size[0]
                count +=1
                # if count == 3: # check if is time to jump to new line and draw more candidates painel
                #     y += 110
                #     x = 70
                #     count = 0
                # else:
                y += 45
            self.choice
        
        print(self.voteChoice)

    def sendToServer(self, message):
        try:
            self.response = self.client.connectingToServer(message)
            return True
        except:
            return False