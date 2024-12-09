
import pygad
import os.path
from kesslergame import Scenario, KesslerGame, GraphicsType, TrainerEnvironment
from project_controller import ProjectController
import math
import random
import pickle

def fitness(ga_instance, solution, solution_idx):
    # print(f"Getting fitness value!")
    my_test_scenario = Scenario(name='Test Scenario',
                            num_asteroids=10,
                            ship_states=[
                                {'position': (400, 400), 'angle': 90, 'lives': 3, 'team': 1, "mines_remaining": 3},
                                # {'position': (400, 600), 'angle': 90, 'lives': 3, 'team': 2, "mines_remaining": 3},
                            ],
                            map_size=(1000, 800),
                            time_limit=60,
                            ammo_limit_multiplier=0,
                            stop_if_no_ammo=False)
    game_settings = {'perf_tracker': True,
                     'graphics_type': GraphicsType.NoGraphics,
                     'realtime_multiplier': 1,
                     'graphics_obj': None,
                     'frequency': 30}
    game = KesslerGame(settings=game_settings)  # Use this to visualize the game scenario
    score, perf_data = game.run(scenario=my_test_scenario, controllers=[ProjectController(solution)])
    # print(f"Calc score: {score.teams[0].asteroids_hit}")
    return score.teams[0].asteroids_hit
    # return 4

def mutation(offspring, ga_instance):

  for chromosome_idx in range(offspring.shape[0]):
    # print(f"Mutating chromosome {chromosome_idx}")
    mutated_genes = []
    # since chromosome is so large, want to mutate more genes at once
    for _ in range(10):
        random_gene_idx = random.randint(0, offspring.shape[1] - 1)
        did_mutate = False
        while not did_mutate:
            if random_gene_idx in mutated_genes:
               random_gene_idx = random.randint(0, offspring.shape[1] - 1)
               continue
            if offspring[chromosome_idx, random_gene_idx] == -1.0:
               random_gene_idx = random.randint(0, offspring.shape[1] - 1)
               continue
            if offspring[chromosome_idx, random_gene_idx] == 1.0:
               random_gene_idx = random.randint(0, offspring.shape[1] - 1)
               continue
            # print(f"old value (chrom {chromosome_idx}, gene {random_gene_idx}): {offspring[chromosome_idx, random_gene_idx]}")
            offspring[chromosome_idx, random_gene_idx] = random.uniform(offspring[chromosome_idx, random_gene_idx - 1], offspring[chromosome_idx, random_gene_idx + 1])
            # print(f"new value (chrom {chromosome_idx}, gene {random_gene_idx}): {offspring[chromosome_idx, random_gene_idx]}")
            did_mutate = True
            mutated_genes.append(random_gene_idx)

    return offspring

def on_generation(ga_instance):
    global last_fitness
    print(f"Generation = {ga_instance.generations_completed}")
    print(f"Fitness    = {ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]}")
    print(f"Change     = {ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1] - last_fitness}")
    last_fitness = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]
    print(ga_instance.population)

def init_pop():
    # print(f"creating initial population!")
    global sol_per_pop
    global file_name
    population = []
    for _ in range(sol_per_pop):
        values = []
        try:
            sol_file = open(file_name, 'rb')
            best_sol_data = pickle.load(sol_file)
            values = best_sol_data['parameters']
            # print(f"{values}")
            sol_file.close()
            print("Got data from file")
        
        except:
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
            print("Got data from set values")

        

        population.append(values)
    return population



file_name = 'ga_instance'
# num_generations = 5
num_generations = 10
# num_parents_mating = 2
num_parents_mating = 4
# sol_per_pop = 5
sol_per_pop = 8
num_genes = 238 # number of fuzzy membership function variables
last_fitness = 0
population = init_pop()

ga = pygad.GA(
    num_generations=num_generations,
    num_parents_mating=num_parents_mating,
    sol_per_pop=sol_per_pop,
    num_genes=num_genes,
    fitness_func=fitness,
    on_generation=on_generation,
    initial_population=population,
    mutation_type=mutation,
    parallel_processing=["process", 8],
)
ga.run()
ga.plot_fitness()

solution, solution_fitness, solution_idx = ga.best_solution(ga.last_generation_fitness)
print(f"Parameters of the best solution : {solution}")
print(f"Fitness value of the best solution = {solution_fitness}")
print(f"Index of the best solution : {solution_idx}")

best_sol_data = { 'fitness': solution_fitness, 'parameters': solution.tolist() }

try:
    sol_file = open(file_name, 'rb')
    best_sol_data_from_file = pickle.load(sol_file)
    best_fitness = best_sol_data_from_file['fitness']
    values = best_sol_data_from_file['parameters']
    sol_file.close()
    if best_fitness < solution_fitness:
        sol_file = open(file_name, 'wb')
        pickle.dump(best_sol_data, sol_file)
        sol_file.close()
except:
    try:
        sol_file = open(file_name, 'wb')
        pickle.dump(best_sol_data, sol_file)
        sol_file.close()
    except:
        print("cannot open pickle file - don't save!")

# init_pop()