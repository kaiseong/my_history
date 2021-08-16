import pygame




# 화면 크기 설정
screen_width=1080
screen_height=720



# 캐릭터 설정
# pygame.sprite.Sprite 를 상속받음
class Player(pygame.sprite.Sprite):
    def __init__(self,game):
        super(Player,self).__init__() # 부모 클래스 생성자 호출
        self.game=game
        self.load_image() # 이미지 로드 함수
        self.size=self.image.get_size() # 이미지 크기를 튜플형식으로 저장합니다
        self.pos = (50, 10) # 캐릭터 초기 위치 지정.
        self.rect = pygame.Rect(self.pos, self.size) # pygame.Rect 객체로 이미지의 좌표와 크기 데이터를 지정합니다.
        self.dx = 0 # x축 움직임 속도
        self.dy =  0 # y축 움직임 속도
        self.gravity = 0.163 # 플레이어의 기본 y축 가속도(중력)은 -2입니다.
    def load_image(self):
        self.image=pygame.image.load("game/resources/character.png")
    
    def condition(self):
        if self.rect.x<0:
            self.rect.x=0
        elif self.rect.x+self.size[0]>screen_width:
            self.rect.x=screen_width-self.size[0]
        if self.rect.y<0:
            self.rect.y=0
        elif self.rect.y+self.size[1]>screen_height:
            self.rect.y=screen_height-self.size[1]
            self.dy=0

    def update(self):
        self.dy+=self.gravity
        
        self.rect.x+=self.dx
        self.rect.y+=self.dy
        # 키보드에 따라 이미지 변환 추가해야함
       # self.image = self.img[0] if self.vel < 0 else self.img[1] # 속도가 음수라면 기본 이미지를 양수라면 뛰는 이미지로 만듭니다.

# 블럭들 클래스
class Block(pygame.sprite.Sprite):
    def __init__(self,game,x,y,image):
        super(Block,self).__init__() #부모 클래스 생성자 호출
        self.game=game
        self.load_image()
        self.size=self.image.get_size()
        self.pos=(x,y)
        self.rect=pygame.Rect(self.pos,self.size)
        self.imagename=image
    def load_image(self):
        self.image=pygame.image.load(self.imagename)

    def collide(self,sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self,sprite):
                return sprite


        

class Game:
    def __init__(self):
        pygame.init() # 초기화 작업
        self.screen=pygame.display.set_mode((screen_width,screen_height))
        # 화면 제목
        pygame.display.set_caption("18100038 권기성")
        # clock 객체 생성
        self.clock=pygame.time.Clock()
        # 배경 이미지 부르기
        self.background=pygame.image.load("game/resources/background.png")
        self.onGame = True
        self.newGame()
        self.player=Player()

    def newGame(self):
        self.start=False
        self.all_sprites=pygame.sprite.Group()
        # 캐릭터 객체 생성
        self.player=Player(self)
        self.all_sprites.add([self.player]) # 스프라이트 묶기
    

        while self.onGame:
            self.clock.tick(60) # 프레임 60
            self.update() 
            self.draw()
            self.events()
            pygame.display.update() # 화면 업데이트
            
    def update(self):
        self.player.update() # 캐릭터 현재 좌표 업데이트

    def events(self):
        # 이벤트 조건
        event=pygame.event.poll()
        if event.type==pygame.QUIT: # 게임 종료
            self.onGame=False
        if event.type==pygame.KEYDOWN: # 키보드를 눌렀는가?
            if event.key==pygame.K_LEFT: # 좌
                self.player.dx=-4
            elif event.key==pygame.K_RIGHT: # 우
                self.player.dx=4
            elif event.key==pygame.K_SPACE: # 점프
                self.player.dy=-7
        elif event.type==pygame.KEYUP: # 키보드에서 손때면 이동 멈춤
            if event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT:
                self.player.dx=0
          
        self.player.condition() # 화면 밖 으로 안나가는 조건

    def draw(self):
        self.screen.blit(self.background,(0,0)) # 배경 그리기
        self.all_sprites.draw(self.screen) # 캐릭터 그리기
        pygame.display.flip() # 화면 업데이트
        
if __name__=='__main__':
    game=Game()





        
