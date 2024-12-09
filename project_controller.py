"""
NOTE: some code adapted from Scott Dick's controller
"""
from pickle import FALSE
import pickle

from kesslergame import KesslerController
from typing import Dict, Tuple
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import math
import numpy as np

"""
NOTE: targeting_control code adapted from Scott Dick's controller
"""
def targeting_control(chrom):
    # print(chrom)
    # self.targeting_control is the targeting rulebase, which is static in this controller.      
    # Declare variables
    bullet_time = ctrl.Antecedent(np.arange(0,1.0,0.01), 'bullet_time')
    theta_delta = ctrl.Antecedent(np.arange(-1*math.pi/30,math.pi/30,0.01), 'theta_delta') # Radians due to Python
    ship_turn = ctrl.Consequent(np.arange(-180,180,1), 'ship_turn') # Degrees due to Kessler
    ship_fire = ctrl.Consequent(np.arange(-1,1,0.1), 'ship_fire')
    
    # Declare fuzzy sets for bullet_time (how long it takes for the bullet to reach the intercept point)
    bullet_time['S'] = fuzz.trimf(bullet_time.universe, [(chrom[1] + 1.0) / 2, (chrom[2] + 1.0) / 2, (chrom[4] + 1.0) / 2]) 
    bullet_time['M'] = fuzz.trimf(bullet_time.universe, [(chrom[3] + 1.0) / 2, (chrom[5] + 1.0) / 2, (chrom[6] + 1.0) / 2])  
    bullet_time['L'] = fuzz.smf(bullet_time.universe, (chrom[0] + 1.0) / 2, (chrom[7] + 1.0) / 2)

    # Declare fuzzy sets for theta_delta (degrees of turn needed to reach the calculated firing angle)
    # Hard-coded for a game step of 1/30 seconds
    theta_delta['NL'] = fuzz.zmf(theta_delta.universe, chrom[8] * math.pi / 30, chrom[10] * math.pi / 30)
    theta_delta['NM'] = fuzz.trimf(theta_delta.universe, [chrom[9] * math.pi / 30, chrom[11] * math.pi / 30, chrom[13] * math.pi / 30])
    theta_delta['NS'] = fuzz.trimf(theta_delta.universe, [chrom[12] * math.pi / 30, chrom[14] * math.pi / 30, chrom[16] * math.pi / 30])
    theta_delta['PS'] = fuzz.trimf(theta_delta.universe, [chrom[15] * math.pi / 30, chrom[17] * math.pi / 30, chrom[19] * math.pi / 30])
    theta_delta['PM'] = fuzz.trimf(theta_delta.universe, [chrom[18] * math.pi / 30, chrom[20] * math.pi / 30, chrom[22] * math.pi / 30])
    theta_delta['PL'] = fuzz.smf(theta_delta.universe, chrom[21] * math.pi / 30, chrom[23] * math.pi / 30)

    # Declare fuzzy sets for the ship_turn consequent; this will be returned as turn_rate.
    # Hard-coded for a game step of 1/30 seconds
    ship_turn['NL'] = fuzz.trimf(ship_turn.universe, [chrom[24] * 180, chrom[25] * 180, chrom[27] * 180])
    ship_turn['NM'] = fuzz.trimf(ship_turn.universe, [chrom[26] * 180, chrom[28] * 180, chrom[30] * 180])
    ship_turn['NS'] = fuzz.trimf(ship_turn.universe, [chrom[29] * 180, chrom[31] * 180, chrom[33] * 180])
    ship_turn['PS'] = fuzz.trimf(ship_turn.universe, [chrom[32] * 180, chrom[34] * 180, chrom[36] * 180])
    ship_turn['PM'] = fuzz.trimf(ship_turn.universe, [chrom[35] * 180, chrom[37] * 180, chrom[39] * 180])
    ship_turn['PL'] = fuzz.trimf(ship_turn.universe, [chrom[38] * 180, chrom[40] * 180, chrom[41] * 180])

    # Declare singleton fuzzy sets for the ship_fire consequent; -1 -> don't fire, +1 -> fire; this will be thresholded
    # and returned as the boolean 'fire'
    ship_fire['N'] = fuzz.trimf(ship_fire.universe, [chrom[42], chrom[43], chrom[45]])
    ship_fire['Y'] = fuzz.trimf(ship_fire.universe, [chrom[44], chrom[46], chrom[47]])

            
    #Declare each fuzzy rule
    rule1 = ctrl.Rule(bullet_time['L'] & theta_delta['NL'], (ship_turn['NL'], ship_fire['Y']))
    rule2 = ctrl.Rule(bullet_time['L'] & theta_delta['NM'], (ship_turn['NM'], ship_fire['Y']))
    rule3 = ctrl.Rule(bullet_time['L'] & theta_delta['NS'], (ship_turn['NS'], ship_fire['Y']))
    rule5 = ctrl.Rule(bullet_time['L'] & theta_delta['PS'], (ship_turn['PS'], ship_fire['Y']))
    rule6 = ctrl.Rule(bullet_time['L'] & theta_delta['PM'], (ship_turn['PM'], ship_fire['Y']))
    rule7 = ctrl.Rule(bullet_time['L'] & theta_delta['PL'], (ship_turn['PL'], ship_fire['Y']))
    rule8 = ctrl.Rule(bullet_time['M'] & theta_delta['NL'], (ship_turn['NL'], ship_fire['Y']))
    rule9 = ctrl.Rule(bullet_time['M'] & theta_delta['NM'], (ship_turn['NM'], ship_fire['Y']))
    rule10 = ctrl.Rule(bullet_time['M'] & theta_delta['NS'], (ship_turn['NS'], ship_fire['Y']))
    rule12 = ctrl.Rule(bullet_time['M'] & theta_delta['PS'], (ship_turn['PS'], ship_fire['Y']))
    rule13 = ctrl.Rule(bullet_time['M'] & theta_delta['PM'], (ship_turn['PM'], ship_fire['N']))
    rule14 = ctrl.Rule(bullet_time['M'] & theta_delta['PL'], (ship_turn['PL'], ship_fire['N']))
    rule15 = ctrl.Rule(bullet_time['S'] & theta_delta['NL'], (ship_turn['NL'], ship_fire['Y']))
    rule16 = ctrl.Rule(bullet_time['S'] & theta_delta['NM'], (ship_turn['NM'], ship_fire['Y']))
    rule17 = ctrl.Rule(bullet_time['S'] & theta_delta['NS'], (ship_turn['NS'], ship_fire['Y']))
    rule19 = ctrl.Rule(bullet_time['S'] & theta_delta['PS'], (ship_turn['PS'], ship_fire['Y']))
    rule20 = ctrl.Rule(bullet_time['S'] & theta_delta['PM'], (ship_turn['PM'], ship_fire['Y']))
    rule21 = ctrl.Rule(bullet_time['S'] & theta_delta['PL'], (ship_turn['PL'], ship_fire['Y']))

    return [rule1, rule2, rule3, rule5, rule6, rule7, rule8, rule9, rule10, rule12, rule13, rule14, rule15, rule16, rule17, rule19, rule20, rule21]

def thrust_control(chrom):
    # Declare variables
    asteroid_dist = ctrl.Antecedent(np.arange(0, 1.0, 0.01), 'asteroid_dist') # 0 -> 1 to avoid absolutes
    asteroid_angle = ctrl.Antecedent(np.arange(-math.pi / 2, math.pi / 2, 0.01), 'asteroid_angle')
    ship_velo_x = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_velo_x') # -1 -> 1 to avoid absolutes
    ship_velo_y = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_velo_y') # -1 -> 1 to avoid absolutes
    # ship_disp_x = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_disp_x') # -1 -> 1 to avoid absolutes
    # ship_disp_y = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_disp_y') # -1 -> 1 to avoid absolutes
    ship_heading = ctrl.Antecedent(np.arange(-math.pi / 2, math.pi / 2, 0.01), 'ship_heading')
    ship_thrust = ctrl.Consequent(np.arange(-480.0, 480.0, 1), 'ship_thrust') # from Kessler

    # Declare fuzzy sets for asteroid_dist (relative x-displacement of ship from nearest asteroid)
    # print(f"asteroid_dist: {chrom[48:57]}")
    asteroid_dist['S'] = fuzz.trimf(asteroid_dist.universe, [(chrom[48] + 1.0) / 2, (chrom[49] + 1.0) / 2, (chrom[51] + 1.0) / 2])
    asteroid_dist['M'] = fuzz.trimf(asteroid_dist.universe, [(chrom[50] + 1.0) / 2, (chrom[52] + 1.0) / 2, (chrom[54] + 1.0) / 2])
    asteroid_dist['L'] = fuzz.trimf(asteroid_dist.universe, [(chrom[53] + 1.0) / 2, (chrom[55] + 1.0) / 2, (chrom[56] + 1.0) / 2])

    # Declare fuzzy sets for asteroid_angle (relative angle of the nearest asteroid to the ship)
    # print(f"asteroid_angle: {chrom[57:72]}")
    asteroid_angle['N'] = fuzz.trimf(asteroid_angle.universe, [chrom[57] * (math.pi / 2), chrom[58] * (math.pi / 2), chrom[60] * (math.pi / 2)])
    asteroid_angle['W'] = fuzz.trimf(asteroid_angle.universe, [chrom[59] * (math.pi / 2), chrom[61] * (math.pi / 2), chrom[63] * (math.pi / 2)])
    asteroid_angle['S'] = fuzz.trimf(asteroid_angle.universe, [chrom[62] * (math.pi / 2), chrom[64] * (math.pi / 2), chrom[66] * (math.pi / 2)])
    asteroid_angle['E1'] = fuzz.trimf(asteroid_angle.universe, [chrom[65] * (math.pi / 2), chrom[67] * (math.pi / 2), chrom[69] * (math.pi / 2)])
    asteroid_angle['E2'] = fuzz.trimf(asteroid_angle.universe, [chrom[68] * (math.pi / 2), chrom[70] * (math.pi / 2), chrom[71] * (math.pi / 2)])

    # Declare fuzzy sets for ship_velo_x (relative x-velocity of ship)
    # print(f"ship_velo_x: {chrom[72:93]}")
    ship_velo_x['NL'] = fuzz.trimf(ship_velo_x.universe, [chrom[72], chrom[73], chrom[75]])
    ship_velo_x['NM'] = fuzz.trimf(ship_velo_x.universe, [chrom[74], chrom[76], chrom[78]])
    ship_velo_x['NS'] = fuzz.trimf(ship_velo_x.universe, [chrom[77], chrom[79], chrom[81]])
    ship_velo_x['Z'] = fuzz.trimf(ship_velo_x.universe, [chrom[80], chrom[82], chrom[84]])
    ship_velo_x['PS'] = fuzz.trimf(ship_velo_x.universe, [chrom[83], chrom[85], chrom[87]])
    ship_velo_x['PM'] = fuzz.trimf(ship_velo_x.universe, [chrom[86], chrom[88], chrom[90]])
    ship_velo_x['PL'] = fuzz.trimf(ship_velo_x.universe, [chrom[89], chrom[91], chrom[92]])

    # Declare fuzzy sets for ship_velo_y (relative y-velocity of ship)
    # print(f"ship_velo_y: {chrom[93:114]}")
    ship_velo_y['NL'] = fuzz.trimf(ship_velo_y.universe, [chrom[93], chrom[94], chrom[96]])
    ship_velo_y['NM'] = fuzz.trimf(ship_velo_y.universe, [chrom[95], chrom[97], chrom[99]])
    ship_velo_y['NS'] = fuzz.trimf(ship_velo_y.universe, [chrom[98], chrom[100], chrom[102]])
    ship_velo_y['Z'] = fuzz.trimf(ship_velo_y.universe, [chrom[101], chrom[103], chrom[105]])
    ship_velo_y['PS'] = fuzz.trimf(ship_velo_y.universe, [chrom[104], chrom[106], chrom[108]])
    ship_velo_y['PM'] = fuzz.trimf(ship_velo_y.universe, [chrom[107], chrom[109], chrom[111]])
    ship_velo_y['PL'] = fuzz.trimf(ship_velo_y.universe, [chrom[110], chrom[112], chrom[113]])

    # Declare fuzzy sets for ship_heading (direction ship is facing)
    # print(f"ship_heading: {chrom[114:129]}")
    ship_heading['N'] = fuzz.trimf(ship_heading.universe, [chrom[114] * (math.pi / 2), chrom[115] * (math.pi / 2), chrom[117] * (math.pi / 2)])
    ship_heading['W'] = fuzz.trimf(ship_heading.universe, [chrom[116] * (math.pi / 2), chrom[118] * (math.pi / 2), chrom[120] * (math.pi / 2)])
    ship_heading['S'] = fuzz.trimf(ship_heading.universe, [chrom[119] * (math.pi / 2), chrom[121] * (math.pi / 2), chrom[123] * (math.pi / 2)])
    ship_heading['E1'] = fuzz.trimf(ship_heading.universe, [chrom[122] * (math.pi / 2), chrom[124] * (math.pi / 2), chrom[126] * (math.pi / 2)])
    ship_heading['E2'] = fuzz.trimf(ship_heading.universe, [chrom[125] * (math.pi / 2), chrom[127] * (math.pi / 2), chrom[128] * (math.pi / 2)])

    # Declare fuzzy sets for the ship_thrust consequent
    # print(f"ship_thrust: {chrom[129:150]}")
    ship_thrust['NL'] = fuzz.trimf(ship_thrust.universe, [chrom[129] * 480, chrom[130] * 480, chrom[132] * 480])
    ship_thrust['NM'] = fuzz.trimf(ship_thrust.universe, [chrom[131] * 480, chrom[133] * 480, chrom[135] * 480])
    ship_thrust['NS'] = fuzz.trimf(ship_thrust.universe, [chrom[134] * 480, chrom[136] * 480, chrom[138] * 480])
    ship_thrust['Z'] = fuzz.trimf(ship_thrust.universe, [chrom[137] * 480, chrom[139] * 480, chrom[141] * 480])
    ship_thrust['PS'] = fuzz.trimf(ship_thrust.universe, [chrom[140] * 480, chrom[142] * 480, chrom[144] * 480])
    ship_thrust['PM'] = fuzz.trimf(ship_thrust.universe, [chrom[143] * 480, chrom[145] * 480, chrom[147] * 480])
    ship_thrust['PL'] = fuzz.trimf(ship_thrust.universe, [chrom[146] * 480, chrom[148] * 480, chrom[149] * 480])


    # close by, facing it
        # moving to it
    rule1 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['N'] & asteroid_angle['N']) & (ship_velo_y['PL'] | ship_velo_y['PM']), ship_thrust['NL'])
    rule2 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['S'] & asteroid_angle['S']) & (ship_velo_y['NL'] | ship_velo_y['NM']), ship_thrust['NL'])
    rule3 = ctrl.Rule((asteroid_dist['S']) & ((ship_heading['E1'] | ship_heading['E2']) & (asteroid_angle['E1'] | asteroid_angle['E2'])) & (ship_velo_x['PL'] | ship_velo_x['PM']), ship_thrust['NL'])
    rule4 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['W'] & asteroid_angle['W']) & (ship_velo_x['NL'] | ship_velo_x['NM']), ship_thrust['NL'])
        # moving away from it
    rule5 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['N'] & asteroid_angle['N']) & (ship_velo_y['NL'] | ship_velo_y['NM']), ship_thrust['Z'])
    rule6 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['S'] & asteroid_angle['S']) & (ship_velo_y['PL'] | ship_velo_y['PM']), ship_thrust['Z'])
    rule7 = ctrl.Rule((asteroid_dist['S']) & ((ship_heading['E1'] | ship_heading['E2']) & (asteroid_angle['E1'] | asteroid_angle['E2'])) & (ship_velo_x['NL'] | ship_velo_x['NM']), ship_thrust['Z'])
    rule8 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['W'] & asteroid_angle['W']) & (ship_velo_x['PL'] | ship_velo_x['PM']), ship_thrust['Z'])
        # not moving
    rule9 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['N'] & asteroid_angle['N']) & (ship_velo_y['Z'] | ship_velo_y['NS'] | ship_velo_y['PS']), ship_thrust['NM'])
    rule10 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['S'] & asteroid_angle['S']) & (ship_velo_y['Z'] | ship_velo_y['NS'] | ship_velo_y['PS']), ship_thrust['NM'])
    rule11 = ctrl.Rule((asteroid_dist['S']) & ((ship_heading['E1'] | ship_heading['E2']) & (asteroid_angle['E1'] | asteroid_angle['E2'])) & (ship_velo_x['Z'] | ship_velo_x['NS'] | ship_velo_x['PS']), ship_thrust['NM'])
    rule12 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['W'] & asteroid_angle['W']) & (ship_velo_x['Z'] | ship_velo_x['NS'] | ship_velo_x['PS']), ship_thrust['NM'])

    # close by, facing away
        # moving to it
    rule13 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['N'] & (asteroid_angle['S'] | asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['W'])) & (ship_velo_y['NL'] | ship_velo_y['NM']), ship_thrust['PM'])
    rule14 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['S'] & (asteroid_angle['N'] | asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['W'])) & (ship_velo_y['PL'] | ship_velo_y['PM']), ship_thrust['PM'])
    rule15 = ctrl.Rule((asteroid_dist['S']) & ((ship_heading['E1'] | ship_heading['E2']) & (asteroid_angle['W'] | asteroid_angle['S'] | asteroid_angle['N'])) & (ship_velo_x['NL'] | ship_velo_x['NM']), ship_thrust['PM'])
    rule16 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['W'] & (asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['N'] | asteroid_angle['S'])) & (ship_velo_x['PL'] | ship_velo_x['PM']), ship_thrust['PM'])
        # moving away from it
    rule17 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['N'] & (asteroid_angle['S'] | asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['W'])) & (ship_velo_y['PL'] | ship_velo_y['PM']), ship_thrust['Z'])
    rule18 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['S'] & (asteroid_angle['N'] | asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['W'])) & (ship_velo_y['NL'] | ship_velo_y['NM']), ship_thrust['Z'])
    rule19 = ctrl.Rule((asteroid_dist['S']) & ((ship_heading['E1'] | ship_heading['E2']) & (asteroid_angle['W'] | asteroid_angle['S'] | asteroid_angle['N'])) & (ship_velo_x['PL'] | ship_velo_x['PM']), ship_thrust['Z'])
    rule20 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['W'] & (asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['N'] | asteroid_angle['S'])) & (ship_velo_x['NL'] | ship_velo_x['NM']), ship_thrust['Z'])
        # not moving
    rule21 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['N'] & (asteroid_angle['S'] | asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['W'])) & (ship_velo_y['Z'] | ship_velo_y['NS'] | ship_velo_y['PS']), ship_thrust['NS'])
    rule22 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['S'] & (asteroid_angle['N'] | asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['W'])) & (ship_velo_y['Z'] | ship_velo_y['NS'] | ship_velo_y['PS']), ship_thrust['NS'])
    rule23 = ctrl.Rule((asteroid_dist['S']) & ((ship_heading['E1'] | ship_heading['E2']) & (asteroid_angle['W'] | asteroid_angle['S'] | asteroid_angle['N'])) & (ship_velo_x['Z'] | ship_velo_x['NS'] | ship_velo_x['PS']), ship_thrust['NS'])
    rule24 = ctrl.Rule((asteroid_dist['S']) & (ship_heading['W'] & (asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['N'] | asteroid_angle['S'])) & (ship_velo_x['Z'] | ship_velo_x['NS'] | ship_velo_x['PS']), ship_thrust['NS'])

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
    rule33 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['N'] & asteroid_angle['N']) & (ship_velo_y['Z'] | ship_velo_y['NS'] | ship_velo_y['PS']), ship_thrust['PS'])
    rule34 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['S'] & asteroid_angle['S']) & (ship_velo_y['Z'] | ship_velo_y['NS'] | ship_velo_y['PS']), ship_thrust['PS'])
    rule35 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & ((ship_heading['E1'] | ship_heading['E2']) & (asteroid_angle['E1'] | asteroid_angle['E2'])) & (ship_velo_x['Z'] | ship_velo_x['NS'] | ship_velo_x['PS']), ship_thrust['PS'])
    rule36 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['W'] & asteroid_angle['W']) & (ship_velo_x['Z'] | ship_velo_x['NS'] | ship_velo_x['PS']), ship_thrust['PS'])

    # far away, facing away
        # moving to it
    rule37 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['N'] & (asteroid_angle['S'] | asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['W'])) & (ship_velo_y['NL'] | ship_velo_y['NM']), ship_thrust['PS'])
    rule38 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['S'] & (asteroid_angle['N'] | asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['W'])) & (ship_velo_y['PL'] | ship_velo_y['PM']), ship_thrust['PS'])
    rule39 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & ((ship_heading['E1'] | ship_heading['E2']) & (asteroid_angle['W'] | asteroid_angle['S'] | asteroid_angle['N'])) & (ship_velo_x['NL'] | ship_velo_x['NM']), ship_thrust['PS'])
    rule40 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['W'] & (asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['N'] | asteroid_angle['S'])) & (ship_velo_x['PL'] | ship_velo_x['PM']), ship_thrust['PS'])
        # moving away from it
    rule41 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['N'] & (asteroid_angle['S'] | asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['W'])) & (ship_velo_y['PL'] | ship_velo_y['PM']), ship_thrust['Z'])
    rule42 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['S'] & (asteroid_angle['N'] | asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['W'])) & (ship_velo_y['NL'] | ship_velo_y['NM']), ship_thrust['Z'])
    rule43 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & ((ship_heading['E1'] | ship_heading['E2']) & (asteroid_angle['W'] | asteroid_angle['S'] | asteroid_angle['N'])) & (ship_velo_x['PL'] | ship_velo_x['PM']), ship_thrust['Z'])
    rule44 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['W'] & (asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['N'] | asteroid_angle['S'])) & (ship_velo_x['NL'] | ship_velo_x['NM']), ship_thrust['Z'])
        # not moving
    rule45 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['N'] & (asteroid_angle['S'] | asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['W'])) & (ship_velo_y['Z'] | ship_velo_y['NS'] | ship_velo_y['PS']), ship_thrust['Z'])
    rule46 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['S'] & (asteroid_angle['N'] | asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['W'])) & (ship_velo_y['Z'] | ship_velo_y['NS'] | ship_velo_y['PS']), ship_thrust['Z'])
    rule47 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & ((ship_heading['E1'] | ship_heading['E2']) & (asteroid_angle['W'] | asteroid_angle['S'] | asteroid_angle['N'])) & (ship_velo_x['Z'] | ship_velo_x['NS'] | ship_velo_x['PS']), ship_thrust['Z'])
    rule48 = ctrl.Rule((asteroid_dist['M'] | asteroid_dist['L']) & (ship_heading['W'] & (asteroid_angle['E1'] | asteroid_angle['E2'] | asteroid_angle['N'] | asteroid_angle['S'])) & (ship_velo_x['Z'] | ship_velo_x['NS'] | ship_velo_x['PS']), ship_thrust['Z'])
     
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
    ]

def mine_control(chrom):

    asteroid_disp_x = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'asteroid_disp_x') # -1 -> 1 to avoid absolutes
    asteroid_disp_y = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'asteroid_disp_y') # -1 -> 1 to avoid absolutes
    ship_velo_x = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_velo_x') # -1 -> 1 to avoid absolutes
    ship_velo_y = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_velo_y') # -1 -> 1 to avoid absolutes
    mine_drop = ctrl.Consequent(np.arange(-1.0, 1.0, 0.01), 'mine_drop') # from Kessler

    # Declare fuzzy sets for asteroid_disp_x (relative x-displacement of ship from nearest asteroid)
    asteroid_disp_x['NL'] = fuzz.trimf(asteroid_disp_x.universe, [chrom[150], chrom[151], chrom[153]])
    asteroid_disp_x['NM'] = fuzz.trimf(asteroid_disp_x.universe, [chrom[152], chrom[154], chrom[156]])
    asteroid_disp_x['NS'] = fuzz.trimf(asteroid_disp_x.universe, [chrom[155], chrom[157], chrom[159]])
    asteroid_disp_x['Z'] = fuzz.trimf(asteroid_disp_x.universe, [chrom[158], chrom[160], chrom[162]])
    asteroid_disp_x['PS'] = fuzz.trimf(asteroid_disp_x.universe, [chrom[161], chrom[163], chrom[165]])
    asteroid_disp_x['PM'] = fuzz.trimf(asteroid_disp_x.universe, [chrom[164], chrom[166], chrom[168]])
    asteroid_disp_x['PL'] = fuzz.trimf(asteroid_disp_x.universe, [chrom[167], chrom[169], chrom[170]])
    
    # Declare fuzzy sets for asteroid_disp_y (relative y-displacement of ship from nearest asteroid)
    asteroid_disp_y['NL'] = fuzz.trimf(asteroid_disp_y.universe, [chrom[171], chrom[172], chrom[174]])
    asteroid_disp_y['NM'] = fuzz.trimf(asteroid_disp_y.universe, [chrom[173], chrom[175], chrom[177]])
    asteroid_disp_y['NS'] = fuzz.trimf(asteroid_disp_y.universe, [chrom[176], chrom[178], chrom[180]])
    asteroid_disp_y['Z'] = fuzz.trimf(asteroid_disp_y.universe, [chrom[179], chrom[181], chrom[183]])
    asteroid_disp_y['PS'] = fuzz.trimf(asteroid_disp_y.universe, [chrom[182], chrom[184], chrom[186]])
    asteroid_disp_y['PM'] = fuzz.trimf(asteroid_disp_y.universe, [chrom[185], chrom[187], chrom[189]])
    asteroid_disp_y['PL'] = fuzz.trimf(asteroid_disp_y.universe, [chrom[188], chrom[190], chrom[191]])
    
    # Declare fuzzy sets for ship_velo_x (relative x-velocity of ship)
    ship_velo_x['NL'] = fuzz.trimf(ship_velo_x.universe, [chrom[192], chrom[193], chrom[195]])
    ship_velo_x['NM'] = fuzz.trimf(ship_velo_x.universe, [chrom[194], chrom[196], chrom[198]])
    ship_velo_x['NS'] = fuzz.trimf(ship_velo_x.universe, [chrom[197], chrom[199], chrom[201]])
    ship_velo_x['Z'] = fuzz.trimf(ship_velo_x.universe, [chrom[200], chrom[202], chrom[204]])
    ship_velo_x['PS'] = fuzz.trimf(ship_velo_x.universe, [chrom[203], chrom[205], chrom[207]])
    ship_velo_x['PM'] = fuzz.trimf(ship_velo_x.universe, [chrom[206], chrom[208], chrom[210]])
    ship_velo_x['PL'] = fuzz.trimf(ship_velo_x.universe, [chrom[209], chrom[211], chrom[212]])

    # Declare fuzzy sets for ship_velo_y (relative y-velocity of ship)
    ship_velo_y['NL'] = fuzz.trimf(ship_velo_y.universe, [chrom[213], chrom[214], chrom[216]])
    ship_velo_y['NM'] = fuzz.trimf(ship_velo_y.universe, [chrom[215], chrom[217], chrom[219]])
    ship_velo_y['NS'] = fuzz.trimf(ship_velo_y.universe, [chrom[218], chrom[220], chrom[222]])
    ship_velo_y['Z'] = fuzz.trimf(ship_velo_y.universe, [chrom[221], chrom[223], chrom[225]])
    ship_velo_y['PS'] = fuzz.trimf(ship_velo_y.universe, [chrom[224], chrom[226], chrom[228]])
    ship_velo_y['PM'] = fuzz.trimf(ship_velo_y.universe, [chrom[227], chrom[229], chrom[231]])
    ship_velo_y['PL'] = fuzz.trimf(ship_velo_y.universe, [chrom[230], chrom[232], chrom[233]])

    # Declare singleton fuzzy sets for the mine_drop consequent; -1 -> don't drop mine, +1 -> drop mine
    mine_drop['N'] = fuzz.trimf(mine_drop.universe, [chrom[234], chrom[235], chrom[237]])
    mine_drop['Y'] = fuzz.trimf(mine_drop.universe, [chrom[236], chrom[238], chrom[239]])


    # if asteroids close and ship is moving, drop mine
    rule1 = ctrl.Rule(asteroid_disp_x['Z'] & asteroid_disp_y['Z'] & (ship_velo_x['NL'] | ship_velo_x['NM'] | ship_velo_x['PL'] | ship_velo_x['PM'] | ship_velo_y['NL'] | ship_velo_y['NM'] | ship_velo_y['PL'] | ship_velo_y['PM']), mine_drop['Y'])
    rule2 = ctrl.Rule(asteroid_disp_x['NS'], mine_drop['N'])
    rule3 = ctrl.Rule(asteroid_disp_x['NM'], mine_drop['N'])
    rule4 = ctrl.Rule(asteroid_disp_x['NL'], mine_drop['N'])
    rule5 = ctrl.Rule(asteroid_disp_x['PS'], mine_drop['N'])
    rule6 = ctrl.Rule(asteroid_disp_x['PM'], mine_drop['N'])
    rule7 = ctrl.Rule(asteroid_disp_x['PL'], mine_drop['N'])
    rule8 = ctrl.Rule(asteroid_disp_x['Z'] & asteroid_disp_y['Z'] & (ship_velo_x['NS']| ship_velo_x['PS'] | ship_velo_x['Z'] | ship_velo_y['NS'] | ship_velo_y['PS'] | ship_velo_y['Z']), mine_drop['N'])
    rule9 = ctrl.Rule(asteroid_disp_y['NS'], mine_drop['N'])
    rule10 = ctrl.Rule(asteroid_disp_y['NM'], mine_drop['N'])
    rule11 = ctrl.Rule(asteroid_disp_y['NL'], mine_drop['N'])
    rule12 = ctrl.Rule(asteroid_disp_y['PS'], mine_drop['N'])
    rule13 = ctrl.Rule(asteroid_disp_y['PM'], mine_drop['N'])
    rule14 = ctrl.Rule(asteroid_disp_y['PL'], mine_drop['N'])

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
    ]

# controller adapted from Dr. Dick's controller, with original comments and all.
class ProjectController(KesslerController):
    def __init__(self, solution=[]):
        self.eval_frames = 0 #What is this?
        self.normalization_dist = None

        if len(solution) == 0:
            try:
                sol_file = open('ga_instance', 'rb')
                best_sol_data_from_file = pickle.load(sol_file)
                values = best_sol_data_from_file['parameters']
                sol_file.close()
                solution = values
            
            except:
                values = []

                # my custom values to start initialization
                values.extend([-1, -1, -1, -1, -0.9, -0.9, -0.8, 1])
                values.extend([x/(math.pi / 30) for x in sorted([-1*math.pi/30, -2*math.pi/90, -1*math.pi/30, -2*math.pi/90, -1*math.pi/90, -2*math.pi/90, -1*math.pi/90, math.pi/90, -1*math.pi/90, math.pi/90, 2*math.pi/90, math.pi/90, 2*math.pi/90, math.pi/30, 2*math.pi/90, math.pi/30])])
                values.extend([x/180 for x in sorted([-180, -180, -120, -180, -120, -60, -120, -60, 60, -60, 60, 120, 60, 120, 180, 120, 180, 180])])
                values.extend(sorted([-1, -1, 0.0, 0.0, 1, 1]))
                values.extend([(x * 2) - 1 for x in sorted([0, 0, 0.2, 0.2, 0.5, 0.8, 0.8, 1, 1.0])])
                values.extend([x/(math.pi / 2) for x in sorted([-math.pi/2, -math.pi/4, 0, -math.pi/4, 0, math.pi/4, 0, math.pi/4, math.pi/2, math.pi/4, math.pi/2, math.pi/2, -math.pi/2, -math.pi/2, -math.pi/4])])
                values.extend(sorted([-1.0, -1.0, -0.6, -1.0, -0.6, -0.2, -0.6, -0.2, 0, -0.2, 0, 0.2, 0, 0.2, 0.6, 0.2, 0.6, 1.0, 0.6, 1.0, 1.0]))
                values.extend(sorted([-1.0, -1.0, -0.6, -1.0, -0.6, -0.2, -0.6, -0.2, 0, -0.2, 0, 0.2, 0, 0.2, 0.6, 0.2, 0.6, 1.0, 0.6, 1.0, 1.0]))
                values.extend([x/(math.pi / 2) for x in sorted([-math.pi/2, -math.pi/4, 0, -math.pi/4, 0, math.pi/4, 0, math.pi/4, math.pi/2, math.pi/4, math.pi/2, math.pi/2, -math.pi/2, -math.pi/2, -math.pi/4])])
                values.extend([x / 480 for x in sorted([-480.0, -480.0, -460.0, -480.0, -460.0, -420.0, -460.0, -420.0, 0, -420.0, 0, 420.0, 0, 420.0, 460.0, 420.0, 460.0, 480.0, 460.0, 480.0, 480.0])])
                values.extend(sorted([-1.0, -1.0, -0.6, -1.0, -0.6, -0.2, -0.6, -0.2, 0, -0.2, 0, 0.2, 0, 0.2, 0.6, 0.2, 0.6, 1.0, 0.6, 1.0, 1.0]))
                values.extend(sorted([-1.0, -1.0, -0.6, -1.0, -0.6, -0.2, -0.6, -0.2, 0, -0.2, 0, 0.2, 0, 0.2, 0.6, 0.2, 0.6, 1.0, 0.6, 1.0, 1.0]))
                values.extend(sorted([-1.0, -1.0, -0.6, -1.0, -0.6, -0.2, -0.6, -0.2, 0, -0.2, 0, 0.2, 0, 0.2, 0.6, 0.2, 0.6, 1.0, 0.6, 1.0, 1.0]))
                values.extend(sorted([-1.0, -1.0, -0.6, -1.0, -0.6, -0.2, -0.6, -0.2, 0, -0.2, 0, 0.2, 0, 0.2, 0.6, 0.2, 0.6, 1.0, 0.6, 1.0, 1.0]))
                values.extend(sorted([-1, -1, 0.0, 0.0, 1, 1]))

                solution = values

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
        ) = targeting_control(solution)
            
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
            # thrustRule49, 
            # thrustRule50, 
            # thrustRule51, 
            # thrustRule52, 
            # thrustRule53, 
            # thrustRule54, 
            # thrustRule55, 
            # thrustRule56, 
            # thrustRule57, 
            # thrustRule58, 
            # thrustRule59, 
            # thrustRule60, 
            # thrustRule61, 
            # thrustRule62, 
            # thrustRule63, 
            # thrustRule64, 
        ) = thrust_control(solution)

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
        # self.thrust_control.addrule(thrustRule49)
        # self.thrust_control.addrule(thrustRule50)
        # self.thrust_control.addrule(thrustRule51)
        # self.thrust_control.addrule(thrustRule52)
        # self.thrust_control.addrule(thrustRule53)
        # self.thrust_control.addrule(thrustRule54)
        # self.thrust_control.addrule(thrustRule55)
        # self.thrust_control.addrule(thrustRule56)
        # self.thrust_control.addrule(thrustRule57)
        # self.thrust_control.addrule(thrustRule58)
        # self.thrust_control.addrule(thrustRule59)
        # self.thrust_control.addrule(thrustRule60)
        # self.thrust_control.addrule(thrustRule61)
        # self.thrust_control.addrule(thrustRule62)
        # self.thrust_control.addrule(thrustRule63)
        # self.thrust_control.addrule(thrustRule64)


        (
            mineRule1,
            mineRule2,
            mineRule3,
            mineRule4,
            mineRule5,
            mineRule6,
            mineRule7,
            mineRule8,
            mineRule9,
            mineRule10,
            mineRule11,
            mineRule12,
            mineRule13,
            mineRule14,
        ) = mine_control(solution)
        self.mine_control = ctrl.ControlSystem()
        self.mine_control.addrule(mineRule1)
        self.mine_control.addrule(mineRule2)
        self.mine_control.addrule(mineRule3)
        self.mine_control.addrule(mineRule4)
        self.mine_control.addrule(mineRule5)
        self.mine_control.addrule(mineRule6)
        self.mine_control.addrule(mineRule7)
        self.mine_control.addrule(mineRule8)
        self.mine_control.addrule(mineRule9)
        self.mine_control.addrule(mineRule10)
        self.mine_control.addrule(mineRule11)
        self.mine_control.addrule(mineRule12)
        self.mine_control.addrule(mineRule13)
        self.mine_control.addrule(mineRule14)
        
        

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

        # get velocity of closest asteroid

        # if it hasn't already been calculated, calculate normalization distance by using map size diagonal/2
        if not self.normalization_dist:
            self.normalization_dist = np.sqrt(game_state["map_size"][0]**2 + game_state["map_size"][1]**2)/2

        # normalize distance
        norm_asteroid_displ_x = asteroid_displ_x/(game_state["map_size"][0] / 2)
        norm_asteroid_displ_y = asteroid_displ_y/(game_state["map_size"][1] / 2)
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
        # thrusting.input['ship_disp_x'] = rel_disp_x
        # thrusting.input['ship_disp_y'] = rel_disp_y
        thrusting.input['ship_heading'] = (ship_state["heading"] * (math.pi / 360)) - (math.pi / 2)

        thrusting.compute()

        thrust = thrusting.output["ship_thrust"]

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
        
        return thrust, turn_rate, fire, drop_mine

    @property
    def name(self) -> str:
        return "Group 3 Controller"