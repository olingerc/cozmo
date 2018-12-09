#!/usr/bin/env python3

import random
import time

import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps

def cozmo_program(robot: cozmo.robot.Robot):

    # Lookaround until Cozmo knows where at least 3 cubes are:
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=60)
    lookaround.stop()

    if len(cubes) < 3:
        print("Error: need 3 Cubes but only found", len(cubes), "Cube(s)")
    else:
        print("Found 3 cubes, seting random lights")

        # Light up cubes randomly
        lights = [cozmo.lights.red_light, cozmo.lights.blue_light,
                  cozmo.lights.green_light]

        i = 0
        for cube in cubes:
           cube.set_lights(lights[i])
           i = i + 1

        # choose a number
        chosen = random.randint(0, 3)

        time.sleep(5)

        if chosen < 3:
            cube = cubes[chosen]
            print("Chose " + str(chosen))

            # Drive to the cube
            action = robot.go_to_object(cube, distance_mm(20.0))
            action.wait_for_completed()
            print("Completed action: result = %s" % action)

            # take a step back, lift fork and drive to the tube
            robot.drive_straight(distance_mm(-10), speed_mmps(50)).wait_for_completed()
            robot.set_lift_height(10.0).wait_for_completed()
            robot.set_head_angle(degrees(0.0)).wait_for_completed()
            robot.drive_straight(distance_mm(20), speed_mmps(50)).wait_for_completed()

            # hit the tube
            for _ in range(2):
               robot.move_lift(-5)
               time.sleep(0.05)
               robot.move_lift(5)
               time.sleep(0.05)


            # blink the cube
            for _ in range(0, 10):
               cube.set_lights(cozmo.lights.off_light)
               time.sleep(0.2)
               cube.set_lights(lights[chosen])
               time.sleep(0.2)

            # Say the color
            if chosen == 0:
                robot.say_text("Rot").wait_for_completed()
            if chosen == 1:
                robot.say_text("Blau").wait_for_completed()
            if chosen == 2:
                robot.say_text("Grün").wait_for_completed()

            # Be happy
            robot.drive_straight(distance_mm(-50), speed_mmps(150)).wait_for_completed()
            robot.play_anim(name="anim_poked_giggle").wait_for_completed()

        else:
            # Cozmo chose black
            robot.say_text("Nein!").wait_for_completed()
            robot.turn_in_place(degrees(180)).wait_for_completed()
            robot.say_text("Ich will doch lieber bei schwarz bleiben!").wait_for_completed()

cozmo.run_program(cozmo_program)
