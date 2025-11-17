import random
from src.population import Population
from src.visualizer import visualize_solution, print_board

def main():
    """
    Main function to run the genetic algorithm
    """
    # Set random seed for reproducibility (optional, remove for true randomness)
    # random.seed(42)
    
    # Parameters
    population_size = 50
    max_generations = 1000  # Safety limit
    
    print("=" * 60)
    print("Knight's Tour - Genetic Algorithm")
    print("=" * 60)
    print(f"Population size: {population_size}")
    print(f"Target: Visit all 64 squares")
    print("=" * 60)
    print()
    
    # Create initial population
    population = Population(population_size)
    
    # Main evolution loop
    while True:
        # Validate all knight moves
        population.check_population()
        
        # Evaluate fitness of all knights
        max_fitness, best_solution = population.evaluate()
        
        # Get statistics
        stats = population.get_statistics()
        
        # Print progress
        print(f"Generation {population.generation:4d} | "
              f"Best: {max_fitness:2d}/64 | "
              f"Avg: {stats['avg']:5.2f} | "
              f"Min: {stats['min']:2d}")
        
        # Check if solution found
        if max_fitness == 64:
            print()
            print("=" * 60)
            print("🎉 SOLUTION FOUND! 🎉")
            print("=" * 60)
            print(f"Generation: {population.generation}")
            print(f"Fitness: {max_fitness}/64")
            print(f"Path length: {len(best_solution.path)}")
            print()
            print("First 10 moves:", best_solution.path[:10])
            print("Last 10 moves:", best_solution.path[-10:])
            print()
            print("Chromosome (first 20 genes):", best_solution.chromosome.genes[:20])
            print("=" * 60)
            print()
            
            
            # Show graphical board
            print("Displaying visualization...")
            visualize_solution(best_solution)
            break
        
        # Safety check - stop if taking too long
        if population.generation >= max_generations:
            print()
            print("=" * 60)
            print(f"⚠️ Reached maximum generations ({max_generations})")
            print(f"Best fitness achieved: {max_fitness}/64")
            print("=" * 60)
            print()
            
            # Show best solution found so far
            print("Best solution found:")
            print_board(best_solution)
            print()
            visualize_solution(best_solution)
            break
        
        # Create next generation
        population.create_new_generation()

if __name__ == "__main__":
    main()