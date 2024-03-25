import pygad
import copy

class FlowOptimizer:
    def __init__(self, packets, model_name, flow_id, max_fitness):
        self.packets = packets
        self.model_name = model_name
        self.flow_id = flow_id
        self.ga_instance = None
        self.max_fitness = max_fitness
        
    def apply_best_solution(self):
        best_solution, best_solution_fitness, _ = self.ga_instance.best_solution()
        best_operations = self.decode_operations(best_solution)
        self.best_modified_packets = self.apply_operations_to_packets(best_operations, self.packets, self.flow_id)
        return self.best_modified_packets, best_solution_fitness

    def on_generation(self, ga_instance):
        print(f"Flow ID: {self.flow_id}, Generation: {ga_instance.generations_completed}")
        message = f"Best score: {ga_instance.best_solution()[1]}"
        print(message)
            
    def on_fitness(self, ga_instance):
        ga_instance.plot_fitness()

    def fitness_function(self, ga_instance, solution, solution_idx):
        fitnesses = []
        operations = self.decode_operations(solution)
        
        modified_packets = self.packets
        sizing_stats = prepare_size_stats(modified_packets, self.flow_id)
        timing_stats = prepare_timing_stats(modified_packets, self.flow_id)
        fitnesses.append(1.0 - predict_single_flow(self.model_name, sizing_stats, timing_stats))
        
        for operation in operations:
            modified_packets = self.apply_operations_to_packets(operation, operation['op_type'])
            sizing_stats = prepare_size_stats(modified_packets, self.flow_id)
            timing_stats = prepare_timing_stats(modified_packets, self.flow_id)
            fitnesses.append(1.0 - predict_single_flow(self.model_name, sizing_stats, timing_stats))
        
        max_fitness_value = max(fitnesses)
        if max_fitness_value > self.max_fitness[0]:
            self.max_fitness = [max_fitness_value, operations, fitnesses.index(max_fitness_value)]
        
        return max_fitness_value

    def optimize_for_flow(self):
        ga_instance = pygad.GA(num_generations=8,
                               num_parents_mating=2,
                               fitness_func=self.fitness_function,
                               sol_per_pop=3,                          
                               mutation_probability=0.6,
                               on_generation=self.on_generation,
                               num_genes=6,
                               gene_space=[{'low': 1.1, 'high': 5.0},
                                           {'low': 0.25, 'high': 5.0},
                                           {'low': 1.1, 'high': 3.0},
                                           {'low': 0.4, 'high': 2.4},
                                           [0,1,2],
                                           [0,1,2]])
        
        ga_instance.run()
        return ga_instance, self.max_fitness

    def decode_operations(self, genotype):
        focus_point_map = {0: "start", 1: "middle", 2: "end"}
        focus_point = focus_point_map[genotype[5]]

        operations = [
            {'scaling_factor': genotype[0], 'direction': genotype[4], 'focus_point': focus_point, 'op_type': 'size_norm'},
            {'scaling_factor': genotype[1], 'direction': genotype[4], 'focus_point': focus_point, 'op_type': 'size_uni'},
            {'scaling_factor': genotype[2], 'direction': genotype[4], 'focus_point': focus_point, 'op_type': 'time_norm'},
            {'scaling_factor': genotype[3], 'direction': genotype[4], 'focus_point': focus_point, 'op_type': 'time_uni'}
        ]
        return operations 

    def apply_operations_to_packets(self, operation, op_type):
        scaling_factor = operation['scaling_factor']
        direction = operation['direction']
        focus_point = operation['focus_point']
        
        if op_type == 'size_norm':
            packets = adjust_packet_size_deepcopy(self.packets, self.flow_id, direction, 'normal', scaling_factor, focus_point)
        elif op_type == 'size_uni':
            packets = adjust_packet_size_deepcopy(self.packets, self.flow_id, direction, 'uniform', scaling_factor, focus_point)
        elif op_type == 'time_norm':
            packets = apply_time_perturbation_with_focus_deepcopy(self.packets, self.flow_id, 'normal', focus_point, scaling_factor)
        elif op_type == 'time_uni':
            packets = apply_time_perturbation_with_focus_deepcopy(self.packets, self.flow_id, 'uniform', focus_point, scaling_factor)
        
        return packets



def apply_best_on_packets(packets, best_solution, flow_id):
    """
    Apply the best operations on the packets based on the best solution found for a given flow_id.
    This function needs to be implemented based on your packet structure and how operations affect them.
    """
    
    operations = best_solution[1][1]  # Assuming best_solution format is [fitness, [operations], index]
    for operation in operations:
        if operation['op_type'] == 'size_norm':
            packets = adjust_packet_size(packets, flow_id, operation['direction'], 'normal', operation['scaling_factor'], operation['focus_point'])
        elif operation['op_type'] == 'size_uni':
            packets = adjust_packet_size(packets, flow_id, operation['direction'], 'uniform', operation['scaling_factor'], operation['focus_point'])
        elif operation['op_type'] == 'time_norm':
            packets = apply_time_perturbation_with_focus(packets, flow_id, 'normal', operation['focus_point'], operation['scaling_factor'])
        elif operation['op_type'] == 'time_uni':
            packets = apply_time_perturbation_with_focus(packets, flow_id, 'uniform', operation['focus_point'], operation['scaling_factor'])
    return packets
