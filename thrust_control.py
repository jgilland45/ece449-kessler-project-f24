from skfuzzy import control as ctrl
import numpy as np
import skfuzzy as fuzz

def thrust_control():   
    # Declare variables
    # TODO: add in ship facing direction to antecedants, as well as angle to nearest asteroid
    asteroid_disp_x = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'asteroid_disp_x') # -1 -> 1 to avoid absolutes
    asteroid_disp_y = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'asteroid_disp_y') # -1 -> 1 to avoid absolutes
    asteroid_vel_x = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'asteroid_vel_x') # -1 -> 1 to avoid absolutes
    asteroid_vel_y = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'asteroid_vel_y') # -1 -> 1 to avoid absolutes
    ship_velo_x = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_velo_x') # -1 -> 1 to avoid absolutes
    ship_velo_y = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_velo_y') # -1 -> 1 to avoid absolutes
    ship_disp_x = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_disp_x') # -1 -> 1 to avoid absolutes
    ship_disp_y = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_disp_y') # -1 -> 1 to avoid absolutes
    ship_heading = ctrl.Antecedent(np.arange(0.0, 360.0, 1.0), 'ship_heading')
    ship_thrust = ctrl.Consequent(np.arange(-480.0, 480.0, 1), 'ship_thrust') # from Kessler

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

    # Declare fuzzy sets for asteroid_vel_x (relative x-velocity of the asteroid compared to the ship)
    asteroid_vel_x['NL'] = fuzz.trimf(asteroid_vel_x.universe, [-1.0, -1.0, -0.6])
    asteroid_vel_x['NM'] = fuzz.trimf(asteroid_vel_x.universe, [-1.0, -0.6, -0.2])
    asteroid_vel_x['NS'] = fuzz.trimf(asteroid_vel_x.universe, [-0.6, -0.2, 0])
    asteroid_vel_x['Z'] = fuzz.trimf(asteroid_vel_x.universe, [-0.2, 0, 0.2])
    asteroid_vel_x['PS'] = fuzz.trimf(asteroid_vel_x.universe, [0, 0.2, 0.6])
    asteroid_vel_x['PM'] = fuzz.trimf(asteroid_vel_x.universe, [0.2, 0.6, 1.0])
    asteroid_vel_x['PL'] = fuzz.trimf(asteroid_vel_x.universe, [0.6, 1.0, 1.0])

    # Declare fuzzy sets for asteroid_vel_y (relative y-velocity of the asteroid compared to the ship)
    asteroid_vel_y['NL'] = fuzz.trimf(asteroid_vel_y.universe, [-1.0, -1.0, -0.6])
    asteroid_vel_y['NM'] = fuzz.trimf(asteroid_vel_y.universe, [-1.0, -0.6, -0.2])
    asteroid_vel_y['NS'] = fuzz.trimf(asteroid_vel_y.universe, [-0.6, -0.2, 0])
    asteroid_vel_y['Z'] = fuzz.trimf(asteroid_vel_y.universe, [-0.2, 0, 0.2])
    asteroid_vel_y['PS'] = fuzz.trimf(asteroid_vel_y.universe, [0, 0.2, 0.6])
    asteroid_vel_y['PM'] = fuzz.trimf(asteroid_vel_y.universe, [0.2, 0.6, 1.0])
    asteroid_vel_y['PL'] = fuzz.trimf(asteroid_vel_y.universe, [0.6, 1.0, 1.0])

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
    ship_heading['N'] = fuzz.trimf(ship_heading.universe, [0, 0, 135])
    ship_heading['S'] = fuzz.trimf(ship_heading.universe, [45, 135, 225])
    ship_heading['E'] = fuzz.trimf(ship_heading.universe, [135, 225, 315])
    ship_heading['W'] = fuzz.trimf(ship_heading.universe, [225, 360, 360])
    
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

    # far away, moving with it
    rule1 = ctrl.Rule((asteroid_vel_x['PL'] | asteroid_vel_x['PM'] | asteroid_vel_x['PS']) & (asteroid_disp_x['NL'] | asteroid_disp_x['NM'] | asteroid_disp_x['PM'] | asteroid_disp_x['PL']) & (ship_velo_x['PL'] | ship_velo_x['PM'] | ship_velo_x['PS']), ship_thrust['PS'])
    rule2 = ctrl.Rule((asteroid_vel_x['NL'] | asteroid_vel_x['NM'] | asteroid_vel_x['NS']) & (asteroid_disp_x['NL'] | asteroid_disp_x['NM'] | asteroid_disp_x['PM'] | asteroid_disp_x['PL']) & (ship_velo_x['NL'] | ship_velo_x['NM'] | ship_velo_x['NS']), ship_thrust['PS'])
    rule3 = ctrl.Rule((asteroid_vel_y['PL'] | asteroid_vel_y['PM'] | asteroid_vel_y['PS']) & (asteroid_disp_y['NL'] | asteroid_disp_y['NM'] | asteroid_disp_y['PM'] | asteroid_disp_y['PL']) & (ship_velo_y['PL'] | ship_velo_y['PM'] | ship_velo_y['PS']), ship_thrust['PS'])
    rule4 = ctrl.Rule((asteroid_vel_y['NL'] | asteroid_vel_y['NM'] | asteroid_vel_y['NS']) & (asteroid_disp_y['NL'] | asteroid_disp_y['NM'] | asteroid_disp_y['PM'] | asteroid_disp_y['PL']) & (ship_velo_y['NL'] | ship_velo_y['NM'] | ship_velo_y['NS']), ship_thrust['PS'])
    # far away, moving against it
    rule5 = ctrl.Rule((asteroid_vel_x['PL'] | asteroid_vel_x['PM'] | asteroid_vel_x['PS']) & (asteroid_disp_x['NL'] | asteroid_disp_x['NM'] | asteroid_disp_x['PM'] | asteroid_disp_x['PL']) & (ship_velo_x['NL'] | ship_velo_x['NM'] | ship_velo_x['NS']), ship_thrust['Z'])
    rule6 = ctrl.Rule((asteroid_vel_x['NL'] | asteroid_vel_x['NM'] | asteroid_vel_x['NS']) & (asteroid_disp_x['NL'] | asteroid_disp_x['NM'] | asteroid_disp_x['PM'] | asteroid_disp_x['PL']) & (ship_velo_x['PL'] | ship_velo_x['PM'] | ship_velo_x['PS']), ship_thrust['Z'])
    rule7 = ctrl.Rule((asteroid_vel_y['PL'] | asteroid_vel_y['PM'] | asteroid_vel_y['PS']) & (asteroid_disp_y['NL'] | asteroid_disp_y['NM'] | asteroid_disp_y['PM'] | asteroid_disp_y['PL']) & (ship_velo_y['NL'] | ship_velo_y['NM'] | ship_velo_y['NS']), ship_thrust['Z'])
    rule8 = ctrl.Rule((asteroid_vel_y['NL'] | asteroid_vel_y['NM'] | asteroid_vel_y['NS']) & (asteroid_disp_y['NL'] | asteroid_disp_y['NM'] | asteroid_disp_y['PM'] | asteroid_disp_y['PL']) & (ship_velo_y['PL'] | ship_velo_y['PM'] | ship_velo_y['PS']), ship_thrust['Z'])
    # close, moving with it
    rule9 = ctrl.Rule((asteroid_vel_x['PL'] | asteroid_vel_x['PM'] | asteroid_vel_x['PS']) & (asteroid_disp_x['NS'] | asteroid_disp_x['Z'] | asteroid_disp_x['PS'] | asteroid_disp_x['Z']) & (ship_velo_x['PL'] | ship_velo_x['PM'] | ship_velo_x['PS']), ship_thrust['NS'])
    rule10 = ctrl.Rule((asteroid_vel_x['NL'] | asteroid_vel_x['NM'] | asteroid_vel_x['NS']) & (asteroid_disp_x['NS'] | asteroid_disp_x['Z'] | asteroid_disp_x['PS'] | asteroid_disp_x['Z']) & (ship_velo_x['NL'] | ship_velo_x['NM'] | ship_velo_x['NS']), ship_thrust['NS'])
    rule11 = ctrl.Rule((asteroid_vel_y['PL'] | asteroid_vel_y['PM'] | asteroid_vel_y['PS']) & (asteroid_disp_y['NS'] | asteroid_disp_y['Z'] | asteroid_disp_y['PS'] | asteroid_disp_y['Z']) & (ship_velo_y['PL'] | ship_velo_y['PM'] | ship_velo_y['PS']), ship_thrust['NS'])
    rule12 = ctrl.Rule((asteroid_vel_y['NL'] | asteroid_vel_y['NM'] | asteroid_vel_y['NS']) & (asteroid_disp_y['NS'] | asteroid_disp_y['Z'] | asteroid_disp_y['PS'] | asteroid_disp_y['Z']) & (ship_velo_y['NL'] | ship_velo_y['NM'] | ship_velo_y['NS']), ship_thrust['NS'])
    # close, moving against it
    rule13 = ctrl.Rule((asteroid_vel_x['PL'] | asteroid_vel_x['PM'] | asteroid_vel_x['PS']) & (asteroid_disp_x['NS'] | asteroid_disp_x['Z'] | asteroid_disp_x['PS'] | asteroid_disp_x['Z']) & (ship_velo_x['NL'] | ship_velo_x['NM'] | ship_velo_x['NS']), ship_thrust['Z'])
    rule14 = ctrl.Rule((asteroid_vel_x['NL'] | asteroid_vel_x['NM'] | asteroid_vel_x['NS']) & (asteroid_disp_x['NS'] | asteroid_disp_x['Z'] | asteroid_disp_x['PS'] | asteroid_disp_x['Z']) & (ship_velo_x['PL'] | ship_velo_x['PM'] | ship_velo_x['PS']), ship_thrust['Z'])
    rule15 = ctrl.Rule((asteroid_vel_y['PL'] | asteroid_vel_y['PM'] | asteroid_vel_y['PS']) & (asteroid_disp_y['NS'] | asteroid_disp_y['Z'] | asteroid_disp_y['PS'] | asteroid_disp_y['Z']) & (ship_velo_y['NL'] | ship_velo_y['NM'] | ship_velo_y['NS']), ship_thrust['Z'])
    rule16 = ctrl.Rule((asteroid_vel_y['NL'] | asteroid_vel_y['NM'] | asteroid_vel_y['NS']) & (asteroid_disp_y['NS'] | asteroid_disp_y['Z'] | asteroid_disp_y['PS'] | asteroid_disp_y['Z']) & (ship_velo_y['PL'] | ship_velo_y['PM'] | ship_velo_y['PS']), ship_thrust['Z'])

    # close to left edge
    rule17 = ctrl.Rule(ship_disp_x['NL'] & (ship_velo_x['NL'] | ship_velo_x['NM'] | ship_velo_x['NS'] | ship_velo_x['Z']) & ship_heading['W'], ship_thrust['NL'])
    rule18 = ctrl.Rule(ship_disp_x['NL'] & (ship_velo_x['NL'] | ship_velo_x['NM'] | ship_velo_x['NS'] | ship_velo_x['Z']) & ship_heading['E'], ship_thrust['PL'])
    rule19 = ctrl.Rule(ship_disp_x['NL'] & (ship_velo_x['PL'] | ship_velo_x['PM'] | ship_velo_x['PS']) & ship_heading['W'], ship_thrust['NM'])
    rule20 = ctrl.Rule(ship_disp_x['NL'] & (ship_velo_x['PL'] | ship_velo_x['PM'] | ship_velo_x['PS']) & ship_heading['E'], ship_thrust['PM'])
    # close to right edge
    rule21 = ctrl.Rule(ship_disp_x['PL'] & (ship_velo_x['NL'] | ship_velo_x['NM'] | ship_velo_x['NS']) & ship_heading['W'], ship_thrust['NM'])
    rule22 = ctrl.Rule(ship_disp_x['PL'] & (ship_velo_x['NL'] | ship_velo_x['NM'] | ship_velo_x['NS']) & ship_heading['E'], ship_thrust['PM'])
    rule23 = ctrl.Rule(ship_disp_x['PL'] & (ship_velo_x['PL'] | ship_velo_x['PM'] | ship_velo_x['PS'] | ship_velo_x['Z']) & ship_heading['W'], ship_thrust['PL'])
    rule24 = ctrl.Rule(ship_disp_x['PL'] & (ship_velo_x['PL'] | ship_velo_x['PM'] | ship_velo_x['PS'] | ship_velo_x['Z']) & ship_heading['E'], ship_thrust['NL'])
    # close to bottom edge
    rule25 = ctrl.Rule(ship_disp_y['NL'] & (ship_velo_y['NL'] | ship_velo_y['NM'] | ship_velo_y['NS'] | ship_velo_y['Z']) & ship_heading['N'], ship_thrust['PL'])
    rule26 = ctrl.Rule(ship_disp_y['NL'] & (ship_velo_y['NL'] | ship_velo_y['NM'] | ship_velo_y['NS'] | ship_velo_y['Z']) & ship_heading['S'], ship_thrust['NL'])
    rule27 = ctrl.Rule(ship_disp_y['NL'] & (ship_velo_y['PL'] | ship_velo_y['PM'] | ship_velo_y['PS']) & ship_heading['N'], ship_thrust['NM'])
    rule28 = ctrl.Rule(ship_disp_y['NL'] & (ship_velo_y['PL'] | ship_velo_y['PM'] | ship_velo_y['PS']) & ship_heading['S'], ship_thrust['PM'])
    # close to top edge
    rule29 = ctrl.Rule(ship_disp_y['PL'] & (ship_velo_y['NL'] | ship_velo_y['NM'] | ship_velo_y['NS']) & ship_heading['N'], ship_thrust['NM'])
    rule30 = ctrl.Rule(ship_disp_y['PL'] & (ship_velo_y['NL'] | ship_velo_y['NM'] | ship_velo_y['NS']) & ship_heading['S'], ship_thrust['PM'])
    rule31 = ctrl.Rule(ship_disp_y['PL'] & (ship_velo_y['PL'] | ship_velo_y['PM'] | ship_velo_y['PS'] | ship_velo_y['Z']) & ship_heading['N'], ship_thrust['NL'])
    rule32 = ctrl.Rule(ship_disp_y['PL'] & (ship_velo_y['PL'] | ship_velo_y['PM'] | ship_velo_y['PS'] | ship_velo_y['Z']) & ship_heading['S'], ship_thrust['PL'])
     
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
        ]