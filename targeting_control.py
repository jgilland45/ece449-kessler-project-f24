from skfuzzy import control as ctrl
import math
import numpy as np
import skfuzzy as fuzz

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
    rule1 = ctrl.Rule(bullet_time['L'] & theta_delta['NL'], (ship_turn['NL'], ship_fire['N']))
    rule2 = ctrl.Rule(bullet_time['L'] & theta_delta['NM'], (ship_turn['NM'], ship_fire['N']))
    rule3 = ctrl.Rule(bullet_time['L'] & theta_delta['NS'], (ship_turn['NS'], ship_fire['Y']))
    # rule4 = ctrl.Rule(bullet_time['L'] & theta_delta['Z'], (ship_turn['Z'], ship_fire['Y']))
    rule5 = ctrl.Rule(bullet_time['L'] & theta_delta['PS'], (ship_turn['PS'], ship_fire['Y']))
    rule6 = ctrl.Rule(bullet_time['L'] & theta_delta['PM'], (ship_turn['PM'], ship_fire['N']))
    rule7 = ctrl.Rule(bullet_time['L'] & theta_delta['PL'], (ship_turn['PL'], ship_fire['N']))
    rule8 = ctrl.Rule(bullet_time['M'] & theta_delta['NL'], (ship_turn['NL'], ship_fire['N']))
    rule9 = ctrl.Rule(bullet_time['M'] & theta_delta['NM'], (ship_turn['NM'], ship_fire['N']))
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