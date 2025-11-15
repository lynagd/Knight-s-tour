import random
from .chromosome import Chromosome

class Knight:
    """
    Represents a knight on the chessboard with its movement sequence
    """
    
    # Define the 8 possible L-shaped knight moves
    # Direction: (row_change, col_change)
    MOVES = {
        1: (-1, 2),   # up-right
        2: (-2, 1),   # right-up
        3: (-2, -1),  # right-down
        4: (-1, -2),  # down-right
        5: (1, -2),   # down-left
        6: (2, -1),   # left-down
        7: (2, 1),    # left-up
        8: (1, 2)     # up-left
    }
    
    def __init__(self, chromosome=None):
        """
        Initialize a knight
        
        Args:
            chromosome: Chromosome object with move sequence. 
                       If None, creates random chromosome
        """
        # Create or assign chromosome
        self.chromosome = chromosome if chromosome else Chromosome()
        
        # Starting position (top-left corner)
        self.position = (0, 0)
        
        # Path of visited positions
        self.path = [(0, 0)]
        
        # Fitness score (how many squares visited)
        self.fitness = 0
    
    def move_forward(self, direction):
        """
        Calculate new position after moving in given direction
        
        Args:
            direction: Move direction (1-8)
            
        Returns:
            Tuple (new_row, new_col)
        """
        if direction not in self.MOVES:
            raise ValueError(f"Invalid direction: {direction}")
        
        dr, dc = self.MOVES[direction]
        new_row = self.position[0] + dr
        new_col = self.position[1] + dc
        
        return (new_row, new_col)
    
    def move_backward(self, direction):
        """
        Undo a move (go back one step)
        
        Args:
            direction: The direction that was taken
        """
        dr, dc = self.MOVES[direction]
        self.position = (self.position[0] - dr, self.position[1] - dc)
        self.path.pop()  # Remove last position from path
    
    def is_valid_position(self, pos):
        """
        Check if position is valid (inside board and not visited)
        
        Args:
            pos: Tuple (row, col)
            
        Returns:
            True if valid, False otherwise
        """
        row, col = pos
        
        # Check if inside 8x8 board
        if row < 0 or row >= 8 or col < 0 or col >= 8:
            return False
        
        # Check if not already visited
        if pos in self.path:
            return False
        
        return True
    
    def check_moves(self):
        """
        Validate and correct the chromosome's move sequence
        Goes through all 63 moves and corrects invalid ones
        """
        # Reset to starting position
        self.position = (0, 0)
        self.path = [(0, 0)]
        
        # Go through all 63 genes
        for i in range(63):
            current_move = self.chromosome.genes[i]
            
            # Try the current move
            new_pos = self.move_forward(current_move)
            
            # If valid, make the move and continue
            if self.is_valid_position(new_pos):
                self.position = new_pos
                self.path.append(new_pos)
                continue
            
            # If invalid, try to find a valid alternative
            # Randomly choose cycle direction (forward or backward)
            cycle_forward = random.choice([True, False])
            
            found_valid = False
            
            # Try all 8 possible moves
            for attempt in range(8):
                # Cycle through moves
                if cycle_forward:
                    test_move = (current_move % 8) + 1
                else:
                    test_move = ((current_move - 2) % 8) + 1
                
                current_move = test_move
                
                # Try this move
                new_pos = self.move_forward(test_move)
                
                if self.is_valid_position(new_pos):
                    # Found valid move!
                    self.position = new_pos
                    self.path.append(new_pos)
                    self.chromosome.genes[i] = test_move  # Update gene
                    found_valid = True
                    break
            
            # If no valid move found, stop here
            if not found_valid:
                break
    
    def evaluate_fitness(self):
        """
        Calculate fitness score (number of unique squares visited)
        
        Returns:
            Fitness value (1-64)
        """
        self.fitness = len(self.path)
        return self.fitness
    
    def __str__(self):
        """String representation for debugging"""
        return f"Knight(fitness={self.fitness}, path_length={len(self.path)})"
    
    def __repr__(self):
        return self.__str__()