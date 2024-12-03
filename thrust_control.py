from skfuzzy import control as ctrl
import math
import numpy as np
import skfuzzy as fuzz

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