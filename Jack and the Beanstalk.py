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
        self.load_image() # 이미지 로드 함수
        self.size=self.image.get_size() # 이미지 크기를 튜플형식으로 저장합니다
        self.pos = (20, 650) # 캐릭터 초기 위치 지정.
        self.rect = pg.Rect(self.pos, self.size) # pygame.Rect 객체로 이미지의 좌표와 크기 데이터를 지정합니다.
        self.dx = 0 # x축 변수지정
        self.dy =  0 # y축 변수지정
        self.gravity=True # 중력장 지정
        self.acc = 0.163 # 플레이어의 기본 y축 가속도(중력)은 -0.163입니다.
        self.jump=False # 점프 중인가?
        self.speed=2 # x축 움직임 속도
    def load_image(self):
        self.image=pg.image.load("pythongame-18100038/resources/right.png")
    
    # 화면 밖으로 못나가게하기
    def condition(self):
        if self.rect.x<0: # 왼쪽 창 밖으로 못나가는 조건
            self.rect.x=0
        elif self.rect.x+self.size[0]>screen_width and self.rect.y>164: # 출구 제외오른쪽 창 밖으로 못 나가는 조건
            self.rect.x=screen_width-self.size[0]
        if self.rect.y<0: # 천장 위로 못나가는 조건
            self.rect.y=0
        
    # 중력 설정과 움직임
    def update(self):
        if self.gravity==True: # 중력장이 켜지면 가속도 0.1를 준다
            self.acc=0.1
        elif self.gravity==False: # 중력장이 꺼지면 가속도는 없어진다.
            self.acc=0
        self.dy+=self.acc # 중력 가속
        self.rect.x+=self.dx # x축 움직임 업데이트
        self.rect.y+=self.dy # y축 움직임 업데이트
       # 충돌 검사
    def collide(self,sprites): # 충돌 여부 묻는 함수
        for sprite in sprites:
            if pg.sprite.collide_rect(self,sprite):
                return sprite

# 블럭들 클래스
class Block(pg.sprite.Sprite):
    def __init__(self,game,x,y,n):
        super(Block,self).__init__() #부모 클래스 생성자 호출
        # 이미지 선정
        self.n=n
        if self.n=='b':
            self.load_image_block()
        elif self.n=='t':
            self.load_image_trap()
        elif self.n=='d':
            self.load_image_door()
        elif self.n=='bo':
            self.load_image_buttonon()
        elif self.n=='bf':
            self.load_image_buttonoff()
        elif self.n=='w':
            self.load_image_windy()
        elif self.n=='treasure':
            self.load_image_treasure()
        self.size=self.image.get_size()
        self.pos=(x,y)
        self.rect=pg.Rect(self.pos,self.size)
    def load_image_block(self):
      self.image=pg.image.load("pythongame-18100038/resources/leafblock.png")
      self.image.set_colorkey((255,255,255))
    def load_image_trap(self):
        self.image=pg.image.load("pythongame-18100038/resources/trap.png")
        self.image.set_colorkey(0)
    def load_image_door(self):
        self.image=pg.image.load("pythongame-18100038/resources/door.png")
    def load_image_buttonon(self):
        self.image=pg.image.load("pythongame-18100038/resources/buttonon.png")
        self.image.set_colorkey((255,255,255))
    def load_image_buttonoff(self):
        self.image=pg.image.load("pythongame-18100038/resources/buttonoff.png")
        self.image.set_colorkey((255,255,255))
    def load_image_windy(self):
        self.image=pg.image.load("pythongame-18100038/resources/wind.png")
        self.image.set_colorkey((255,255,255))
    def load_image_treasure(self):
        self.image=pg.image.load("pythongame-18100038/resources/treasure.png")
        self.image.set_colorkey((255,255,255))

class Rain(pg.sprite.Sprite):
    def __init__(self,game,x):
        super(Rain,self).__init__() #부모 클래스 생성자 호출
        self.load_image()
        self.size=self.image.get_size()
        self.dy=4 # 비 내리는 속도
        self.pos=(rd.randint(390,1050),rd.randint(0,720)) # 비 초기 위치 설정값
        self.rect=pg.Rect(self.pos,self.size) # 비 이미지 좌표와 크기 데이터 지정
        self.rect.x=x
        # 비 나오는 패턴 변수
        self.select=0
    
    def load_image(self):
        self.image=pg.image.load("pythongame-18100038/resources/drop.png")
        self.image.set_colorkey((255,255,255))

        # 랜덤 패턴 in stage1
    def pattern_sg1(self):
        self.rect.y+=self.dy
        if self.rect.y+self.size[1]>720:
            # 비 구역 랜덤 지정
            self.select=rd.randrange(3)
            self.rect.y=0
            if self.select==0:
               self.rect.x=rd.randint(430,553)
            elif self.select==1:
                self.rect.x=rd.randint(610,853)
            elif self.select==2:
                self.rect.x=rd.randint(910,1033)


        # 같은 패턴 in stage2
    def pattern_sg2(self):
        self.rect.y+=self.dy
        if self.rect.y+self.size[1]>540:
            self.rect.y=130

class Game:
    def __init__(self):
        pg.init() # 초기화 작업
        pg.mixer.init() # 배경음악 사용
        self.screen=pg.display.set_mode((screen_width,screen_height))
        # 화면 제목
        pg.display.set_caption("18100038 권기성 잭과 콩나무")
        # clock 객체 생성
        self.clock=pg.time.Clock()
        # 배경 이미지 부르기
        self.background=pg.image.load("pythongame-18100038/resources/background.png")
        # 플레이어 오른쪽 왼쪽 이미지 이름 
        self.right="pythongame-18100038/resources/right.png"
        self.left="pythongame-18100038/resources/left.png"
        pg.mixer.music.load("pythongame-18100038/resources/backbgm.mp3") # 기본 배경 bgm불러오기
        self.jump_sound=pg.mixer.Sound("pythongame-18100038/resources/jump.mp3")
        self.button_sound=pg.mixer.Sound("pythongame-18100038/resources/button.mp3")
        self.alarm_sound=pg.mixer.Sound("pythongame-18100038/resources/alarm.mp3")
        self.dead_sound=pg.mixer.Sound("pythongame-18100038/resources/dead.mp3")

        self.onGame = True # 게임 실행 중인가  
        self.newGame() 
        

    def newGame(self):

        self.start=False # 게임이 시작했는가
        self.die=False # 사망했는가
        self.clear=False # 게임을 클리어했는가
        
        # 객체들 초기화
        self.initset()
        self.start_time=pg.time.get_ticks()
        self.period_time=pg.time.get_ticks() #  반복 주기 기록용
        self.door_time=0 # 문 구간 제한 시간용
        self.try_time=pg.time.get_ticks()
        self.record_time=0
        # 스테이지 번호
        self.SN=1
        # 이벤트 조건
        self.turn_on=False
        self.alarm_sound.play()

        while self.onGame:
            self.clock.tick(60) # 프레임 60
            self.update()
            self.draw()
            self.events()
            self.died()
            if self.SN==1:
                self.wind() # 1 stage 바람 효과
            pg.display.update() # 화면 업데이트
        
    def update(self):
        self.player.update() # 캐릭터 현재 좌표 업데이트
        if self.start:
            self.record_time=int((pg.time.get_ticks()-self.start_time)/1000) # 게임 깨는데 걸리는 시간
        if self.die: # 죽으면 캐릭터 객체를 지워라
            self.all_sprites1.remove(self.player)
            self.all_sprites2.remove(self.player)
            pg.mixer.music.pause() # 배경음악은 멈추고
            self.dead_sound.play() # 죽음 효과음을 재생
        if self.SN==1: # 스테이지 1에서
            self.push(self.blocks1)
            for sprite in self.rain1: # 비 새로운 좌표 업데이트
                sprite.pattern_sg1() 
        elif self.SN==2: # 스테이지 2에서
            self.repeat=int((pg.time.get_ticks()-self.period_time)/1000) # 교차 블럭 주기 시간
            self.second=int((pg.time.get_ticks()-self.try_time)/1000) # 버튼 눌렀을 때부터 지난 시간을 초단위로 저장
            
            if self.turn_on:
                self.door_time=15-self.second # 문열리는 지속시간
            if self.door_time<0:
                self.door_time=0
            self.push(self.blocks2) # 블럭 충돌
            for sprite in self.rain2: # 비 충돌 검사
                sprite.pattern_sg2()
            if self.repeat<2: # 2초 주기로 블럭 사라졌다 나타나게하기
                self.push(self.jokeblocks1)
            elif 2<=self.repeat and self.repeat<4: 
                self.push(self.jokeblocks2)
            else:
                self.period_time=pg.time.get_ticks()
            
            self.buttoncondition()

    
        


    def died(self):
        if self.player.collide(self.rain1) and self.SN==1: # 빗물에 부딪혔는가?
            self.die=True
        if self.SN==2:
            if self.player.collide(self.traps): # 함정에 부딪혔는가?
                self.die=True
            if self.player.collide(self.rain2): # 빗물에 부딪혔는가?
                self.die=True
        if self.player.rect.y>screen_height+50:  # 화면 밖으로 떨어졌는가?
            self.die=True
        
      

    def events(self):
        # 이벤트 조건
        event=pg.event.poll()
        if event.type==pg.QUIT: # 게임 종료
            self.onGame=False
        # 처음 게임 시작 및 기록 측정 시작
        if self.start==False and self.die==False and (event.type == pg.MOUSEBUTTONDOWN):
            self.start=True
            self.start_time=pg.time.get_ticks()
            pg.mixer.music.play(-1)
        # 클리어후 재시작
        
        if self.clear and (event.type == pg.MOUSEBUTTONDOWN): # 클리어 상태에서 마우스를 누르면 게임을 초기화 합니다.
            self.newGame()
        if self.die and (event.type == pg.MOUSEBUTTONDOWN): # 죽은 상태에서 마우스를 누르면 게임을 초기화합니다.
                self.dead_sound.stop()
                self.newGame()
        if self.start==True:
            if event.type==pg.KEYDOWN: # 키보드를 눌렀는가?
                if event.key==pg.K_LEFT: # 좌
                    self.player.dx=-self.player.speed
                    self.player.image=pg.image.load(self.left)
                elif event.key==pg.K_RIGHT: # 우
                    self.player.dx=self.player.speed
                    self.player.image=pg.image.load(self.right)
                elif event.key==pg.K_SPACE and self.player.jump==True: # 점프
                    self.jump_sound.play()
                    self.player.dy=-5
                    self.player.jump=False # 점프 기회 소진

                elif event.key==pg.K_x and self.player.collide(self.button) and self.turn_on==False: # 버튼 누르는 조건
                    self.button_sound.play()
                    self.turn_on=True
                    self.try_time=pg.time.get_ticks()

                elif (not self.die) and self.player.collide(self.treasure) and self.SN==2 and event.key==pg.K_x: # 게임 클리어 조건
                    self.clear=True
                    self.record=self.record_time

            elif event.type==pg.KEYUP: # 키보드에서 손때면 이동 멈춤
                if event.key==pg.K_RIGHT or event.key==pg.K_LEFT:
                    self.player.dx=0
            
        self.player.condition() # 화면 밖 으로 못 나가는 조건
        
        if self.player.rect.x>screen_width and self.player.rect.y<164: # 다음 스테이지 넘어가는 조건
            self.player.rect.x=50;  self.player.rect.y=600    
            self.SN+=1

        # 객체 초기화 함수
    def initset(self):
        # 캐릭터 및 블록, 비 등 객체 생성
        self.player=Player(self)
        self.blocks1=pg.sprite.Group() # 블럭 빈 묶음 만들기
        self.blocks2=pg.sprite.Group()
        self.jokeblocks1=pg.sprite.Group()
        self.jokeblocks2=pg.sprite.Group()
        self.rain1=pg.sprite.Group() # 비 빈 묶음 만들기
        self.rain2=pg.sprite.Group()
        self.treasure=pg.sprite.Group()
        self.windy=pg.sprite.Group()
        self.traps=pg.sprite.Group()
        self.door=pg.sprite.Group()
        self.button=pg.sprite.Group()
        self.all_sprites1=pg.sprite.Group() # 묶음집 빈 묶음 만들기
        self.all_sprites2=pg.sprite.Group()
        self.Stage1()
        self.Stage2()
        # 스프라이트 스테이지 별로 묶기
        self.all_sprites1.add([self.player,self.blocks1,self.rain1,self.windy]) 
        self.all_sprites2.add([self.player,self.blocks2,self.rain2,self.traps,self.button,self.treasure]) 

    # 스테이지1 함수
    def Stage1(self):
        # stage1
        for i in range(11):
            self.blocks1.add(Block(self,i*30,690,'b'))
            self.blocks1.add(Block(self,240,660-(i*120),'b'))
        for i in range(21):
            self.blocks1.add(Block(self,270,660-(i*30),'b'))
            self.blocks1.add(Block(self,360,i*30,'b'))
        for i in range(2):
            self.blocks1.add(Block(self,570,690-i*240,'b'))
            self.blocks1.add(Block(self,870,690-i*240,'b'))
            self.blocks1.add(Block(self,1020+i*30,185,'b'))
            self.windy.add(Block(self,600+i*300,100,'w'))
        for i in range(5):
            self.blocks1.add(Block(self,500+i*200,185,'b'))
            # 비
            self.rain1.add(Rain(self,rd.randint(390,1050)))
        
        self.blocks1.add(Block(self,1050,550,'b'))
        self.blocks1.add(Block(self,390,320,'b'))
    
    def Stage2(self):
        for i in range(7):
            self.blocks2.add(Block(self,i*30,690,'b'))
            self.blocks2.add(Block(self,930+i*30,300,'b'))
        for i in range(33): 
            self.blocks2.add(Block(self,90+i*30,-30,'b'))
            self.blocks2.add(Block(self,i*30,570,'b'))
            self.blocks2.add(Block(self,100+i*30,100,'b'))
            self.traps.add(Block(self,i*30,540,'t'))
        for i in range(2):
            self.jokeblocks1.add(Block(self,350+i*340,690,'b'))
            self.jokeblocks2.add(Block(self,520+i*340,690,'b'))
            self.jokeblocks2.add(Block(self,220+i*370,480,'b'))
            self.jokeblocks2.add(Block(self,220+i*370,240,'b'))
            
            self.blocks2.add(Block(self,1020+i*30,690,'b'))
            self.blocks2.add(Block(self,1050,580-i*90,'b'))
            self.blocks2.add(Block(self,930+i*30,400,'b'))
            
            self.blocks2.add(Block(self,0,300-i*90,'b'))
            self.rain2.add(Rain(self,270+i*400))
        for i in range(3):
            self.jokeblocks1.add(Block(self,100+i*300,360,'b'))
        self.door.add(Block(self,30,140,'d'))
        self.button.add(Block(self,930,370,'bf'))
        self.treasure.add(Block(self,950,30,'treasure'))
            
    def wind(self): # 바람 
        if 390<self.player.rect.x and self.player.rect.x< 1020 and self.player.rect.y+self.player.size[1] <210: # 구역 지정
            self.player.rect.x-=1
        for sprite in self.windy:
            sprite.rect.x-=0.1 # 바람 속도
            if sprite.rect.x<390:
                sprite.rect.x=1000

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
        self.draw_text('Time:'+str(self.record_time), 30, 0.5,0.5, 0, False) # 기록 시간 
        if self.SN==1:
            self.all_sprites1.draw(self.screen) # 스테이지 1 객체들 그리기
        elif self.SN==2:
            self.draw_text('time:'+str(self.door_time),20,1,50,0,False)
            self.all_sprites2.draw(self.screen) # 스테이지 2 객체들 그리기
            if self.repeat<2:
                    self.jokeblocks1.draw(self.screen) # 깜짝 상자 1번 그리기
            elif 2<=self.repeat and self.repeat<4:
                    self.jokeblocks2.draw(self.screen) # 깜짝 상자 2번 그리기
            if self.turn_on==False:
               self.door.draw(self.screen) # 문 그리기
        if not self.start: # 시작하지 않은 상태라면 시작 메세지를 보여줍니다.
            self.draw_text('Press Mouse button to start', 60,screen_width * 0.5, screen_height * 0.5, (255, 255, 0), True)
        if self.die: # 죽은 상태라면 재시작이 가능하도록 안내 메세지를 보여줍니다.
            self.draw_text('Game Over', 100,  screen_width*0.5, screen_height*0.5, (255,255,0), True)
            self.draw_text('Press any Key to restart', 40, screen_width*0.5, screen_height*0.6, (180,255,200), True)
        if self.clear:
            self.draw_text("Clear!!!",60,screen_width*0.5,screen_height*0.5-50,0,True)
            self.draw_text("record time: "+str(self.record),45,screen_width*0.5,screen_height*0.5,(255,0,255),True)
            self.draw_text('Press Mouse button to restart', 40,screen_width * 0.5, screen_height * 0.5+60, (255, 0, 255), True)
        pg.display.flip() # 화면 업데이트

    def draw_text(self, text, font_size, x, y, color, isCenter):
        font = pg.font.Font("pythongame-18100038/resources/NanumBarunGothic.ttf", font_size) # 인수로 받은 font size에 따라 font 객체를 생성합니다.
        text_obj = font.render(text, True, color) # font를 사용해 텍스트 객체를 만듭니다.
        text_rect = text_obj.get_rect() # 텍스트가 위치와 크기를 저장하는 객체입니다.
        if isCenter: # isCenter 변수가 True라면 좌표를 텍스트의 중심으로 삼습니다.
            text_rect.centerx = int(x)
            text_rect.centery = int(y)
        else: # isCenter 변수가 False라면 좌표를 텍스트의 좌상단점으로 삼습니다.
            text_rect.x = int(x)
            text_rect.y = int(y)
        self.screen.blit(text_obj, text_rect) # 화면에 업데이트합니다.
               

    def buttoncondition(self):
        if self.door_time <=0: # 0초 이하로 내려가면 문을 닫아라
            self.turn_on=False
            # 버튼 색 바꾸기
        if self.turn_on==True: 
            for sprite in self.button:
                sprite.image=pg.image.load("pythongame-18100038/resources/buttonon.png")
        elif self.turn_on==False:
            self.push(self.door)
            for sprite in self.button:
                sprite.image=pg.image.load("pythongame-18100038/resources/buttonoff.png")
    
    
                        
        
if __name__=='__main__':
    game=Game()
