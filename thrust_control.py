from skfuzzy import control as ctrl
import numpy as np
import skfuzzy as fuzz

def thrust_control():
    # self.targeting_control is the targeting rulebase, which is static in this controller.      
    # Declare variables
    # TODO: add current velocity as antecedant
    asteroid_disp_x = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'asteroid_disp_x') # 0-1 to avoid absolute distances
    asteroid_disp_y = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'asteroid_disp_y') # 0-1 to avoid absolute distances
    ship_velo_x = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_velo_x')
    ship_velo_y = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'ship_velo_y')
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
    
    # Declare fuzzy sets for the ship_thrust consequent
    ship_thrust['NL'] = fuzz.trimf(ship_thrust.universe, [-480.0, -480.0, -470.0])
    ship_thrust['NM'] = fuzz.trimf(ship_thrust.universe, [-480.0, -470.0, -460.0])
    ship_thrust['NS'] = fuzz.trimf(ship_thrust.universe, [-470.0, -460.0, 0])
    ship_thrust['Z'] = fuzz.trimf(ship_thrust.universe, [-460.0, 0, 460.0])
    ship_thrust['PS'] = fuzz.trimf(ship_thrust.universe, [0, 460.0, 470.0])
    ship_thrust['PM'] = fuzz.trimf(ship_thrust.universe, [460.0, 470.0, 480.0])
    ship_thrust['PL'] = fuzz.trimf(ship_thrust.universe, [470.0, 480.0, 480.0])
    
    rule1 = ctrl.Rule((asteroid_disp_x['NL'] | asteroid_disp_x['NM'] | asteroid_disp_x['NS']) & ship_velo_x['NL'], ship_thrust['NL'])
    rule2 = ctrl.Rule((asteroid_disp_y['NL'] | asteroid_disp_y['NM'] | asteroid_disp_y['NS']) & ship_velo_y['NL'], ship_thrust['NL'])
    rule3 = ctrl.Rule((asteroid_disp_x['NL'] | asteroid_disp_x['NM'] | asteroid_disp_x['NS']) & ship_velo_x['NM'], ship_thrust['NM'])
    rule4 = ctrl.Rule((asteroid_disp_y['NL'] | asteroid_disp_y['NM'] | asteroid_disp_y['NS']) & ship_velo_y['NM'], ship_thrust['NM'])
    rule5 = ctrl.Rule((asteroid_disp_x['NL'] | asteroid_disp_x['NM'] | asteroid_disp_x['NS']) & ship_velo_x['NS'], ship_thrust['NS'])
    rule6 = ctrl.Rule((asteroid_disp_y['NL'] | asteroid_disp_y['NM'] | asteroid_disp_y['NS']) & ship_velo_y['NS'], ship_thrust['NS'])
    rule7 = ctrl.Rule((asteroid_disp_x['NL'] | asteroid_disp_x['NM'] | asteroid_disp_x['NS']) & ship_velo_x['Z'], ship_thrust['PS'])
    rule8 = ctrl.Rule((asteroid_disp_y['NL'] | asteroid_disp_y['NM'] | asteroid_disp_y['NS']) & ship_velo_y['Z'], ship_thrust['PS'])
    rule9 = ctrl.Rule((asteroid_disp_x['NL'] | asteroid_disp_x['NM'] | asteroid_disp_x['NS']) & ship_velo_x['PS'], ship_thrust['Z'])
    rule10 = ctrl.Rule((asteroid_disp_y['NL'] | asteroid_disp_y['NM'] | asteroid_disp_y['NS']) & ship_velo_y['PS'], ship_thrust['Z'])
    rule11 = ctrl.Rule((asteroid_disp_x['NL'] | asteroid_disp_x['NM'] | asteroid_disp_x['NS']) & ship_velo_x['PM'], ship_thrust['Z'])
    rule12 = ctrl.Rule((asteroid_disp_y['NL'] | asteroid_disp_y['NM'] | asteroid_disp_y['NS']) & ship_velo_y['PM'], ship_thrust['Z'])
    rule13 = ctrl.Rule((asteroid_disp_x['NL'] | asteroid_disp_x['NM'] | asteroid_disp_x['NS']) & ship_velo_x['PL'], ship_thrust['Z'])
    rule14 = ctrl.Rule((asteroid_disp_y['NL'] | asteroid_disp_y['NM'] | asteroid_disp_y['NS']) & ship_velo_y['PL'], ship_thrust['Z'])
    rule15 = ctrl.Rule(asteroid_disp_x['Z'] & ship_velo_x['NL'], ship_thrust['NL'])
    rule16 = ctrl.Rule(asteroid_disp_x['Z'] & ship_velo_x['NM'], ship_thrust['NM'])
    rule17 = ctrl.Rule(asteroid_disp_x['Z'] & ship_velo_x['NS'], ship_thrust['NS'])
    rule18 = ctrl.Rule(asteroid_disp_x['Z'] & ship_velo_x['Z'] , ship_thrust['NL'])
    rule19 = ctrl.Rule(asteroid_disp_x['Z'] & ship_velo_x['PS'], ship_thrust['PS'])
    rule20 = ctrl.Rule(asteroid_disp_x['Z'] & ship_velo_x['PM'], ship_thrust['PM'])
    rule21 = ctrl.Rule(asteroid_disp_x['Z'] & ship_velo_x['PL'], ship_thrust['PL'])
    rule22 = ctrl.Rule(asteroid_disp_y['Z'] & ship_velo_y['NL'], ship_thrust['NL'])
    rule23 = ctrl.Rule(asteroid_disp_y['Z'] & ship_velo_y['NM'], ship_thrust['NM'])
    rule24 = ctrl.Rule(asteroid_disp_y['Z'] & ship_velo_y['NS'], ship_thrust['NS'])
    rule25 = ctrl.Rule(asteroid_disp_y['Z'] & ship_velo_y['Z'] , ship_thrust['NL'])
    rule26 = ctrl.Rule(asteroid_disp_y['Z'] & ship_velo_y['PS'], ship_thrust['PS'])
    rule27 = ctrl.Rule(asteroid_disp_y['Z'] & ship_velo_y['PM'], ship_thrust['PM'])
    rule28 = ctrl.Rule(asteroid_disp_y['Z'] & ship_velo_y['PL'], ship_thrust['PL'])
    rule29 = ctrl.Rule((asteroid_disp_x['PL'] | asteroid_disp_x['PM'] | asteroid_disp_x['PS']) & ship_velo_x['NL'], ship_thrust['Z'])
    rule30 = ctrl.Rule((asteroid_disp_y['PL'] | asteroid_disp_y['PM'] | asteroid_disp_y['PS']) & ship_velo_y['NL'], ship_thrust['Z'])
    rule31 = ctrl.Rule((asteroid_disp_x['PL'] | asteroid_disp_x['PM'] | asteroid_disp_x['PS']) & ship_velo_x['NM'], ship_thrust['Z'])
    rule32 = ctrl.Rule((asteroid_disp_y['PL'] | asteroid_disp_y['PM'] | asteroid_disp_y['PS']) & ship_velo_y['NM'], ship_thrust['Z'])
    rule33 = ctrl.Rule((asteroid_disp_x['PL'] | asteroid_disp_x['PM'] | asteroid_disp_x['PS']) & ship_velo_x['NS'], ship_thrust['Z'])
    rule34 = ctrl.Rule((asteroid_disp_y['PL'] | asteroid_disp_y['PM'] | asteroid_disp_y['PS']) & ship_velo_y['NS'], ship_thrust['Z'])
    rule35 = ctrl.Rule((asteroid_disp_x['PL'] | asteroid_disp_x['PM'] | asteroid_disp_x['PS']) & ship_velo_x['Z'], ship_thrust['NS'])
    rule36 = ctrl.Rule((asteroid_disp_y['PL'] | asteroid_disp_y['PM'] | asteroid_disp_y['PS']) & ship_velo_y['Z'], ship_thrust['NS'])
    rule37 = ctrl.Rule((asteroid_disp_x['PL'] | asteroid_disp_x['PM'] | asteroid_disp_x['PS']) & ship_velo_x['PS'], ship_thrust['PS'])
    rule38 = ctrl.Rule((asteroid_disp_y['PL'] | asteroid_disp_y['PM'] | asteroid_disp_y['PS']) & ship_velo_y['PS'], ship_thrust['PS'])
    rule39 = ctrl.Rule((asteroid_disp_x['PL'] | asteroid_disp_x['PM'] | asteroid_disp_x['PS']) & ship_velo_x['PM'], ship_thrust['PM'])
    rule40 = ctrl.Rule((asteroid_disp_y['PL'] | asteroid_disp_y['PM'] | asteroid_disp_y['PS']) & ship_velo_y['PM'], ship_thrust['PM'])
    rule41 = ctrl.Rule((asteroid_disp_x['PL'] | asteroid_disp_x['PM'] | asteroid_disp_x['PS']) & ship_velo_x['PL'], ship_thrust['PL'])
    rule42 = ctrl.Rule((asteroid_disp_y['PL'] | asteroid_disp_y['PM'] | asteroid_disp_y['PS']) & ship_velo_y['PL'], ship_thrust['PL'])
     
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
        rule42
        ]