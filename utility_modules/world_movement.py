import cv2
import numpy as np
from time import sleep, time

import multiprocessing as mp
import math

import random

from utility_modules.calculus import calculate_vector_magnitude
from utility_modules.capture import capture_mode
import utility_modules.move_ctype as cici


def movement_calculations(player_coords, player_angle, checkpoint_coords, angle_only = None):


    if angle_only:
        try:
            delta = 0
            print(player_angle, angle_only)
            if abs(player_angle - angle_only) > 180:
                print('if')
                if angle_only > player_angle:
                    delta = (angle_only - 360) - player_angle
                if player_angle > angle_only:
                    delta = (360 - player_angle) + angle_only
            else:
                print('else')
                if player_angle > angle_only:
                    delta = angle_only - player_angle
                if angle_only > player_angle:
                    delta = angle_only - player_angle
        except Exception as e:
                delta = 1
                print(f'exception, {e}')

        return delta

    vector_checkpoint = (checkpoint_coords[0] - player_coords[0], -(checkpoint_coords[1] - player_coords[1]))
    angle_radians = math.atan2(vector_checkpoint[0], vector_checkpoint[1])

    angle_degrees = math.degrees(angle_radians)
    if angle_degrees < 0:
        angle_degrees = 360 + angle_degrees

    angle_delta = cici.calculate_rotation_direction(player_angle, angle_degrees, True)
    distance = calculate_vector_magnitude(vector_checkpoint)

    return angle_delta, distance

def get_locationd_fromID(location_id):
    zone_ids = {
        2112: "Thaldrassus",
        2266: "Timetravel",
        862: "Zuldazar",
        863: "Nazmir",
        896: "Drustvar",
        895: "Tiragarde",
        936: "Freehold",
        85: "Orgrimmar"
    }
    if location_id in zone_ids:
        return zone_ids[location_id]
    else:
        return "Hearthstone"
def gonnafly(deserved_outcome):
    print('gonnafly', deserved_outcome)
    match deserved_outcome:

        case "horizontal":
            cici.move_cursor_steps(960, 540)
            cici.press_key('c')
            sleep(0.1)

            cici.move_mouse_steps(960, 360)
        case "45down":
            cici.move_cursor_steps(960,540)
            cici.move_mouse_steps(960,1080)
        case "23down":
            cici.move_cursor_steps(960, 540)
            cici.press_key('c')
            sleep(0.1)
            cici.move_mouse_steps(960, 360)


            cici.move_cursor_steps(960, 540)
            cici.move_mouse_steps(960, 810)
        case"up_0.5sec":
            _,_,shape, _ = gather_data()
            if shape == 50:
                cici.press_key('7')
                sleep(0.4)
            cici.press_key('space', 0.5)
        case"up_1sec":
            _,_,shape, _ = gather_data()
            if shape == 50:
                cici.press_key('7')
                sleep(0.4)
            cici.press_key('space', 1.2)
        case"up_abit":
            _, _, shape, _ = gather_data()
            if shape == 50:
                cici.press_key('7')
                sleep(0.4)
            cici.press_key('space', 0.15)
def gather_data(queue = None, stop_flag = None,):
    cant_get = 0
    while True:
        start_time = time()

        coords = capture_mode('addon_coords')
        if type(coords) == bool:
            print('perhaps loading')
            sleep(5)
            cant_get += 1
            if cant_get > 10:
                print('breaking gatherer')
                if stop_flag is not None:
                    stop_flag.value = 1
                return False
            continue


        location_list = coords[0, 20].tolist()


        zone_id = int(str(location_list[2]) + str(location_list[1]))  ##bgr
        location = get_locationd_fromID(zone_id)

        if location == "Heartstone":
            print('we need to heart')
            if stop_flag is not None:
                stop_flag.value = 1
            return None, None, None, location


        shapeshift_list = coords[0, 30].tolist()
        x_list = coords[0,66].tolist()
        y_list = coords[0,180].tolist()
        angle_list = coords[0,125].tolist()



        shapeshift_req = sum(shapeshift_list)

        y_list.reverse()
        x_list.reverse()

        x_coord = x_list[0] + x_list[1]*0.01
        y_coord = y_list[0] + y_list[1]*0.01

        player_coords = (x_coord, y_coord)
        player_angle = sum(angle_list)

        elapsed_time = time() - start_time
        sleep_time = 1/15 - elapsed_time



        if queue is not None:
            queue.put((player_coords, player_angle, shapeshift_req, location))

            if stop_flag.value == 1:
                print('finished gatherer')
                queue.put((None))
                break
        else:
            return player_coords, player_angle, shapeshift_req, location

        if sleep_time > 0:
            sleep(sleep_time)

def mover(queue,stop_flag,cp_list):
    print('started mover')
    for checkpoint in cp_list:
        for_starter = time()
        match len(checkpoint):
            case 2:
                print(f'case 2 default for {checkpoint}')
                req_dist = 0.3
                req_angle = None
            case 3:
                print(f'case 3 for {checkpoint}')
                req_dist = checkpoint[2]
                req_angle = None
            case 4:
                print(f'case 4 for {checkpoint}')
                req_dist = checkpoint[2]
                req_angle = checkpoint[3]

        print('got first location')
        old_magnitude = 100
        first_location = True
        while True:
            print('trying to use q inside while')
            player_coords, player_angle, shapeshift_req, location = queue.get()
            print('got data from q', player_coords, player_angle, shapeshift_req)

            if first_location == True:
                first_location = location
                print('saved first location', first_location)

            if first_location != location:
                print('left location', first_location, 'entered', location)
                cici.keybd_up('w')
                cici.keybd_up('d')
                cici.keybd_up('a')
                break
            elif location == "Freehold":
                print('entered freehold')
                cici.keybd_up('d')
                cici.keybd_up('a')
                cici.keybd_up('w')
                stop_flag.value = 1
                return print('finished mover completely, print via return')




            if shapeshift_req == 50:
                cici.press_key('7')
            elif shapeshift_req == 100:
                cici.press_key('t')

            delta, magnitude = movement_calculations(player_coords, player_angle, checkpoint)
            print(f'magnitude: {magnitude}, delta: {delta}')

            difference_magnitude = old_magnitude - magnitude
            if difference_magnitude < 0.01 and difference_magnitude > 0:
                print('happened random')
                cici.press_key(random.choice(['d', 'a', 'space', 's']), 0.1)

            old_magnitude = magnitude

            if abs(delta) > 10:
                if delta > 0:
                    cici.keybd_down('d')
                else:
                    cici.keybd_down('a')
            else:
                cici.keybd_up('d')
                cici.keybd_up('a')

            if magnitude > req_dist and abs(delta) < 40:
                cici.keybd_down('w')

            elif magnitude < req_dist:
                cici.keybd_up('w')
                cici.keybd_up('d')
                cici.keybd_up('a')
                print(f'reached cp {checkpoint}')
                break

            if random.random() > 0.999:
                cici.press_key('space')


            cp_tooktime = time() - for_starter
            if cp_tooktime > 120:
                print('we fucked up in time spent')
                break

            #visualisation
            if False:
                img = np.full((100, 400, 3), (234, 183, 39), dtype=np.int8)
                cv2.putText(img, f'{player_coords[0]}, {player_coords[1]}, {player_angle}', (
                10, int(cv2.getTextSize(f'{player_coords[0]}, {player_coords[1]}, {player_angle}', cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0][1] + 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                cv2.putText(img, f'{magnitude, delta}', (
                10, int(cv2.getTextSize(f'{player_coords[0]}, {player_coords[1]}, {player_angle}', cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0][1] + 60)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                window_name = "Top Window"
                cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
                cv2.imshow(window_name, img)
                cv2.waitKey(1)


        ##req angle
        while req_angle != None:
            player_coords, player_angle,shapeshift_req, location = queue.get()
            delta = movement_calculations(player_coords, player_angle, checkpoint, req_angle)
            if stop_flag.value:
                print('broke mover')
                break


            if abs(delta) > 20:

                if delta > 0:
                    cici.keybd_down('d')
                else:
                    cici.keybd_down('a')

            else:

                cici.keybd_up('d')
                cici.keybd_up('a')
                break


    cici.keybd_up('d')
    cici.keybd_up('a')
    cici.keybd_up('w')
    stop_flag.value = 1
    print('finished mover completely')
def mp_moving(checkpoints_list):
    queue = mp.Queue()
    stop_flag = mp.Value('i', 0)
    gather_process = mp.Process(target=gather_data, args=(queue,stop_flag,))
    mover_process = mp.Process(target=mover, args=(queue,stop_flag,checkpoints_list,))

    gather_process.start()
    mover_process.start()

    gather_process.join()
    mover_process.join()

    print('joint')
    while not stop_flag.value == 1:
        print('not finished mp moving')

    print('MOVIMOVI FINISHED SEXY')




def decision_maker(going_todo=None, location= None):
    extra_action = None

    if going_todo is None:
        zone_routes = {
            'Thaldrassus': [(48.1,49.12), (49.88,53.46), (52.93,56.50), (53.48,55.49, 0.2), 'portal'],
            'Timetravel': [(55.37,57.09), (61.48, 64.46), (60.84, 68.64, 0.2, 220), 'portal'],
            'Drustvar': []
        }

        going_todo = zone_routes[location]

    def extra_action(extra_action):
        print('extra action: ', extra_action)
        match extra_action:
            case 'portal':
                cici.press_key('n')
                cici.move_cursor_steps(960,540)
                cici.press_left_button()
                cici.release_left_button()
                sleep(5)

            case 'horizontal_fly':
                gonnafly('horizontal')
            case '23down':
                gonnafly('23down')
            case 'get_up':
                gonnafly('up_0.5sec')
            case 'get_up1':
                gonnafly('up_1sec')
            case 'getup_abit':
                gonnafly('up_abit')
            case 'tp_kultiras':
                cici.press_key('enter')
                cici.type_string('/target dread-admiral')
                cici.press_key('enter')
                cici.press_key('n')
                sleep(0.2)
                cici.move_cursor_steps(150,292)
                sleep(0.6)
                cici.press_left_button()
                cici.release_left_button()
                sleep(2)
            case 'enter_freehold':
                cici.press_key('w', 3)
                sleep(2)


    assigned_actions = True
    extra_actions = []
    while assigned_actions or going_todo[0] is str or going_todo[-1] is str:
        print('assigning')
        if type(going_todo[0]) is str:
            extra_actions.append((0, going_todo[0]))
            going_todo.pop(0)
            continue
        elif type(going_todo[-1]) is str:
            extra_actions.append((1, going_todo[-1]))
            going_todo.pop(-1)
            continue
        elif len(extra_actions) == 0:
            print('none eas, just running')
            mp_moving(going_todo)
            return print('leaveing decision_making')
        print('finished assign', extra_actions)

        for action in extra_actions:
            if action[0] == 0:
                print('performing ea', action)
                extra_action(action[1])
                if action == extra_actions[-1]:
                    print('last action')
                    mp_moving(going_todo)
            elif action[0] == 1:
                mp_moving(going_todo)
                print('performing ea', action)
                extra_action(action[1])

        return print('made actions leaving')




def understand_situation():
    player_coords, player_angle, shapeshift_req, location = gather_data()
    print(location)
    if location == "Freehold":
        print('WE DID IT')
        return False

    if location == "Hearthstone":
        print('hearting')
        return True


    situational_cooords = {
        "Orgrimmar": [((53.65, 78.72), 'tavern'), ((52.46,79.12), 'crossroad')],
        "Thaldrassus": [((47.28, 46.95), 'tavern'), ((49.1,53.94), 'out_tavern'), ((53.42, 55.62), 'portal')],
        "Timetravel": [((54.88, 55.77), 'to_drustvar')],
        "Drustvar": [((36.92,41.14), 'to_tiragarde')],
        "Tiragarde": [((51.98, 63.87), 'to_align'), ((74.61, 64.58), 'angle_down'), ((84.60, 78.78), 'close_freehold'), ((85.37,80.36), 'freehold_tavern'),
        ((89.37,53.51,), 'tiragarde_ship')],
        "Zuldazar": [((57.97,63.19), 'pier'), ((58.42,63.00),'admiral')]


    }
    situational_routes = {
        "Thaldrassus": {
            "tavern": [(48.1,49.12), (49.88,53.46), (53.11,56.76,0.2), (53.48,55.49, 0.2), 'portal'],
            "out_tavern": [(53.11,56.76,0.2), (53.48,55.49, 0.2), 'portal'],
            "portal": [(53.11,56.76,0.2), (53.48,55.49, 0.2), 'portal'],
                        },
        "Timetravel": {
            "to_drustvar": [(56.15,59.89), (60.46, 66.77), (60.84, 68.64, 0.2, 220), 'portal'],
        },
        "Drustvar": {
            "to_tiragarde": ['horizontal_fly', (38.05, 38.13), (76.02, 55.22)],
        },
        "Tiragarde": {
            "to_align": [(74.61, 64.58)],
            "angle_down": ['23down',(85.43, 77.59), (84.77, 78.44), (84.57,78.80,0.1,255)],
            "close_freehold": ['23down', (84.54,78.81, 0.1, 240), 'enter_freehold'],
            "freehold_tavern": ['get_up', (85.41, 80.11), (84.76,78.73)],
            "tiragarde_ship" : ['get_up1','horizontal_fly', (88.88,53.29),(90.25, 59.15), (90.42,63.60),(88.82,72.41),(88.75,74.93),(87.94,77.44),
                                (85.54,76.59),(85.48,77.95)],

        },
        "Orgrimmar": {
            "tavern": [(52.73,79.14)],
            "crossroad": ['get_up','horizontal_fly',  (52.65,81.82), (52.59,84.61), (52.82,90.64), (55.14,90.12), (57.22,89.92),(58.63,91.40), 'portal']
        },
        "Zuldazar": {
            "pier": ['get_up1','23down', (58.43,63.01, 0.02),'tp_kultiras'],
            "admiral": [(58.43,63.01, 0.02), 'tp_kultiras']

        }

    }


    if situational_cooords[location]:
        outcome = None
        for identifier in  situational_cooords[location]:
            distance = calculate_vector_magnitude((identifier[0][0] - player_coords[0], identifier[0][1] - player_coords[1]))

            if outcome is None:
                outcome = (distance, identifier[1])
            elif outcome[0] > distance:
                outcome = (distance, identifier[1])


        precise_location = outcome[1]
        print(precise_location, 'precise loc')
        desired_route = situational_routes[location][precise_location]
        print(desired_route,'desired route')
        return desired_route

    else:
        print('no possible locations here')
        return None


def reshala():
    print('started reshala')
    while True:
        try:
            path_to_take = understand_situation()
            if type(path_to_take) is not bool:
                print(path_to_take)
                decision_maker(path_to_take)
            elif type(path_to_take) is bool and path_to_take is True:
                print('using hs')
                cici.press_key('enter')
                cici.type_string('/use hearthstone')
                cici.press_key('enter')
                sleep(20)
            else:
                return True
        except Exception as e:
            print('in reshala we failed exception:', e)
            return False
