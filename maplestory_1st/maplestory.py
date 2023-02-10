import pygame
import os
#########################################################
#기본 초기화(반드시 해야 하는 것들)
pygame.init() #초기화(반드시 필요)

#화면 크기 설정
screen_width =1080 # 가로크기
screen_height=720 # 세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Maple Story") #게임이름

# FPS
clock = pygame.time.Clock()
#########################################################

# 1. 사용자 게임 초기화(배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__) # 현재파일의 위치 반환
image_path = os.path.join(current_path, "image") #project image 폴더 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

#스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] #stage 높이

#캐릭터 만들기
character_stand_right = pygame.image.load(os.path.join(image_path, "character_stand_right.png"))
character_stand_left = pygame.image.load(os.path.join(image_path, "character_stand_left.png"))
character_run_right = pygame.image.load(os.path.join(image_path, "character_run_right.png"))
character_run_left = pygame.image.load(os.path.join(image_path, "character_run_left.png"))

character_size = character_stand_right.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width/2 - character_width/2
character_y_pos = screen_height - character_height - stage_height


#캐릭터 이동 방향
character_to_x_right = 0
character_to_x_left = 0
# 0: stand_right
# 1: stand_left
# 2: run_right
# 3: run_left
character_image_state = 0


#캐릭터 이동 속도
character_speed = 5

# 점프 이벤트
jump_event = 0
init_jump_speed=7
to_jump = init_jump_speed # 점프 속도
jump_dif = 0.5 # 공중에서 속도 변화


# 무기 만들기
weapon_right = pygame.image.load(os.path.join(image_path, "weapon_right.png"))
weapon_left = pygame.image.load(os.path.join(image_path, "weapon_left.png"))
weapon_size = weapon_right.get_rect().size
weapon_width = weapon_size[0]
weapon_height = weapon_size[1]

# 무기 방향
weapon_direction = 0 # 0: 오른쪽, 1: 왼쪽

# 무기는 한 번에 여러 발 발사 가능
weapons =[]

# 무기 이동 속도
weapon_speed = 10


running =True
while running:
    dt = clock.tick(60) # 게임화면의 초당 프레임 수를 설정


    # 2. 이벤트 처리(키보드, 마우스 등)   
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생하였는가?
                running= False

        if event.type == pygame.KEYDOWN:
           
            if event.key == pygame.K_LEFT: # 왼쪽 이동
                character_to_x_left -= character_speed
                character_image_state = 3
            if event.key == pygame.K_RIGHT:# 오른쪽 이동
                character_to_x_right += character_speed
                character_image_state =2

            if event.key == pygame.K_LALT: # 점프
                jump_event = 1
            
            if event.key == pygame.K_LSHIFT: # 무기 발사
                if character_image_state == 0 or character_image_state == 2: # 오른쪽   
                    weapon_x_pos = character_x_pos + weapon_width
                    weapon_y_pos = character_y_pos + character_height/2 - weapon_height/2
                    weapon_direction = 0
                    weapons.append([weapon_x_pos, weapon_y_pos, weapon_direction])
                else: #왼쪽
                    weapon_x_pos = character_x_pos
                    weapon_y_pos = character_y_pos + character_height/2 - weapon_height/2
                    weapon_direction = 1
                    weapons.append([weapon_x_pos, weapon_y_pos, weapon_direction])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                character_to_x_left = 0
                if character_to_x_right != 0:
                    character_image_state = 2

                    
            if event.key == pygame.K_RIGHT:
                character_to_x_right =0
                if character_to_x_left != 0:
                    character_image_state = 3
            
            if event.key == pygame.K_LALT:
                jump_event = 0            

    # 캐릭터 서 있을 때
    if character_to_x_left ==0 and character_to_x_right == 0:
        if character_image_state == 2:
            character_image_state = 0
        elif character_image_state == 3:
            character_image_state = 1
        
    
    # 3. 게임 캐릭터 위치 정의 
    character_x_pos = character_x_pos + character_to_x_right + character_to_x_left


    if jump_event == 1:
        character_y_pos -= to_jump
        to_jump -= jump_dif
        if character_y_pos > (screen_height - stage_height-character_height):
            to_jump = init_jump_speed # 초기화
    elif jump_event == 0:
        if character_y_pos < (screen_height - stage_height-character_height):
            character_y_pos -= to_jump
            to_jump -= jump_dif
        elif character_y_pos >= (screen_height - stage_height-character_height):
            character_y_pos =screen_height - stage_height-character_height
            

    

    if character_x_pos <0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    #무기 위치 조정
    thing = [ ]
    for w in weapons:
        if w[2] == 0:
            thing.append([w[0]+weapon_speed,w[1],w[2]])
        elif w[2] == 1:
            thing.append([w[0]-weapon_speed,w[1],w[2]])
    weapons = thing
            

    # 스크린 밖 무기 없애기
    weapons = [ [w[0], w[1], w[2]] for w in weapons if (w[0] > 0 and w[0] < screen_width - weapon_width)]

    # 4. 충돌 처리

    # 5. 화면에 그리기
    screen.blit(background,(0,0))
    screen.blit(stage,(0,screen_height - stage_height))
    

    

    if character_image_state == 0:
        screen.blit(character_stand_right,(character_x_pos,character_y_pos))
    elif character_image_state == 1:
        screen.blit(character_stand_left,(character_x_pos,character_y_pos))
    elif character_image_state == 2:
        screen.blit(character_run_right,(character_x_pos,character_y_pos))
    elif character_image_state == 3:
        screen.blit(character_run_left,(character_x_pos,character_y_pos))
    
    for w in weapons:
        if w[2] == 0:
            screen.blit(weapon_right,(w[0], w[1]))
        else:
            screen.blit(weapon_left,(w[0], w[1]))

   


        

    pygame.display.update() # 게임화면 다시 그리기!



# pygame 종료
pygame.quit()