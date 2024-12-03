"""
NOTE: some code adapted from Scott Dick's controller
"""
from pickle import FALSE

from kesslergame import KesslerController
from typing import Dict, Tuple
from cmath import sqrt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import math
import numpy as np
import matplotlib as plt



"""
NOTE: targeting_control code adapted from Scott Dick's controller
"""
def targeting_control():
    # self.targeting_control is the targeting rulebase, which is static in this controller.      
    # Declare variables
    bullet_time = ctrl.Antecedent(np.arange(0,1.0,0.002), 'bullet_time')
    theta_delta = ctrl.Antecedent(np.arange(-1*math.pi/30,math.pi/30,0.1), 'theta_delta') # Radians due to Python
    ship_turn = ctrl.Consequent(np.arange(-180,180,1), 'ship_turn') # Degrees due to Kessler
    ship_fire = ctrl.Consequent(np.arange(-1,1,0.1), 'ship_fire')
    
    #Declare fuzzy sets for bullet_time (how long it takes for the bullet to reach the intercept point)
    bullet_time['S'] = fuzz.trimf(bullet_time.universe,[0,0,0.05])
    bullet_time['M'] = fuzz.trimf(bullet_time.universe, [0,0.05,0.1])
    bullet_time['L'] = fuzz.smf(bullet_time.universe,0.0,0.1)
    
    # Declare fuzzy sets for theta_delta (degrees of turn needed to reach the calculated firing angle)
    # Hard-coded for a game step of 1/30 seconds
    theta_delta['NL'] = fuzz.zmf(theta_delta.universe, -1*math.pi/30,-2*math.pi/90)
    theta_delta['NM'] = fuzz.trimf(theta_delta.universe, [-1*math.pi/30, -2*math.pi/90, -1*math.pi/90])
    theta_delta['NS'] = fuzz.trimf(theta_delta.universe, [-2*math.pi/90,-1*math.pi/90,math.pi/90])
    # theta_delta['Z'] = fuzz.trimf(theta_delta.universe, [-1*math.pi/90,0,math.pi/90])
    theta_delta['PS'] = fuzz.trimf(theta_delta.universe, [-1*math.pi/90,math.pi/90,2*math.pi/90])
    theta_delta['PM'] = fuzz.trimf(theta_delta.universe, [math.pi/90,2*math.pi/90, math.pi/30])
    theta_delta['PL'] = fuzz.smf(theta_delta.universe,2*math.pi/90,math.pi/30)
    
    # Declare fuzzy sets for the ship_turn consequent; this will be returned as turn_rate.
    # Hard-coded for a game step of 1/30 seconds
    ship_turn['NL'] = fuzz.trimf(ship_turn.universe, [-180,-180,-120])
    ship_turn['NM'] = fuzz.trimf(ship_turn.universe, [-180,-120,-60])
    ship_turn['NS'] = fuzz.trimf(ship_turn.universe, [-120,-60,60])
    # ship_turn['Z'] = fuzz.trimf(ship_turn.universe, [-60,0,60])
    ship_turn['PS'] = fuzz.trimf(ship_turn.universe, [-60,60,120])
    ship_turn['PM'] = fuzz.trimf(ship_turn.universe, [60,120,180])
    ship_turn['PL'] = fuzz.trimf(ship_turn.universe, [120,180,180])
    
    #Declare singleton fuzzy sets for the ship_fire consequent; -1 -> don't fire, +1 -> fire; this will be  thresholded
    #   and returned as the boolean 'fire'
    ship_fire['N'] = fuzz.trimf(ship_fire.universe, [-1,-1,0.0])
    ship_fire['Y'] = fuzz.trimf(ship_fire.universe, [0.0,1,1]) 
            
    #Declare each fuzzy rule
    rule1 = ctrl.Rule(bullet_time['L'] & theta_delta['NL'], (ship_turn['NL'], ship_fire['Y']))
    rule2 = ctrl.Rule(bullet_time['L'] & theta_delta['NM'], (ship_turn['NM'], ship_fire['Y']))
    rule3 = ctrl.Rule(bullet_time['L'] & theta_delta['NS'], (ship_turn['NS'], ship_fire['Y']))
    # rule4 = ctrl.Rule(bullet_time['L'] & theta_delta['Z'], (ship_turn['Z'], ship_fire['Y']))
    rule5 = ctrl.Rule(bullet_time['L'] & theta_delta['PS'], (ship_turn['PS'], ship_fire['Y']))
    rule6 = ctrl.Rule(bullet_time['L'] & theta_delta['PM'], (ship_turn['PM'], ship_fire['Y']))
    rule7 = ctrl.Rule(bullet_time['L'] & theta_delta['PL'], (ship_turn['PL'], ship_fire['Y']))
    rule8 = ctrl.Rule(bullet_time['M'] & theta_delta['NL'], (ship_turn['NL'], ship_fire['Y']))
    rule9 = ctrl.Rule(bullet_time['M'] & theta_delta['NM'], (ship_turn['NM'], ship_fire['Y']))
    rule10 = ctrl.Rule(bullet_time['M'] & theta_delta['NS'], (ship_turn['NS'], ship_fire['Y']))
    # rule11 = ctrl.Rule(bullet_time['M'] & theta_delta['Z'], (ship_turn['Z'], ship_fire['Y']))
    rule12 = ctrl.Rule(bullet_time['M'] & theta_delta['PS'], (ship_turn['PS'], ship_fire['Y']))
    rule13 = ctrl.Rule(bullet_time['M'] & theta_delta['PM'], (ship_turn['PM'], ship_fire['N']))
    rule14 = ctrl.Rule(bullet_time['M'] & theta_delta['PL'], (ship_turn['PL'], ship_fire['N']))
    rule15 = ctrl.Rule(bullet_time['S'] & theta_delta['NL'], (ship_turn['NL'], ship_fire['Y']))
    rule16 = ctrl.Rule(bullet_time['S'] & theta_delta['NM'], (ship_turn['NM'], ship_fire['Y']))
    rule17 = ctrl.Rule(bullet_time['S'] & theta_delta['NS'], (ship_turn['NS'], ship_fire['Y']))
    # rule18 = ctrl.Rule(bullet_time['S'] & theta_delta['Z'], (ship_turn['Z'], ship_fire['Y']))
    rule19 = ctrl.Rule(bullet_time['S'] & theta_delta['PS'], (ship_turn['PS'], ship_fire['Y']))
    rule20 = ctrl.Rule(bullet_time['S'] & theta_delta['PM'], (ship_turn['PM'], ship_fire['Y']))
    rule21 = ctrl.Rule(bullet_time['S'] & theta_delta['PL'], (ship_turn['PL'], ship_fire['Y']))
     
    #DEBUG
    #bullet_time.view()
    #theta_delta.view()
    #ship_turn.view()
    #ship_fire.view()
     
     
    
    # Declare the fuzzy controller, add the rules 
    # This is an instance variable, and thus available for other methods in the same object. See notes.                         
    # self.targeting_control = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15])

    return [rule1, rule2, rule3, rule5, rule6, rule7, rule8, rule9, rule10, rule12, rule13, rule14, rule15, rule16, rule17, rule19, rule20, rule21]

def thrust_control():   
    # Declare variables
    asteroid_dist = ctrl.Antecedent(np.arange(0, 1.0, 0.001), 'asteroid_dist') # 0 -> 1 to avoid absolutes
    asteroid_angle = ctrl.Antecedent(np.arange(-math.pi / 2, math.pi / 2, 0.001), 'asteroid_angle')
    ship_velo_x = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_velo_x') # -1 -> 1 to avoid absolutes
    ship_velo_y = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_velo_y') # -1 -> 1 to avoid absolutes
    ship_disp_x = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_disp_x') # -1 -> 1 to avoid absolutes
    ship_disp_y = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_disp_y') # -1 -> 1 to avoid absolutes
    ship_heading = ctrl.Antecedent(np.arange(-math.pi / 2, math.pi / 2, 0.001), 'ship_heading')
    ship_thrust = ctrl.Consequent(np.arange(-480.0, 480.0, 1), 'ship_thrust') # from Kessler

    # Declare fuzzy sets for asteroid_dist (relative x-displacement of ship from nearest asteroid)
    asteroid_dist['S'] = fuzz.trimf(asteroid_dist.universe, [0, 0, 0.2])
    asteroid_dist['M'] = fuzz.trimf(asteroid_dist.universe, [0.2, 0.5, 0.8])
    asteroid_dist['L'] = fuzz.trimf(asteroid_dist.universe, [0.8, 1, 1.0])

    # Declare fuzzy sets for asteroid_angle (relative angle of the nearest asteroid to the ship)
    asteroid_angle['N'] = fuzz.trimf(asteroid_angle.universe, [-math.pi/2, -math.pi/4, 0])
    asteroid_angle['W'] = fuzz.trimf(asteroid_angle.universe, [-math.pi/4, 0, math.pi/4])
    asteroid_angle['S'] = fuzz.trimf(asteroid_angle.universe, [0, math.pi/4, math.pi/2])
    # this might be wrong
    asteroid_angle['E1'] = fuzz.trimf(asteroid_angle.universe, [math.pi/4, math.pi/2, math.pi/2])
    asteroid_angle['E2'] = fuzz.trimf(asteroid_angle.universe, [-math.pi/2,- math.pi/2, -math.pi/4])

    # Declare fuzzy sets for ship_velo_x (relative x-velocity of ship)
    ship_velo_x['NL'] = fuzz.trimf(ship_velo_x.universe, [-1.0, -1.0, -0.6])
    ship_velo_x['NM'] = fuzz.trimf(ship_velo_x.universe, [-1.0, -0.6, -0.2])
    ship_velo_x['NS'] = fuzz.trimf(ship_velo_x.universe, [-0.6, -0.2, 0])
    ship_velo_x['Z'] = fuzz.trimf(ship_velo_x.universe, [-0.2, 0, 0.2])
    ship_velo_x['PS'] = fuzz.trimf(ship_velo_x.universe, [0, 0.2, 0.6])
    ship_velo_x['PM'] = fuzz.trimf(ship_velo_x.universe, [0.2, 0.6, 1.0])
    ship_velo_x['PL'] = fuzz.trimf(ship_velo_x.universe, [0.6, 1.0, 1.0])

    # Declare fuzzy sets for ship_velo_y (relative y-velocity of ship)
    ship_velo_y['NL'] = fuzz.trimf(ship_velo_y.universe, [-1.0, -1.0, -0.6])
    ship_velo_y['NM'] = fuzz.trimf(ship_velo_y.universe, [-1.0, -0.6, -0.2])
    ship_velo_y['NS'] = fuzz.trimf(ship_velo_y.universe, [-0.6, -0.2, 0])
    ship_velo_y['Z'] = fuzz.trimf(ship_velo_y.universe, [-0.2, 0, 0.2])
    ship_velo_y['PS'] = fuzz.trimf(ship_velo_y.universe, [0, 0.2, 0.6])
    ship_velo_y['PM'] = fuzz.trimf(ship_velo_y.universe, [0.2, 0.6, 1.0])
    ship_velo_y['PL'] = fuzz.trimf(ship_velo_y.universe, [0.6, 1.0, 1.0])

    # Declare fuzzy sets for ship_disp_x (relative x-displacement of ship from the center)
    ship_disp_x['NL'] = fuzz.trimf(ship_disp_x.universe, [-1.0, -1.0, -0.6])
    ship_disp_x['NM'] = fuzz.trimf(ship_disp_x.universe, [-1.0, -0.6, -0.2])
    ship_disp_x['NS'] = fuzz.trimf(ship_disp_x.universe, [-0.6, -0.2, 0])
    ship_disp_x['Z'] = fuzz.trimf(ship_disp_x.universe, [-0.2, 0, 0.2])
    ship_disp_x['PS'] = fuzz.trimf(ship_disp_x.universe, [0, 0.2, 0.6])
    ship_disp_x['PM'] = fuzz.trimf(ship_disp_x.universe, [0.2, 0.6, 1.0])
    ship_disp_x['PL'] = fuzz.trimf(ship_disp_x.universe, [0.6, 1.0, 1.0])

    # Declare fuzzy sets for ship_disp_y (relative y-displacement of ship from the center)
    ship_disp_y['NL'] = fuzz.trimf(ship_disp_y.universe, [-1.0, -1.0, -0.6])
    ship_disp_y['NM'] = fuzz.trimf(ship_disp_y.universe, [-1.0, -0.6, -0.2])
    ship_disp_y['NS'] = fuzz.trimf(ship_disp_y.universe, [-0.6, -0.2, 0])
    ship_disp_y['Z'] = fuzz.trimf(ship_disp_y.universe, [-0.2, 0, 0.2])
    ship_disp_y['PS'] = fuzz.trimf(ship_disp_y.universe, [0, 0.2, 0.6])
    ship_disp_y['PM'] = fuzz.trimf(ship_disp_y.universe, [0.2, 0.6, 1.0])
    ship_disp_y['PL'] = fuzz.trimf(ship_disp_y.universe, [0.6, 1.0, 1.0])

    # Declare fuzzy sets for ship_heading (direction ship is facing)
    ship_heading['N'] = fuzz.trimf(ship_heading.universe, [-math.pi/2, -math.pi/4, 0])
    ship_heading['W'] = fuzz.trimf(ship_heading.universe, [-math.pi/4, 0, math.pi/4])
    ship_heading['S'] = fuzz.trimf(ship_heading.universe, [0, math.pi/4, math.pi/2])
    # this might be wrong
    ship_heading['E1'] = fuzz.trimf(ship_heading.universe, [math.pi/4, math.pi/2, math.pi/2])
    ship_heading['E2'] = fuzz.trimf(ship_heading.universe, [-math.pi/2,- math.pi/2, -math.pi/4])
    
    # Declare fuzzy sets for the ship_thrust consequent
    ship_thrust['NL'] = fuzz.trimf(ship_thrust.universe, [-480.0, -480.0, -470.0])
    ship_thrust['NM'] = fuzz.trimf(ship_thrust.universe, [-480.0, -470.0, -460.0])
    ship_thrust['NS'] = fuzz.trimf(ship_thrust.universe, [-470.0, -460.0, 0])
    ship_thrust['Z'] = fuzz.trimf(ship_thrust.universe, [-460.0, 0, 460.0])
    ship_thrust['PS'] = fuzz.trimf(ship_thrust.universe, [0, 460.0, 470.0])
    ship_thrust['PM'] = fuzz.trimf(ship_thrust.universe, [460.0, 470.0, 480.0])
    ship_thrust['PL'] = fuzz.trimf(ship_thrust.universe, [470.0, 480.0, 480.0])

    # if far away:
        # if moving toward it, small negative thrust
        # if moving away or not moving, zero thrust
    # if close:
        # if moving toward it, huge negative thrust
        # if not moving, small negative thrust
        # if moving away, zero thrust




    # close by, facing it
        # moving to it
    rule1 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['N'] & asteroid_angle['N']) & (ship_velo_y['PL'] | ship_velo_y['PM']), ship_thrust['NM'])
    rule2 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['S'] & asteroid_angle['S']) & (ship_velo_y['NL'] | ship_velo_y['NM']), ship_thrust['PM'])
    rule3 = ctrl.Rule((asteroid_dist['S']) & ((ship_heading['E1'] | ship_heading['E2']) & (asteroid_angle['E1'] | asteroid_angle['E2'])) & (ship_velo_x['PL'] | ship_velo_x['PM']), ship_thrust['NM'])
    rule4 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['W'] & asteroid_angle['W']) & (ship_velo_x['NL'] | ship_velo_x['NM']), ship_thrust['PM'])
        # moving away from it
    rule5 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['N'] & asteroid_angle['N']) & (ship_velo_y['NL'] | ship_velo_y['NM']), ship_thrust['Z'])
    rule6 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['S'] & asteroid_angle['S']) & (ship_velo_y['PL'] | ship_velo_y['PM']), ship_thrust['Z'])
    rule7 = ctrl.Rule((asteroid_dist['S']) & ((ship_heading['E1'] | ship_heading['E2']) & (asteroid_angle['E1'] | asteroid_angle['E2'])) & (ship_velo_x['NL'] | ship_velo_x['NM']), ship_thrust['Z'])
    rule8 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['W'] & asteroid_angle['W']) & (ship_velo_x['PL'] | ship_velo_x['PM']), ship_thrust['Z'])
        # not moving
    rule9 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['N'] & asteroid_angle['N']) & (ship_velo_y['Z'] | ship_velo_y['NS'] | ship_velo_y['PS']), ship_thrust['NS'])
    rule10 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['S'] & asteroid_angle['S']) & (ship_velo_y['Z'] | ship_velo_y['NS'] | ship_velo_y['PS']), ship_thrust['NS'])
    rule11 = ctrl.Rule((asteroid_dist['S']) & ((ship_heading['E1'] | ship_heading['E2']) & (asteroid_angle['E1'] | asteroid_angle['E2'])) & (ship_velo_x['Z'] | ship_velo_x['NS'] | ship_velo_x['PS']), ship_thrust['NS'])
    rule12 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['W'] & asteroid_angle['W']) & (ship_velo_x['Z'] | ship_velo_x['NS'] | ship_velo_x['PS']), ship_thrust['NS'])

    # close by, facing away
        # moving to it
    rule13 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['N'] & asteroid_angle['S']) & (ship_velo_y['NL'] | ship_velo_y['NM']), ship_thrust['PM'])
    rule14 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['S'] & asteroid_angle['N']) & (ship_velo_y['PL'] | ship_velo_y['PM']), ship_thrust['PM'])
    rule15 = ctrl.Rule((asteroid_dist['S']) & ((ship_heading['E1'] | ship_heading['E2']) & asteroid_angle['W']) & (ship_velo_x['NL'] | ship_velo_x['NM']), ship_thrust['PM'])
    rule16 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['W'] & (asteroid_angle['E1'] | asteroid_angle['E2'])) & (ship_velo_x['PL'] | ship_velo_x['PM']), ship_thrust['PM'])
        # moving away from it
    rule17 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['N'] & asteroid_angle['S']) & (ship_velo_y['PL'] | ship_velo_y['PM']), ship_thrust['Z'])
    rule18 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['S'] & asteroid_angle['N']) & (ship_velo_y['NL'] | ship_velo_y['NM']), ship_thrust['Z'])
    rule19 = ctrl.Rule((asteroid_dist['S']) & ((ship_heading['E1'] | ship_heading['E2']) & asteroid_angle['W']) & (ship_velo_x['PL'] | ship_velo_x['PM']), ship_thrust['Z'])
    rule20 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['W'] & (asteroid_angle['E1'] | asteroid_angle['E2'])) & (ship_velo_x['NL'] | ship_velo_x['NM']), ship_thrust['Z'])
        # not moving
    rule21 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['N'] & asteroid_angle['S']) & (ship_velo_y['Z'] | ship_velo_y['NS'] | ship_velo_y['PS']), ship_thrust['Z'])
    rule22 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['S'] & asteroid_angle['N']) & (ship_velo_y['Z'] | ship_velo_y['NS'] | ship_velo_y['PS']), ship_thrust['Z'])
    rule23 = ctrl.Rule((asteroid_dist['S']) & ((ship_heading['E1'] | ship_heading['E2']) & asteroid_angle['W']) & (ship_velo_x['Z'] | ship_velo_x['NS'] | ship_velo_x['PS']), ship_thrust['Z'])
    rule24 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['W'] & (asteroid_angle['E1'] | asteroid_angle['E2'])) & (ship_velo_x['Z'] | ship_velo_x['NS'] | ship_velo_x['PS']), ship_thrust['Z'])

    # far away, facing it
        # moving to it
    rule25 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['N'] & asteroid_angle['N']) & (ship_velo_y['PL'] | ship_velo_y['PM']), ship_thrust['Z'])
    rule26 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['S'] & asteroid_angle['S']) & (ship_velo_y['NL'] | ship_velo_y['NM']), ship_thrust['Z'])
    rule27 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & ((ship_heading['E1'] | ship_heading['E2']) & (asteroid_angle['E1'] | asteroid_angle['E2'])) & (ship_velo_x['PL'] | ship_velo_x['PM']), ship_thrust['Z'])
    rule28 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['W'] & asteroid_angle['W']) & (ship_velo_x['NL'] | ship_velo_x['NM']), ship_thrust['Z'])
        # moving away from it
    rule29 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['N'] & asteroid_angle['N']) & (ship_velo_y['NL'] | ship_velo_y['NM']), ship_thrust['PM'])
    rule30 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['S'] & asteroid_angle['S']) & (ship_velo_y['PL'] | ship_velo_y['PM']), ship_thrust['PM'])
    rule31 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & ((ship_heading['E1'] | ship_heading['E2']) & (asteroid_angle['E1'] | asteroid_angle['E2'])) & (ship_velo_x['NL'] | ship_velo_x['NM']), ship_thrust['PM'])
    rule32 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['W'] & asteroid_angle['W']) & (ship_velo_x['PL'] | ship_velo_x['PM']), ship_thrust['PM'])
        # not moving
    rule33 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['N'] & asteroid_angle['N']) & (ship_velo_y['Z'] | ship_velo_y['NS'] | ship_velo_y['PS']), ship_thrust['PM'])
    rule34 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['S'] & asteroid_angle['S']) & (ship_velo_y['Z'] | ship_velo_y['NS'] | ship_velo_y['PS']), ship_thrust['PM'])
    rule35 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & ((ship_heading['E1'] | ship_heading['E2']) & (asteroid_angle['E1'] | asteroid_angle['E2'])) & (ship_velo_x['Z'] | ship_velo_x['NS'] | ship_velo_x['PS']), ship_thrust['PM'])
    rule36 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['W'] & asteroid_angle['W']) & (ship_velo_x['Z'] | ship_velo_x['NS'] | ship_velo_x['PS']), ship_thrust['PM'])

    # far away, facing away
        # moving to it
    rule37 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['N'] & asteroid_angle['S']) & (ship_velo_y['NL'] | ship_velo_y['NM']), ship_thrust['PS'])
    rule38 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['S'] & asteroid_angle['N']) & (ship_velo_y['PL'] | ship_velo_y['PM']), ship_thrust['PS'])
    rule39 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & ((ship_heading['E1'] | ship_heading['E2']) & asteroid_angle['W']) & (ship_velo_x['NL'] | ship_velo_x['NM']), ship_thrust['PS'])
    rule40 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['W'] & (asteroid_angle['E1'] | asteroid_angle['E2'])) & (ship_velo_x['PL'] | ship_velo_x['PM']), ship_thrust['PS'])
        # moving away from it
    rule41 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['N'] & asteroid_angle['S']) & (ship_velo_y['PL'] | ship_velo_y['PM']), ship_thrust['Z'])
    rule42 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['S'] & asteroid_angle['N']) & (ship_velo_y['NL'] | ship_velo_y['NM']), ship_thrust['Z'])
    rule43 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & ((ship_heading['E1'] | ship_heading['E2']) & asteroid_angle['W']) & (ship_velo_x['PL'] | ship_velo_x['PM']), ship_thrust['Z'])
    rule44 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['W'] & (asteroid_angle['E1'] | asteroid_angle['E2'])) & (ship_velo_x['NL'] | ship_velo_x['NM']), ship_thrust['Z'])
        # not moving
    rule45 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['N'] & asteroid_angle['S']) & (ship_velo_y['Z'] | ship_velo_y['NS'] | ship_velo_y['PS']), ship_thrust['Z'])
    rule46 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['S'] & asteroid_angle['N']) & (ship_velo_y['Z'] | ship_velo_y['NS'] | ship_velo_y['PS']), ship_thrust['Z'])
    rule47 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & ((ship_heading['E1'] | ship_heading['E2']) & asteroid_angle['W']) & (ship_velo_x['Z'] | ship_velo_x['NS'] | ship_velo_x['PS']), ship_thrust['Z'])
    rule48 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['W'] & (asteroid_angle['E1'] | asteroid_angle['E2'])) & (ship_velo_x['Z'] | ship_velo_x['NS'] | ship_velo_x['PS']), ship_thrust['Z'])

    # close to left edge
    rule49 = ctrl.Rule(ship_disp_x['NL'] & (ship_velo_x['NL'] | ship_velo_x['NM'] | ship_velo_x['NS'] | ship_velo_x['Z']) & ship_heading['W'], ship_thrust['NL'])
    rule50 = ctrl.Rule(ship_disp_x['NL'] & (ship_velo_x['NL'] | ship_velo_x['NM'] | ship_velo_x['NS'] | ship_velo_x['Z']) & (ship_heading['E1'] | ship_heading['E2']), ship_thrust['PL'])
    rule51 = ctrl.Rule(ship_disp_x['NL'] & (ship_velo_x['PL'] | ship_velo_x['PM'] | ship_velo_x['PS']) & ship_heading['W'], ship_thrust['NM'])
    rule52 = ctrl.Rule(ship_disp_x['NL'] & (ship_velo_x['PL'] | ship_velo_x['PM'] | ship_velo_x['PS']) & (ship_heading['E1'] | ship_heading['E2']), ship_thrust['PM'])
    # close to right edge
    rule53 = ctrl.Rule(ship_disp_x['PL'] & (ship_velo_x['NL'] | ship_velo_x['NM'] | ship_velo_x['NS']) & ship_heading['W'], ship_thrust['NM'])
    rule54 = ctrl.Rule(ship_disp_x['PL'] & (ship_velo_x['NL'] | ship_velo_x['NM'] | ship_velo_x['NS']) & (ship_heading['E1'] | ship_heading['E2']), ship_thrust['PM'])
    rule55 = ctrl.Rule(ship_disp_x['PL'] & (ship_velo_x['PL'] | ship_velo_x['PM'] | ship_velo_x['PS'] | ship_velo_x['Z']) & ship_heading['W'], ship_thrust['PL'])
    rule56 = ctrl.Rule(ship_disp_x['PL'] & (ship_velo_x['PL'] | ship_velo_x['PM'] | ship_velo_x['PS'] | ship_velo_x['Z']) & (ship_heading['E1'] | ship_heading['E2']), ship_thrust['NL'])
    # close to bottom edge
    rule57 = ctrl.Rule(ship_disp_y['NL'] & (ship_velo_y['NL'] | ship_velo_y['NM'] | ship_velo_y['NS'] | ship_velo_y['Z']) & ship_heading['N'], ship_thrust['PL'])
    rule58 = ctrl.Rule(ship_disp_y['NL'] & (ship_velo_y['NL'] | ship_velo_y['NM'] | ship_velo_y['NS'] | ship_velo_y['Z']) & ship_heading['S'], ship_thrust['NL'])
    rule59 = ctrl.Rule(ship_disp_y['NL'] & (ship_velo_y['PL'] | ship_velo_y['PM'] | ship_velo_y['PS']) & ship_heading['N'], ship_thrust['NM'])
    rule60 = ctrl.Rule(ship_disp_y['NL'] & (ship_velo_y['PL'] | ship_velo_y['PM'] | ship_velo_y['PS']) & ship_heading['S'], ship_thrust['PM'])
    # close to top edge
    rule61 = ctrl.Rule(ship_disp_y['PL'] & (ship_velo_y['NL'] | ship_velo_y['NM'] | ship_velo_y['NS']) & ship_heading['N'], ship_thrust['NM'])
    rule62 = ctrl.Rule(ship_disp_y['PL'] & (ship_velo_y['NL'] | ship_velo_y['NM'] | ship_velo_y['NS']) & ship_heading['S'], ship_thrust['PM'])
    rule63 = ctrl.Rule(ship_disp_y['PL'] & (ship_velo_y['PL'] | ship_velo_y['PM'] | ship_velo_y['PS'] | ship_velo_y['Z']) & ship_heading['N'], ship_thrust['NL'])
    rule64 = ctrl.Rule(ship_disp_y['PL'] & (ship_velo_y['PL'] | ship_velo_y['PM'] | ship_velo_y['PS'] | ship_velo_y['Z']) & ship_heading['S'], ship_thrust['PL'])
     
    #DEBUG
    # asteroid_dist.view()
    # ship_thrust.view()

    return [
        rule1, 
        rule2, 
        rule3, 
        rule4, 
        rule5, 
        rule6, 
        rule7, 
        rule8, 
        rule9, 
        rule10, 
        rule11, 
        rule12, 
        rule13, 
        rule14, 
        rule15, 
        rule16, 
        rule17, 
        rule18, 
        rule19, 
        rule20, 
        rule21, 
        rule22, 
        rule23, 
        rule24, 
        rule25, 
        rule26, 
        rule27, 
        rule28, 
        rule29, 
        rule30, 
        rule31, 
        rule32, 
        rule33, 
        rule34, 
        rule35, 
        rule36, 
        rule37, 
        rule38, 
        rule39, 
        rule40, 
        rule41, 
        rule42, 
        rule43, 
        rule44, 
        rule45, 
        rule46, 
        rule47, 
        rule48, 
        rule49, 
        rule50, 
        rule51, 
        rule52, 
        rule53, 
        rule54, 
        rule55, 
        rule56, 
        rule57, 
        rule58, 
        rule59, 
        rule60, 
        rule61, 
        rule62, 
        rule63, 
        rule64, 
    ]

def mine_control():

    asteroid_disp_x = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'asteroid_disp_x') # -1 -> 1 to avoid absolutes
    asteroid_disp_y = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'asteroid_disp_y') # -1 -> 1 to avoid absolutes
    ship_velo_x = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_velo_x') # -1 -> 1 to avoid absolutes
    ship_velo_y = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_velo_y') # -1 -> 1 to avoid absolutes
    mine_drop = ctrl.Consequent(np.arange(-1.0, 1.0, 0.1), 'mine_drop') # from Kessler

    # Declare fuzzy sets for asteroid_disp_x (relative x-displacement of ship from nearest asteroid)
    asteroid_disp_x['NL'] = fuzz.trimf(asteroid_disp_x.universe, [-1.0, -1.0, -0.6])
    asteroid_disp_x['NM'] = fuzz.trimf(asteroid_disp_x.universe, [-1.0, -0.6, -0.2])
    asteroid_disp_x['NS'] = fuzz.trimf(asteroid_disp_x.universe, [-0.6, -0.2, 0])
    asteroid_disp_x['Z'] = fuzz.trimf(asteroid_disp_x.universe, [-0.2, 0, 0.2])
    asteroid_disp_x['PS'] = fuzz.trimf(asteroid_disp_x.universe, [0, 0.2, 0.6])
    asteroid_disp_x['PM'] = fuzz.trimf(asteroid_disp_x.universe, [0.2, 0.6, 1.0])
    asteroid_disp_x['PL'] = fuzz.trimf(asteroid_disp_x.universe, [0.6, 1.0, 1.0])

    # Declare fuzzy sets for asteroid_disp_y (relative y-displacement of ship from nearest asteroid)
    asteroid_disp_y['NL'] = fuzz.trimf(asteroid_disp_y.universe, [-1.0, -1.0, -0.6])
    asteroid_disp_y['NM'] = fuzz.trimf(asteroid_disp_y.universe, [-1.0, -0.6, -0.2])
    asteroid_disp_y['NS'] = fuzz.trimf(asteroid_disp_y.universe, [-0.6, -0.2, 0])
    asteroid_disp_y['Z'] = fuzz.trimf(asteroid_disp_y.universe, [-0.2, 0, 0.2])
    asteroid_disp_y['PS'] = fuzz.trimf(asteroid_disp_y.universe, [0, 0.2, 0.6])
    asteroid_disp_y['PM'] = fuzz.trimf(asteroid_disp_y.universe, [0.2, 0.6, 1.0])
    asteroid_disp_y['PL'] = fuzz.trimf(asteroid_disp_y.universe, [0.6, 1.0, 1.0])

    # Declare fuzzy sets for ship_velo_x (relative x-velocity of ship)
    ship_velo_x['NL'] = fuzz.trimf(ship_velo_x.universe, [-1.0, -1.0, -0.6])
    ship_velo_x['NM'] = fuzz.trimf(ship_velo_x.universe, [-1.0, -0.6, -0.2])
    ship_velo_x['NS'] = fuzz.trimf(ship_velo_x.universe, [-0.6, -0.2, 0])
    ship_velo_x['Z'] = fuzz.trimf(ship_velo_x.universe, [-0.2, 0, 0.2])
    ship_velo_x['PS'] = fuzz.trimf(ship_velo_x.universe, [0, 0.2, 0.6])
    ship_velo_x['PM'] = fuzz.trimf(ship_velo_x.universe, [0.2, 0.6, 1.0])
    ship_velo_x['PL'] = fuzz.trimf(ship_velo_x.universe, [0.6, 1.0, 1.0])

    # Declare fuzzy sets for ship_velo_y (relative y-velocity of ship)
    ship_velo_y['NL'] = fuzz.trimf(ship_velo_y.universe, [-1.0, -1.0, -0.6])
    ship_velo_y['NM'] = fuzz.trimf(ship_velo_y.universe, [-1.0, -0.6, -0.2])
    ship_velo_y['NS'] = fuzz.trimf(ship_velo_y.universe, [-0.6, -0.2, 0])
    ship_velo_y['Z'] = fuzz.trimf(ship_velo_y.universe, [-0.2, 0, 0.2])
    ship_velo_y['PS'] = fuzz.trimf(ship_velo_y.universe, [0, 0.2, 0.6])
    ship_velo_y['PM'] = fuzz.trimf(ship_velo_y.universe, [0.2, 0.6, 1.0])
    ship_velo_y['PL'] = fuzz.trimf(ship_velo_y.universe, [0.6, 1.0, 1.0])

    #Declare singleton fuzzy sets for the mine_drop consequent; -1 -> don't drop mine, +1 -> drop mine; this will be  thresholded
    #   and returned as the boolean 'drop_mine'
    mine_drop['N'] = fuzz.trimf(mine_drop.universe, [-1,-1,0.0])
    mine_drop['Y'] = fuzz.trimf(mine_drop.universe, [0.0,1,1]) 

    # if asteroids close and ship is moving, drop mine
    rule1 = ctrl.Rule(asteroid_disp_x['Z'] & asteroid_disp_y['Z'] & (ship_velo_x['NL'] | ship_velo_x['NM'] | ship_velo_x['NS'] | ship_velo_x['PL'] | ship_velo_x['PM'] | ship_velo_x['PS']) & (ship_velo_y['NL'] | ship_velo_y['NM'] | ship_velo_y['NS'] | ship_velo_y['PL'] | ship_velo_y['PM'] | ship_velo_y['PS']), mine_drop['Y'])
    rule8 = ctrl.Rule(asteroid_disp_x['Z'] & asteroid_disp_y['Z'] & (ship_velo_x['NS']| ship_velo_x['PS'] | ship_velo_x['Z']) & (ship_velo_y['NS'] | ship_velo_y['PS'] | ship_velo_y['Z']), mine_drop['N'])
    rule2 = ctrl.Rule(asteroid_disp_x['NS'], mine_drop['N'])
    rule3 = ctrl.Rule(asteroid_disp_x['NM'], mine_drop['N'])
    rule4 = ctrl.Rule(asteroid_disp_x['NL'], mine_drop['N'])
    rule5 = ctrl.Rule(asteroid_disp_x['PS'], mine_drop['N'])
    rule6 = ctrl.Rule(asteroid_disp_x['PM'], mine_drop['N'])
    rule7 = ctrl.Rule(asteroid_disp_x['PL'], mine_drop['N'])

    # rule1 = ctrl.Rule((asteroid_disp_x['NS'] | asteroid_disp_x['Z'] | asteroid_disp_x['PS'] | asteroid_disp_y['NS'] | asteroid_disp_y['Z'] | asteroid_disp_y['PS']) & ((ship_velo_x['NL'] & ship_velo_x['NM']) | (ship_velo_x['PL'] & ship_velo_x['PM']) | (ship_velo_y['NL'] & ship_velo_y['NM']) | (ship_velo_y['PL'] & ship_velo_y['PM'])), mine_drop['Y'])
    
    # if asteroids close but not moving, don't drop mine
    # rule2 = ctrl.Rule((asteroid_disp_x['NS'] | asteroid_disp_x['Z'] | asteroid_disp_x['PS'] | asteroid_disp_y['NS'] | asteroid_disp_y['Z'] | asteroid_disp_y['PS']) & (ship_velo_x['Z'] & ship_velo_y['Z']), mine_drop['N'])

    # if asteroids far away, don't drop mine
    # rule3 = ctrl.Rule((asteroid_disp_x['NM'] | asteroid_disp_x['NL'] | asteroid_disp_x['PM'] | asteroid_disp_x['PL'] | asteroid_disp_y['NM'] | asteroid_disp_y['NL'] | asteroid_disp_y['PM'] | asteroid_disp_y['PL']), mine_drop['N'])

    return [
        rule1,
        rule2,
        rule3,
        rule4,
        rule5,
        rule6,
        rule7,
        rule8,
    ]

# controller adapted from Dr. Dick's controller, with original comments and all.
class ProjectController(KesslerController):
    def __init__(self):
        self.eval_frames = 0 #What is this?
        self.normalization_dist = None

        (
            targetControlRule1,
            targetControlRule2,
            targetControlRule3,
            targetControlRule5,
            targetControlRule6,
            targetControlRule7,
            targetControlRule8,
            targetControlRule9,
            targetControlRule10,
            targetControlRule12,
            targetControlRule13,
            targetControlRule14,
            targetControlRule15,
            targetControlRule16,
            targetControlRule17,
            targetControlRule19,
            targetControlRule20,
            targetControlRule21,
        ) = targeting_control()
            
        self.targeting_control = ctrl.ControlSystem()
        self.targeting_control.addrule(targetControlRule1)
        self.targeting_control.addrule(targetControlRule2)
        self.targeting_control.addrule(targetControlRule3)
        # self.targeting_control.addrule(targetControlRule4)
        self.targeting_control.addrule(targetControlRule5)
        self.targeting_control.addrule(targetControlRule6)
        self.targeting_control.addrule(targetControlRule7)
        self.targeting_control.addrule(targetControlRule8)
        self.targeting_control.addrule(targetControlRule9)
        self.targeting_control.addrule(targetControlRule10)
        # self.targeting_control.addrule(targetControlRule11)
        self.targeting_control.addrule(targetControlRule12)
        self.targeting_control.addrule(targetControlRule13)
        self.targeting_control.addrule(targetControlRule14)
        self.targeting_control.addrule(targetControlRule15)
        self.targeting_control.addrule(targetControlRule16)
        self.targeting_control.addrule(targetControlRule17)
        # self.targeting_control.addrule(targetControlRule18)
        self.targeting_control.addrule(targetControlRule19)
        self.targeting_control.addrule(targetControlRule20)
        self.targeting_control.addrule(targetControlRule21)

        
        (
            thrustRule1, 
            thrustRule2, 
            thrustRule3, 
            thrustRule4, 
            thrustRule5, 
            thrustRule6, 
            thrustRule7, 
            thrustRule8, 
            thrustRule9, 
            thrustRule10, 
            thrustRule11, 
            thrustRule12, 
            thrustRule13, 
            thrustRule14, 
            thrustRule15, 
            thrustRule16, 
            thrustRule17, 
            thrustRule18, 
            thrustRule19, 
            thrustRule20, 
            thrustRule21, 
            thrustRule22, 
            thrustRule23, 
            thrustRule24, 
            thrustRule25, 
            thrustRule26, 
            thrustRule27, 
            thrustRule28, 
            thrustRule29, 
            thrustRule30, 
            thrustRule31, 
            thrustRule32, 
            thrustRule33, 
            thrustRule34, 
            thrustRule35, 
            thrustRule36, 
            thrustRule37, 
            thrustRule38, 
            thrustRule39, 
            thrustRule40, 
            thrustRule41, 
            thrustRule42, 
            thrustRule43, 
            thrustRule44, 
            thrustRule45, 
            thrustRule46, 
            thrustRule47, 
            thrustRule48, 
            thrustRule49, 
            thrustRule50, 
            thrustRule51, 
            thrustRule52, 
            thrustRule53, 
            thrustRule54, 
            thrustRule55, 
            thrustRule56, 
            thrustRule57, 
            thrustRule58, 
            thrustRule59, 
            thrustRule60, 
            thrustRule61, 
            thrustRule62, 
            thrustRule63, 
            thrustRule64, 
        ) = thrust_control()

        self.thrust_control = ctrl.ControlSystem()
        self.thrust_control.addrule(thrustRule1)
        self.thrust_control.addrule(thrustRule2)
        self.thrust_control.addrule(thrustRule3)
        self.thrust_control.addrule(thrustRule4)
        self.thrust_control.addrule(thrustRule5)
        self.thrust_control.addrule(thrustRule6)
        self.thrust_control.addrule(thrustRule7)
        self.thrust_control.addrule(thrustRule8)
        self.thrust_control.addrule(thrustRule9)
        self.thrust_control.addrule(thrustRule10)
        self.thrust_control.addrule(thrustRule11)
        self.thrust_control.addrule(thrustRule12)
        self.thrust_control.addrule(thrustRule13)
        self.thrust_control.addrule(thrustRule14)
        self.thrust_control.addrule(thrustRule15)
        self.thrust_control.addrule(thrustRule16)
        self.thrust_control.addrule(thrustRule17)
        self.thrust_control.addrule(thrustRule18)
        self.thrust_control.addrule(thrustRule19)
        self.thrust_control.addrule(thrustRule20)
        self.thrust_control.addrule(thrustRule21)
        self.thrust_control.addrule(thrustRule22)
        self.thrust_control.addrule(thrustRule23)
        self.thrust_control.addrule(thrustRule24)
        self.thrust_control.addrule(thrustRule25)
        self.thrust_control.addrule(thrustRule26)
        self.thrust_control.addrule(thrustRule27)
        self.thrust_control.addrule(thrustRule28)
        self.thrust_control.addrule(thrustRule29)
        self.thrust_control.addrule(thrustRule30)
        self.thrust_control.addrule(thrustRule31)
        self.thrust_control.addrule(thrustRule32)
        self.thrust_control.addrule(thrustRule33)
        self.thrust_control.addrule(thrustRule34)
        self.thrust_control.addrule(thrustRule35)
        self.thrust_control.addrule(thrustRule36)
        self.thrust_control.addrule(thrustRule37)
        self.thrust_control.addrule(thrustRule38)
        self.thrust_control.addrule(thrustRule39)
        self.thrust_control.addrule(thrustRule40)
        self.thrust_control.addrule(thrustRule41)
        self.thrust_control.addrule(thrustRule42)
        self.thrust_control.addrule(thrustRule43)
        self.thrust_control.addrule(thrustRule44)
        self.thrust_control.addrule(thrustRule45)
        self.thrust_control.addrule(thrustRule46)
        self.thrust_control.addrule(thrustRule47)
        self.thrust_control.addrule(thrustRule48)
        self.thrust_control.addrule(thrustRule49)
        self.thrust_control.addrule(thrustRule50)
        self.thrust_control.addrule(thrustRule51)
        self.thrust_control.addrule(thrustRule52)
        self.thrust_control.addrule(thrustRule53)
        self.thrust_control.addrule(thrustRule54)
        self.thrust_control.addrule(thrustRule55)
        self.thrust_control.addrule(thrustRule56)
        self.thrust_control.addrule(thrustRule57)
        self.thrust_control.addrule(thrustRule58)
        self.thrust_control.addrule(thrustRule59)
        self.thrust_control.addrule(thrustRule60)
        self.thrust_control.addrule(thrustRule61)
        self.thrust_control.addrule(thrustRule62)
        self.thrust_control.addrule(thrustRule63)
        self.thrust_control.addrule(thrustRule64)


        (
            mineRule1,
            mineRule2,
            mineRule3,
            mineRule4,
            mineRule5,
            mineRule6,
            mineRule7,
            mineRule8,
        ) = mine_control()
        self.mine_control = ctrl.ControlSystem()
        self.mine_control.addrule(mineRule1)
        self.mine_control.addrule(mineRule2)
        self.mine_control.addrule(mineRule3)
        self.mine_control.addrule(mineRule4)
        self.mine_control.addrule(mineRule5)
        self.mine_control.addrule(mineRule6)
        self.mine_control.addrule(mineRule7)
        self.mine_control.addrule(mineRule8)
        
        

    def actions(self, ship_state: Dict, game_state: Dict) -> Tuple[float, float, bool]:
        """
        Method processed each time step by this controller.
        """
        # These were the constant actions in the basic demo, just spinning and shooting.
        #thrust = 0 <- How do the values scale with asteroid velocity vector?
        #turn_rate = 90 <- How do the values scale with asteroid velocity vector?
        
        # Answers: Asteroid position and velocity are split into their x,y components in a 2-element ?array each.
        # So are the ship position and velocity, and bullet position and velocity. 
        # Units appear to be meters relative to origin (where?), m/sec, m/sec^2 for thrust.
        # Everything happens in a time increment: delta_time, which appears to be 1/30 sec; this is hardcoded in many places.
        # So, position is updated by multiplying velocity by delta_time, and adding that to position.
        # Ship velocity is updated by multiplying thrust by delta time.
        # Ship position for this time increment is updated after the the thrust was applied.
        

        # My demonstration controller does not move the ship, only rotates it to shoot the nearest asteroid.
        # Goal: demonstrate processing of game state, fuzzy controller, intercept computation 
        # Intercept-point calculation derived from the Law of Cosines, see notes for details and citation.

        # Find the closest asteroid (disregards asteroid velocity)
        ship_pos_x = ship_state["position"][0]     # See src/kesslergame/ship.py in the KesslerGame Github
        ship_pos_y = ship_state["position"][1]       
        closest_asteroid = None
        
        for a in game_state["asteroids"]:
            #Loop through all asteroids, find minimum Eudlidean distance
            curr_dist = math.sqrt((ship_pos_x - a["position"][0])**2 + (ship_pos_y - a["position"][1])**2)
            if closest_asteroid is None :
                # Does not yet exist, so initialize first asteroid as the minimum. Ugh, how to do?
                closest_asteroid = dict(aster = a, dist = curr_dist)
                
            else:    
                # closest_asteroid exists, and is thus initialized. 
                if closest_asteroid["dist"] > curr_dist:
                    # New minimum found
                    closest_asteroid["aster"] = a
                    closest_asteroid["dist"] = curr_dist

        # closest_asteroid is now the nearest asteroid object. 

        # code idea from https://github.com/ThalesGroup/kessler-game/blob/main/examples/test_controller_fuzzy.py
        # gets distance to closest asteroid
        asteroid_displ_x = closest_asteroid["aster"]["position"][0] - ship_pos_x
        asteroid_displ_y = closest_asteroid["aster"]["position"][1] - ship_pos_y
        asteroid_dist = closest_asteroid["dist"]
        asteroid_velo_x = closest_asteroid["aster"]["velocity"][0]
        asteroid_velo_y = closest_asteroid["aster"]["velocity"][1]

        # get max asteroid speed from Kessler code
        speed_scaler = 2.0 + (4.0 - closest_asteroid["aster"]["size"]) / 4.0
        aster_max_speed = 60.0 * speed_scaler

        # get velocity of closest asteroid

        # if it hasn't already been calculated, calculate normalization distance by using map size diagonal/2
        if not self.normalization_dist:
            self.normalization_dist = np.sqrt(game_state["map_size"][0]**2 + game_state["map_size"][1]**2)/2

        # normalize distance
        norm_asteroid_displ_x = asteroid_displ_x/(game_state["map_size"][0] / 2)
        norm_asteroid_displ_y = asteroid_displ_y/(game_state["map_size"][1] / 2)
        # normalize velocity
        norm_asteroid_velo_x = asteroid_velo_x/(aster_max_speed)
        norm_asteroid_velo_y = asteroid_velo_y/(aster_max_speed)
        norm_ast_distance = asteroid_dist/self.normalization_dist

        # calculate relative velocities
        rel_vel_x = ship_state["velocity"][0] / ship_state["max_speed"]
        rel_vel_y = ship_state["velocity"][1] / ship_state["max_speed"]

        # calculate relative displacements
        rel_disp_x = (ship_state["position"][0] - game_state["map_size"][0] / 2)/(game_state["map_size"][0] / 2)
        rel_disp_y = (ship_state["position"][1] - game_state["map_size"][1] / 2)/(game_state["map_size"][1] / 2)

        # Calculate intercept time given ship & asteroid position, asteroid velocity vector, bullet speed (not direction).
        # Based on Law of Cosines calculation, see notes.
        
        # Side D of the triangle is given by closest_asteroid.dist. Need to get the asteroid-ship direction
        #    and the angle of the asteroid's current movement.
        # REMEMBER TRIG FUNCTIONS ARE ALL IN RADAINS!!!
        
        
        asteroid_ship_x = ship_pos_x - closest_asteroid["aster"]["position"][0]
        asteroid_ship_y = ship_pos_y - closest_asteroid["aster"]["position"][1]
        
        asteroid_ship_theta = math.atan2(asteroid_ship_y,asteroid_ship_x)
        
        asteroid_direction = math.atan2(closest_asteroid["aster"]["velocity"][1], closest_asteroid["aster"]["velocity"][0]) # Velocity is a 2-element array [vx,vy].
        my_theta2 = asteroid_ship_theta - asteroid_direction
        cos_my_theta2 = math.cos(my_theta2)
        # Need the speeds of the asteroid and bullet. speed * time is distance to the intercept point
        asteroid_vel = math.sqrt(closest_asteroid["aster"]["velocity"][0]**2 + closest_asteroid["aster"]["velocity"][1]**2)
        bullet_speed = 800 # Hard-coded bullet speed from bullet.py
        
        # Determinant of the quadratic formula b^2-4ac
        targ_det = (-2 * closest_asteroid["dist"] * asteroid_vel * cos_my_theta2)**2 - (4*(asteroid_vel**2 - bullet_speed**2) * (closest_asteroid["dist"]**2))
        
        # Combine the Law of Cosines with the quadratic formula for solve for intercept time. Remember, there are two values produced.
        intrcpt1 = ((2 * closest_asteroid["dist"] * asteroid_vel * cos_my_theta2) + math.sqrt(targ_det)) / (2 * (asteroid_vel**2 -bullet_speed**2))
        intrcpt2 = ((2 * closest_asteroid["dist"] * asteroid_vel * cos_my_theta2) - math.sqrt(targ_det)) / (2 * (asteroid_vel**2-bullet_speed**2))
        
        # Take the smaller intercept time, as long as it is positive; if not, take the larger one.
        if intrcpt1 > intrcpt2:
            if intrcpt2 >= 0:
                bullet_t = intrcpt2
            else:
                bullet_t = intrcpt1
        else:
            if intrcpt1 >= 0:
                bullet_t = intrcpt1
            else:
                bullet_t = intrcpt2
                
        # Calculate the intercept point. The work backwards to find the ship's firing angle my_theta1.
        # Velocities are in m/sec, so bullet_t is in seconds. Add one tik, hardcoded to 1/30 sec.
        intrcpt_x = closest_asteroid["aster"]["position"][0] + closest_asteroid["aster"]["velocity"][0] * (bullet_t+1/30)
        intrcpt_y = closest_asteroid["aster"]["position"][1] + closest_asteroid["aster"]["velocity"][1] * (bullet_t+1/30)

        my_theta1 = math.atan2((intrcpt_y - ship_pos_y),(intrcpt_x - ship_pos_x))
        
        # Lastly, find the difference betwwen firing angle and the ship's current orientation. BUT THE SHIP HEADING IS IN DEGREES.
        shooting_theta = my_theta1 - ((math.pi/180)*ship_state["heading"])
        
        # Wrap all angles to (-pi, pi)
        shooting_theta = (shooting_theta + math.pi) % (2 * math.pi) - math.pi
        
        # Pass the inputs to the rulebase and fire it
        shooting = ctrl.ControlSystemSimulation(self.targeting_control,flush_after_run=1)
        
        shooting.input['bullet_time'] = bullet_t
        shooting.input['theta_delta'] = shooting_theta
        
        shooting.compute()
        
        # Get the defuzzified outputs
        turn_rate = shooting.output['ship_turn']
        
        if shooting.output['ship_fire'] >= 0:
            fire = True
        else:
            fire = False
               
        # Pass the inputs to the rulebase
        thrusting = ctrl.ControlSystemSimulation(self.thrust_control,flush_after_run=1)
        thrusting.input['asteroid_dist'] = norm_ast_distance
        thrusting.input['asteroid_angle'] = asteroid_ship_theta
        thrusting.input['ship_velo_x'] = rel_vel_x
        thrusting.input['ship_velo_y'] = rel_vel_y
        thrusting.input['ship_disp_x'] = rel_disp_x
        thrusting.input['ship_disp_y'] = rel_disp_y
        thrusting.input['ship_heading'] = (ship_state["heading"] * (math.pi / 360)) - (math.pi / 2)

        # print(f"norm_asteroid_displ_x: {norm_asteroid_displ_x}")
        # print(f"norm_asteroid_displ_y: {norm_asteroid_displ_y}")
        # print(f"asteroid_velo_x: {norm_asteroid_velo_x}")
        # print(f"asteroid_velo_x: {norm_asteroid_velo_y}")
        # print(f"ship_velo_x: {rel_vel_x}")
        # print(f"ship_velo_y: {rel_vel_y}")
        # print(f"ship_disp_x: {rel_disp_x}")
        # print(f"ship_disp_y: {rel_disp_y}")
        # print(ship_state["heading"])

        thrusting.compute()

        thrust = thrusting.output["ship_thrust"]

        # And return your three outputs to the game simulation. Controller algorithm complete.
        # thrust = 0.0

        
        mine_drop = ctrl.ControlSystemSimulation(self.mine_control,flush_after_run=1)
        mine_drop.input['asteroid_disp_x'] = norm_asteroid_displ_x
        mine_drop.input['asteroid_disp_y'] = norm_asteroid_displ_y
        mine_drop.input['ship_velo_x'] = rel_vel_x
        mine_drop.input['ship_velo_y'] = rel_vel_y

        mine_drop.compute()

        if mine_drop.output['mine_drop'] >= 0:
            drop_mine = True
        else:
            drop_mine = False
        
        self.eval_frames +=1
        
        #DEBUG
        # print(thrust, bullet_t, shooting_theta, turn_rate, fire)
        
        return thrust, turn_rate, fire, drop_mine

    @property
    def name(self) -> str:
        return "Project Controller"