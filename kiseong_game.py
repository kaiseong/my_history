import pygame as pg

# 오차
error=1

# 화면 크기 설정
screen_width=1080
screen_height=720

# 캐릭터 설정
# pygame.sprite.Sprite 를 상속받음
class Player(pg.sprite.Sprite):
    def __init__(self,game):
        super(Player,self).__init__() # 부모 클래스 생성자 호출
        self.game=game
        self.load_image() # 이미지 로드 함수
        self.size=self.image.get_size() # 이미지 크기를 튜플형식으로 저장합니다
        self.pos = (50, 10) # 캐릭터 초기 위치 지정.
        self.rect = pg.Rect(self.pos, self.size) # pygame.Rect 객체로 이미지의 좌표와 크기 데이터를 지정합니다.
        self.dx = 0 # x축 움직임 속도
        self.dy =  0 # y축 움직임 속도
        self.gravity=True
        self.acc = 0.163 # 플레이어의 기본 y축 가속도(중력)은 -0.163입니다.
        self.jump=False # 점프 중인가?
        self.speed=2
    def load_image(self):
        self.image=pg.image.load("game/resources/character.png")
    
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
            self.jump=True

    def update(self):
        if self.gravity==True:
            self.acc=0.1
        elif self.gravity==False:
            self.acc=0
        self.dy+=self.acc
        self.rect.x+=self.dx
        self.rect.y+=self.dy
        # 키보드에 따라 이미지 변환 추가해야함
       # self.image = self.img[0] if self.vel < 0 else self.img[1] # 속도가 음수라면 기본 이미지를 양수라면 뛰는 이미지로 만듭니다.
    def collide(self,sprites):
        for sprite in sprites:
            if pg.sprite.collide_rect(self,sprite):
                return sprite
# 블럭들 클래스
class Block(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        super(Block,self).__init__() #부모 클래스 생성자 호출
        self.game=game
        self.load_image()
        self.size=self.image.get_size()
        self.pos=(x,y)
        self.rect=pg.Rect(self.pos,self.size)
        
        
    def load_image(self):
            self.image=pg.image.load("game/resources/block1.png")

    def collide(self,sprites):
        for sprite in sprites:
            if pg.sprite.collide_rect(self,sprite):
                return sprite


        

class Game:
    def __init__(self):
        pg.init() # 초기화 작업
        self.screen=pg.display.set_mode((screen_width,screen_height))
        # 화면 제목
        pg.display.set_caption("18100038 권기성")
        # clock 객체 생성
        self.clock=pg.time.Clock()
        # 배경 이미지 부르기
        self.background=pg.image.load("game/resources/background.png")
        self.onGame = True
        self.newGame()
        
    
    

    def newGame(self):
        self.start=False
        self.all_sprites=pg.sprite.Group()
        # 캐릭터 객체 생성
        self.player=Player(self)
        self.blocks=pg.sprite.Group()
        # 바닥 라인
        for i in range(10):
            self.blocks.add(Block(self,i*30,690))
        for i in range(3):
            self.blocks.add(Block(self,270,660-(i*31)))
       
        self.all_sprites.add([self.player,self.blocks]) # 스프라이트 묶기


        while self.onGame:
            self.clock.tick(60) # 프레임 60
            self.update()
            self.draw()
            self.events()
            pg.display.update() # 화면 업데이트
            
    def update(self):
        self.player.update() # 캐릭터 현재 좌표 업데이트
        self.push(self.blocks)

    def events(self):
        # 이벤트 조건
        event=pg.event.poll()
        if event.type==pg.QUIT: # 게임 종료
            self.onGame=False
        if event.type==pg.KEYDOWN: # 키보드를 눌렀는가?
            if event.key==pg.K_LEFT: # 좌
                self.player.dx=-self.player.speed
            elif event.key==pg.K_RIGHT: # 우
                self.player.dx=self.player.speed
            elif event.key==pg.K_SPACE and self.player.jump==True: # 점프
                self.player.dy=-5
                self.player.jump=False
        elif event.type==pg.KEYUP: # 키보드에서 손때면 이동 멈춤
            if event.key==pg.K_RIGHT or event.key==pg.K_LEFT:
                self.player.dx=0
          
        self.player.condition() # 화면 밖 으로 안나가는 조건

    
        

    # 블럭과 충돌 조건들
    def push(self,sprites):
        p_x=self.player.rect.x # 캐릭터 x 좌표
        p_y=self.player.rect.y # 캐릭터 y 좌표
        p_width=self.player.size[0] # 캐릭터 가로 넓이
        p_height=self.player.size[1] # 캐릭터 세로 길이
        for sprite in sprites:
            # 왼쪽면 부딪히기
            if p_x+p_width > sprite.rect.x-error and sprite.rect.x>p_x+error and p_y +p_height>sprite.rect.y+error and p_y < sprite.rect.y+sprite.size[1]-error:
                self.player.rect.x=sprite.rect.x-sprite.size[0]-error*2
            # 오른쪽 면 부딪히기
            if p_x < sprite.rect.x+sprite.size[0]+error and p_x+p_width > sprite.rect.x+sprite.size[0] and p_y+p_height>sprite.rect.y and p_y <sprite.rect.y+sprite.size[1] - error:
                self.player.rect.x=sprite.rect.x+sprite.size[0]+error*2
               
            # 블럭 밑변에 부딪히기
            if p_x+p_width >= sprite.rect.x and sprite.rect.x+sprite.size[0] >=p_x and p_y +p_height > sprite.rect.y+sprite.size[1] and p_y < sprite.rect.y+sprite.size[1]+(error*2):
                #print('ok')
                self.player.dy=4
                p_y=sprite.rect.y+sprite.size[1]+error
                self.player.gravity=True
            
            # 블럭위에 서있기 
            if p_x+p_width>sprite.rect.x and p_x < sprite.rect.x+sprite.size[0] and p_y+p_height >= sprite.rect.y - error  and p_y<=sprite.rect.y:
                self.player.gravity=False
                self.player.jump=True
            else:
                self.player.gravity=True

            if p_x+p_width>sprite.rect.x and p_x < sprite.rect.x+sprite.size[0] and p_y+p_height > sprite.rect.y -(error*2) and p_y<sprite.rect.y:
               self.player.rect.y=sprite.rect.y-p_height-1
               self.player.dy=0
               self.player.acc=0 
    # 그리기 함수 
    def draw(self):
        self.screen.blit(self.background,(0,0)) # 배경 그리기
        self.all_sprites.draw(self.screen) # 캐릭터 그리기

        pg.display.flip() # 화면 업데이트
        
if __name__=='__main__':
    game=Game()





        
