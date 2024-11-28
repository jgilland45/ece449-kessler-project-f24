from pickle import FALSE

from kesslergame import KesslerController
from typing import Dict, Tuple
from cmath import sqrt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import math
import numpy as np
import matplotlib as plt

from targeting_control import targeting_control
from thrust_control import thrust_control
from mine_control import mine_control

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
            targetControlRule21
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


        (
            mineRule1,
            mineRule2,
            mineRule3,
            mineRule4,
            mineRule5,
            mineRule6,
            mineRule7,
        ) = mine_control()
        self.mine_control = ctrl.ControlSystem()
        self.mine_control.addrule(mineRule1)
        self.mine_control.addrule(mineRule2)
        self.mine_control.addrule(mineRule3)
        self.mine_control.addrule(mineRule4)
        self.mine_control.addrule(mineRule5)
        self.mine_control.addrule(mineRule6)
        self.mine_control.addrule(mineRule7)
        
        

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
        # asteroid_dist = closest_asteroid["dist"]
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
        # norm_ast_distance = asteroid_dist/self.normalization_dist

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
        thrusting.input['asteroid_disp_x'] = norm_asteroid_displ_x
        thrusting.input['asteroid_disp_y'] = norm_asteroid_displ_y
        thrusting.input['asteroid_vel_x'] = norm_asteroid_velo_x
        thrusting.input['asteroid_vel_y'] = norm_asteroid_velo_y
        thrusting.input['ship_velo_x'] = rel_vel_x
        thrusting.input['ship_velo_y'] = rel_vel_y
        thrusting.input['ship_disp_x'] = rel_disp_x
        thrusting.input['ship_disp_y'] = rel_disp_y
        thrusting.input['ship_heading'] = ship_state["heading"]

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