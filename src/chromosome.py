import random

class Chromosome:
    """
    Represents a sequence of 63 knight moves (genes)
    Each gene is a number from 1-8 representing a direction
    """
    
    def __init__(self, genes=None):
        """
        Initialize chromosome with genes
        
        Args:
            genes: List of 63 moves (1-8). If None, generates random genes
        """
        if genes is not None:
            self.genes = genes[:]  # Copy the list
        else:
            # Generate 63 random moves (1-8)
            self.genes = [random.randint(1, 8) for _ in range(63)]
    
    def crossover(self, partner):
        """
        Perform single-point crossover with another chromosome
        
        Args:
            partner: Another Chromosome object
            
        Returns:
            Tuple of two new Chromosome objects (children)
        """
        # Choose random crossover point (not at start or end)
        crossover_point = random.randint(1, 62)
        
        # Create two children by swapping genes at crossover point
        child1_genes = self.genes[:crossover_point] + partner.genes[crossover_point:]
        child2_genes = partner.genes[:crossover_point] + self.genes[crossover_point:]
        
        # Return two new chromosomes
        return Chromosome(child1_genes), Chromosome(child2_genes)
    
    def mutation(self, rate=0.01):
        """
        Apply mutation to genes
        Each gene has 'rate' probability to mutate to random value
        
        Args:
            rate: Probability of mutation for each gene (default 1%)
        """
        for i in range(len(self.genes)):
            # Check if this gene should mutate
            if random.random() < rate:
                # Change to random move (1-8)
                self.genes[i] = random.randint(1, 8)
    
    def __str__(self):
        """String representation for debugging"""
        return f"Chromosome(genes={self.genes[:10]}...)"  # Show first 10 genes
    
    def __repr__(self):
        return self.__str__()