import pygame as pg
import random as rd
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
        self.pos = (570, 500) # 캐릭터 초기 위치 지정.
        self.rect = pg.Rect(self.pos, self.size) # pygame.Rect 객체로 이미지의 좌표와 크기 데이터를 지정합니다.
        self.dx = 0 # x축 움직임 속도
        self.dy =  0 # y축 움직임 속도
        self.gravity=True
        self.acc = 0.163 # 플레이어의 기본 y축 가속도(중력)은 -0.163입니다.
        self.jump=False # 점프 중인가?
        self.speed=2
    def load_image(self):
        self.image=pg.image.load("game/resources/character.png")
    
    # 화면 밖으로 못나가게하기
    def condition(self):
        if self.rect.x<0:
            self.rect.x=0
        elif self.rect.x+self.size[0]>screen_width and self.rect.y>164: # 출구 제외오른쪽 창 밖으로 못 나가는 조건
            self.rect.x=screen_width-self.size[0]
        if self.rect.y<0:
            self.rect.y=0
        
    # 중력 설정과 움직임
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

class Bullit(pg.sprite.Sprite):
    def __init__(self,game):
        super(Bullit,self).__init__() #부모 클래스 생성자 호출
        self.game=game
        self.load_image()
        self.size=self.image.get_size()
        self.dy=4
        self.pos=(rd.randint(390,1050),rd.randint(0,720))
        self.rect=pg.Rect(self.pos,self.size)
        # 총알 나오는 범위 랜덤지정
        self.select=0
    
    def load_image(self):
        self.image=pg.image.load("game/resources/bullit.png")

    def collide(self,sprites):
        for sprite in sprites:
            if pg.sprite.collide_rect(self.sprite):
                return sprite
    def update(self):
        self.rect.y-=self.dy
        if self.rect.y+self.size[1]<0:
            # 총알 구역 랜덤 지정
            self.select=rd.randrange(3)
            self.rect.y=720
            if self.select==0:
               self.rect.x=rd.randint(430,553)
            elif self.select==1:
                self.rect.x=rd.randint(610,853)
            elif self.select==2:
                self.rect.x=rd.randint(910,1033)
        
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
        self.all_sprites1=pg.sprite.Group()
        self.all_sprites2=pg.sprite.Group()
        # 캐릭터 객체 생성
        self.player=Player(self)
        self.blocks1=pg.sprite.Group() # 블럭 그룹으로 묶기
        self.blocks2=pg.sprite.Group() 
        self.bullits1=pg.sprite.Group() # 총알 그룹으로 묶기
        self.bullits2=pg.sprite.Group()
        self.Stage1()
        self.Stage2()
        self.all_sprites1.add([self.player,self.blocks1,self.bullits1]) # 스프라이트 묶기
        self.all_sprites2.add([self.player,self.blocks2,self.bullits2])
        
        self.start_time=pg.time.get_ticks() # 시작 시간 기록
        # 스테이지 번호
        self.SN=1
       

        while self.onGame:
            self.clock.tick(60) # 프레임 60
            self.second=int((pg.time.get_ticks()-self.start_time)/1000) # 현재 시간에서 시작시간을빼어 초 단위로 저장
            self.update()
            self.draw()
            self.events()
            self.died()
            
            print(f'{self.player.rect.x}  {self.player.rect.y}')
            if self.SN==1:
                self.wind()
            pg.display.update() # 화면 업데이트
        
            #print(f'{self.second}')   
    def update(self):
        self.player.update() # 캐릭터 현재 좌표 업데이트
        self.push(self.blocks1)
        self.push(self.blocks2)
        for sprite in self.bullits1: # 총알 새로운 좌표 업데이트
            sprite.update()
    
    def died(self):
        if self.player.collide(self.bullits1): # 총알이랑 부딪혔는가?
            self.onGame=False
        if self.player.rect.y>screen_height+50:
            self.onGame=False # 화면 밖으로 떨어졌는가?

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
        
        if self.player.rect.x>screen_width and self.player.rect.y<164: # 다음 스테이지 넘어가는 조건
            self.player.rect.x=50
            self.player.rect.y=600    
            self.SN+=1
   
    def Stage1(self):
        # stage1
        for i in range(11):
            self.blocks1.add(Block(self,i*30,690))
            self.blocks1.add(Block(self,240,660-(i*120)))
        for i in range(21):
            self.blocks1.add(Block(self,270,660-(i*30)))
            self.blocks1.add(Block(self,360,i*30))
        for i in range(2):
            self.blocks1.add(Block(self,570,690-i*240))
            self.blocks1.add(Block(self,870,690-i*240))
            self.blocks1.add(Block(self,1020+i*30,185))
        for i in range(5):
            self.blocks1.add(Block(self,500+i*200,185))
            # 총 알들
            self.bullits1.add(Bullit(self))
           
        # 1층 오른쪽 끝
        self.blocks1.add(Block(self,1050,550))
        # 2층 왼쪽 끝
        self.blocks1.add(Block(self,390,320))
    
    def Stage2(self):
        for i in range(11):
            self.blocks2.add(Block(self,i*30,690))

    def wind(self):
        if 390<self.player.rect.x and self.player.rect.x< 1020 and self.player.rect.y+self.player.size[1] <210:
            self.player.rect.x-=1

    # 블럭과 충돌 조건들
    def push(self,sprites):
        p_x=self.player.rect.x # 캐릭터 x 좌표
        p_y=self.player.rect.y # 캐릭터 y 좌표
        p_width=self.player.size[0] # 캐릭터 가로 넓이
        p_height=self.player.size[1] # 캐릭터 세로 길이
        for sprite in sprites:
            # 왼쪽 변 부딪히기
            if p_x+p_width > sprite.rect.x-error*2 and sprite.rect.x>p_x+error and p_y +p_height>sprite.rect.y+error and p_y < sprite.rect.y+sprite.size[1]-error:
                self.player.rect.x-=self.player.speed
            # 오른쪽 변 부딪히기
            if p_x < sprite.rect.x+sprite.size[0]+error*2 and p_x+p_width > sprite.rect.x+sprite.size[0] and p_y+p_height>sprite.rect.y and p_y <sprite.rect.y+sprite.size[1] - error:
                self.player.rect.x+=self.player.speed
               
            # 블럭 밑변에 부딪히기
            if p_x+p_width > sprite.rect.x and sprite.rect.x+sprite.size[0] >p_x and p_y +p_height > sprite.rect.y+sprite.size[1] and p_y < sprite.rect.y+sprite.size[1]+(error*2):
                print('ok')
                self.player.dy=4
                p_y=sprite.rect.y+sprite.size[1]+error
                self.player.gravity=True
            
            # 블럭 위쪽 변 위에 서있기 
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
        if self.SN==1:
            self.all_sprites1.draw(self.screen) # 캐릭터 그리기
        elif self.SN==2:
            self.all_sprites2.draw(self.screen)
        pg.display.flip() # 화면 업데이트
        
if __name__=='__main__':
    game=Game()
