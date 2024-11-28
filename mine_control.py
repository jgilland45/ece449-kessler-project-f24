from skfuzzy import control as ctrl
import numpy as np
import skfuzzy as fuzz

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
    ]