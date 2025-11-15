import random
from .knight import Knight
from .chromosome import Chromosome

class Population:
    """
    Manages a population of knights and evolves them using genetic algorithm
    """
    
    def __init__(self, population_size):
        """
        Initialize population with random knights
        
        Args:
            population_size: Number of knights in population (e.g., 50)
        """
        self.population_size = population_size
        self.generation = 1
        
        # Create initial population of random knights
        self.knights = [Knight() for _ in range(population_size)]
        
        print(f"Created initial population of {population_size} knights")
    
    def check_population(self):
        """
        Validate moves for all knights in population
        """
        for knight in self.knights:
            knight.check_moves()
    
    def evaluate(self):
        """
        Evaluate fitness of all knights and find the best one
        
        Returns:
            Tuple (best_fitness, best_knight)
        """
        best_fitness = 0
        best_knight = None
        
        for knight in self.knights:
            fitness = knight.evaluate_fitness()
            
            if fitness > best_fitness:
                best_fitness = fitness
                best_knight = knight
        
        return best_fitness, best_knight
    
    def tournament_selection(self, size=3):
        """
        Select 2 parents using tournament selection
        
        Args:
            size: Number of knights to sample for tournament (default 3)
            
        Returns:
            Tuple of 2 Knight objects (parents)
        """
        # Randomly sample 'size' knights from population
        sample = random.sample(self.knights, size)
        
        # Sort by fitness (highest first)
        sample.sort(key=lambda k: k.fitness, reverse=True)
        
        # Return top 2 as parents
        return sample[0], sample[1]
    
    def create_new_generation(self):
        """
        Create new generation through selection, crossover, and mutation
        Replaces current population with new offspring
        """
        new_knights = []
        
        # Create population_size/2 pairs of children (total = population_size)
        for _ in range(self.population_size // 2):
            # Select 2 parents using tournament selection
            parent1, parent2 = self.tournament_selection()
            
            # Crossover: create 2 children
            child1_chromosome, child2_chromosome = parent1.chromosome.crossover(
                parent2.chromosome
            )
            
            # Mutation: mutate both children
            child1_chromosome.mutation()
            child2_chromosome.mutation()
            
            # Create new knights from children chromosomes
            new_knights.append(Knight(child1_chromosome))
            new_knights.append(Knight(child2_chromosome))
        
        # Replace old population with new generation
        self.knights = new_knights
        self.generation += 1
    
    def get_statistics(self):
        """
        Get statistics about current population
        
        Returns:
            Dictionary with min, max, average fitness
        """
        fitnesses = [k.fitness for k in self.knights]
        
        return {
            'min': min(fitnesses),
            'max': max(fitnesses),
            'avg': sum(fitnesses) / len(fitnesses)
        }
    
    def __str__(self):
        stats = self.get_statistics()
        return (f"Population(generation={self.generation}, "
                f"size={self.population_size}, "
                f"fitness: min={stats['min']}, max={stats['max']}, "
                f"avg={stats['avg']:.2f})")