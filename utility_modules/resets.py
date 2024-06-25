import utility_modules.move_ctype as cici
from utility_modules.capture import capture_mode
from time import sleep
from random import uniform
from utility_modules.world_movement import reshala

def grp_creation():
    cici.press_key('i')
    sleep(0.5)

    cici.move_cursor_steps(140,390) ## premade grps
    sleep(uniform(0.3,1))

    cici.press_left_button()
    sleep(0.1)
    cici.release_left_button()
    sleep(0.3)

    cici.move_cursor_steps(290, 270)# dung
    uniform(0.3,1)

    cici.press_left_button()
    sleep(0.1)
    cici.release_left_button()
    sleep(uniform(0.3,1))

    cici.move_cursor_steps(300, 535)# start
    cici.press_left_button()
    sleep(0.1)
    cici.release_left_button()
    sleep(uniform(0.3,1))

    cici.move_cursor_steps(455, 535)# list
    cici.press_left_button()
    sleep(0.1)
    cici.release_left_button() 
    sleep(uniform(7,10))

    cici.press_left_button()
    sleep(0.1)
    cici.release_left_button() #delist
    sleep(uniform(0.3,1))

    cici.press_key('i')
    sleep(0.5)


def change_action(desired_output):

    
    def check_mount():
        
        infobox = capture_mode('infobox')



        mount_B, mount_G, mount_R = infobox[150,250]   

        if mount_B == 255:
            return 'mammoth'

        if mount_G == 255:
            return 'runner'


    mount_info_start = check_mount()

    
    match desired_output:
        case 'runner':

            if mount_info_start != 'runner':
                sleep(0.5)
                cici.press_key('7')
                print('ready to run')
            else:
                print('already mounted for runner')


        case'mammoth':
            if mount_info_start != 'mammoth':
                sleep(0.5)
                cici.press_key('v')
                sleep(1.8)
                print('ready to sell')
            else:
                print('already sellin')

def reset_dung():


    not_finished = True
    reset_killer = 0
    
    while not_finished:
        cici.press_key('c')
        infobox = capture_mode('infobox')
        dung_B, dung_G, dung_R = infobox[150,350]

        while dung_G != 255 and dung_B != 255:
            
            sleep(2)
            infobox = capture_mode('infobox')

            dung_B, dung_G, dung_R = infobox[150,350]



        if dung_G == 255:
            cici.move_cursor_steps(960, 540)
            reset_killer += 1
            change_action('runner')
            if reset_killer >= 2:
                not_finished = False
                break
            
            change_action('runner')
            cici.press_key('w',3)

            sleep(3)
            print('capturing screen')


        if dung_B == 255:
            print('resetting')
            cici.move_cursor_steps(960, 540)
            cici.press_key('c')
            cici.press_key('h')
            sleep(0.2)
            
            change_action('runner')
            sleep(0.3)
            reshala()
            # mouse_moves = cici.calculate_rotation_direction(51, 245)
            #
            # for index, move in enumerate(mouse_moves):
            #     cici.move_mouse_steps(960 + move, 450)
            #     sleep(0.04)
            #
            # cici.press_key('space', 0.1)
            # cici.press_key('w', 3)
            # sleep(3)
            reset_killer += 1
            if reset_killer >= 2:

                not_finished = False
                break
    sleep(3)


def sell_loot():

    infobox = capture_mode('infobox')

    change_action('mammoth')
    sleep(1)

    cici.press_key('b')
    sleep(1)

    cici.press_key('n')
    sleep(1)

    cici.move_cursor_steps(uniform(160,180), uniform(540,500))
    n = 0
    
    while n<5:

        cici.press_left_button()
        sleep(0.3)
        cici.release_left_button()
        sleep(0.2)
        n += 1

    cici.move_cursor_steps(370, 130)
    #cici.press_key('esc')
    cici.press_left_button()
    sleep(0.1)
    cici.release_left_button()

    cici.move_cursor_steps(960, 540)


    change_action('runner')


def logout():
    
    cici.press_key('esc')
    sleep(1.5)

    cici.move_cursor_steps(940,646)
    
    sleep(0.5)

    cici.press_left_button()
    sleep(0.1)
    cici.release_left_button()

    print('logged out successfully')