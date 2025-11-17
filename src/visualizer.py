import pygame
import sys
import time
import math

class KnightTourVisualizer:
    """
    Beautiful animated visualizer for Knight's Tour solution
    """
    
    def __init__(self, knight):
        pygame.init()
    
        try:
            self.knight_image = pygame.image.load('src/knight.jpg')
        # Resize to fit the square nicely
            self.knight_image = pygame.transform.scale(self.knight_image, (42, 42))
            self.has_knight_image = True
        except:
            print("Warning: knight.jpg not found, using fallback")
            self.has_knight_image = False

    # Window settings - OPTIMIZED FOR YOUR SCREEN
        self.CELL_SIZE = 70  # Smaller cells to fit screen
        self.MARGIN = 20
        self.INFO_HEIGHT = 110  # Reduced height
        self.TITLE_HEIGHT = 50
        self.BOARD_SPACING = 15
    
    # Calculate window size
        self.BOARD_SIZE = 8
        self.WINDOW_WIDTH = self.BOARD_SIZE * self.CELL_SIZE + 2 * self.MARGIN
        self.WINDOW_HEIGHT = (self.BOARD_SIZE * self.CELL_SIZE + 
                             2 * self.MARGIN + 
                             self.INFO_HEIGHT + 
                             self.TITLE_HEIGHT + 
                             self.BOARD_SPACING)  # Removed extra spacing
    
    # Create window - MAKE IT RESIZABLE so you can adjust!
        self.screen = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT),
            pygame.RESIZABLE  # ← IMPORTANT! Now you can resize!
        )
        pygame.display.set_caption(" Knight's Tour Puzzle")
    
    # Beautiful color palette 🎨
        self.BACKGROUND = (25, 28, 48)
    
    # Unvisited squares (classic chess colors)
        self.LIGHT_SQUARE = (245, 240, 225)  
        self.DARK_SQUARE = (30, 50, 80)      
    
    # Visited squares (beautiful pastels)
        self.LIGHT_VISITED = (210, 200, 175)  
        self.DARK_VISITED = (50, 80, 120)     
    
    # Special squares
        self.CURRENT_SQUARE = (255, 215, 0)
        self.START_SQUARE = (255, 107, 107)
    
    # UI colors
        self.TITLE_GRADIENT_TOP = (40, 70, 100)      # Darker navy blue
        self.TITLE_GRADIENT_BOTTOM = (20, 40, 70)    # Deep ocean blue
        self.INFO_BG = (25, 45, 70)
        self.ACCENT_COLOR = (230, 200, 140)
        self.TEXT_COLOR = (250, 250, 255)
        self.TEXT_SHADOW = (15, 15, 25)
        self.PROGRESS_BAR = (40, 70, 100)
        self.GRID_COLOR = (100, 80, 60)
    
    # Fonts - smaller to fit
        self.font_title = pygame.font.Font(None, 42)
        self.font_info = pygame.font.Font(None, 22)
        self.font_number = pygame.font.Font(None, 28)
        self.font_instructions = pygame.font.Font(None, 18)
    
    # Knight data
        self.knight = knight
        self.current_step = 0
        self.visited_squares = {(0, 0)}
    
    # Animation
        self.animating = False
        self.animation_speed = 0.4
        self.last_update = time.time()
        self.banner_dismissed = False 
    # Visual effects
        self.glow_pulse = 0
        self.knight_bounce = 0
        
    def draw_gradient_rect(self, surface, color1, color2, rect):
        """Draw a smooth vertical gradient"""
        for i in range(rect.height):
            ratio = i / rect.height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(surface, (r, g, b), 
                           (rect.x, rect.y + i), 
                           (rect.x + rect.width, rect.y + i))
    
    def draw_text_with_shadow(self, text, font, color, x, y, shadow=True):
        """Draw text with shadow for depth"""
        if shadow:
            shadow_surf = font.render(text, True, self.TEXT_SHADOW)
            self.screen.blit(shadow_surf, (x + 2, y + 2))
        text_surf = font.render(text, True, color)
        self.screen.blit(text_surf, (x, y))
        return text_surf.get_rect(topleft=(x, y))
    
    def draw_title_bar(self):
        """Draw beautiful title bar with gradient"""
        title_rect = pygame.Rect(0, 0, self.WINDOW_WIDTH, self.TITLE_HEIGHT)
        self.draw_gradient_rect(self.screen, 
                               self.TITLE_GRADIENT_TOP, 
                               self.TITLE_GRADIENT_BOTTOM, 
                               title_rect)
        
        # Title text
        title_text = "  KNIGHT'S TOUR  "
        title_surface = self.font_title.render(title_text, True, self.TEXT_COLOR)
        title_x = (self.WINDOW_WIDTH - title_surface.get_width()) // 2
        self.draw_text_with_shadow(title_text, self.font_title, 
                                  self.TEXT_COLOR, title_x, 12)
    
    def draw_board(self):
        """Draw the beautiful chessboard"""
        board_x = self.MARGIN
        board_y = self.MARGIN + self.TITLE_HEIGHT + self.BOARD_SPACING
        
        # Board background with rounded corners
        board_rect = pygame.Rect(
            board_x - 5,
            board_y - 5,
            self.BOARD_SIZE * self.CELL_SIZE + 10,
            self.BOARD_SIZE * self.CELL_SIZE + 10
        )
        pygame.draw.rect(self.screen, (50, 40, 30), board_rect, border_radius=15)
        
        # Draw squares
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                # Determine colors
                is_light = (row + col) % 2 == 0
                pos = (row, col)
                
                # Choose color based on state
                if pos == self.knight.path[self.current_step]:
                    # Current position - GOLD!
                    color = self.CURRENT_SQUARE
                elif pos == (0, 0) and self.current_step == 0:
                    # Starting position
                    color = self.START_SQUARE
                elif pos in self.visited_squares:
                    # Visited - beautiful pastels
                    color = self.LIGHT_VISITED if is_light else self.DARK_VISITED
                else:
                    # Unvisited - classic chess colors
                    color = self.LIGHT_SQUARE if is_light else self.DARK_SQUARE
                
                # Draw square with slight rounded corners
                square_rect = pygame.Rect(
                    board_x + col * self.CELL_SIZE,
                    board_y + row * self.CELL_SIZE,
                    self.CELL_SIZE,
                    self.CELL_SIZE
                )
                pygame.draw.rect(self.screen, color, square_rect, border_radius=8)
                
                # Draw move number if visited
                if pos in self.visited_squares and pos != self.knight.path[self.current_step]:
                    try:
                        move_num = self.knight.path.index(pos) + 1
                        
                        # Circle background
                        center_x = square_rect.centerx
                        center_y = square_rect.centery
                        
                        # Determine text color based on square color 
                        is_light = (row + col) % 2 == 0

                        if is_light:
                            text_color = (30, 50, 80)
                        else:
                            text_color = (245, 240, 225)

                        # Draw number
                        num_text = self.font_number.render(str(move_num), True, text_color)
                        num_rect = num_text.get_rect(center=(center_x, center_y))
                        self.screen.blit(num_text, num_rect)
                    except ValueError:
                        pass
        
        # Grid lines (subtle)
        for i in range(self.BOARD_SIZE + 1):
            # Vertical lines
            x = board_x + i * self.CELL_SIZE
            pygame.draw.line(self.screen, self.GRID_COLOR, 
                           (x, board_y), 
                           (x, board_y + self.BOARD_SIZE * self.CELL_SIZE), 2)
            
            # Horizontal lines
            y = board_y + i * self.CELL_SIZE
            pygame.draw.line(self.screen, self.GRID_COLOR, 
                           (board_x, y), 
                           (board_x + self.BOARD_SIZE * self.CELL_SIZE, y), 2)
        
        # Outer frame
        pygame.draw.rect(self.screen, (80, 60, 40), board_rect, 4, border_radius=15)
    
    def draw_knight(self):
        """Draw the knight piece with bounce animation"""
        if self.current_step >= len(self.knight.path):
            return
    
        row, col = self.knight.path[self.current_step]
    
        board_x = self.MARGIN
        board_y = self.MARGIN + self.TITLE_HEIGHT + self.BOARD_SPACING
    
    # Calculate center of square
        center_x = board_x + col * self.CELL_SIZE + self.CELL_SIZE // 2
        center_y = board_y + row * self.CELL_SIZE + self.CELL_SIZE // 2
    
    # Bounce effect
        self.knight_bounce += 0.15
        bounce_offset = int(math.sin(self.knight_bounce) * 3)
    
    # Glow effect
        self.glow_pulse += 0.1
        glow_size = int(45 + math.sin(self.glow_pulse) * 5)
    
    # Draw glow
        for i in range(3):
            alpha_surface = pygame.Surface((glow_size + i * 10, glow_size + i * 10), 
                                      pygame.SRCALPHA)
            glow_color = (255, 215, 0, 60 - i * 15)
            pygame.draw.circle(alpha_surface, glow_color, 
                         (glow_size // 2 + i * 5, glow_size // 2 + i * 5), 
                         glow_size // 2 + i * 5)
            self.screen.blit(alpha_surface, 
                       (center_x - glow_size // 2 - i * 5, 
                        center_y - glow_size // 2 - i * 5 + bounce_offset))
    
    # Draw white background circle
        pygame.draw.circle(self.screen, (255, 255, 255), 
                     (center_x, center_y + bounce_offset), 32)
        pygame.draw.circle(self.screen, (139, 69, 19), 
                     (center_x, center_y + bounce_offset), 32, 3)
    
    # Draw knight image or fallback
        if self.has_knight_image:
        # Use the loaded image
            image_rect = self.knight_image.get_rect(center=(center_x, center_y + bounce_offset))
            self.screen.blit(self.knight_image, image_rect)
        else:
        # Fallback: Draw simple horse shape with text
            knight_font = pygame.font.Font(None, 70)
            knight_text = knight_font.render('♘', True, (139, 69, 19))
            knight_rect = knight_text.get_rect(center=(center_x, center_y + bounce_offset))
            self.screen.blit(knight_text, knight_rect)

    def draw_info_panel(self):
      """Draw information panel at bottom"""
      board_y = self.MARGIN + self.TITLE_HEIGHT + self.BOARD_SPACING
      info_y = board_y + self.BOARD_SIZE * self.CELL_SIZE + self.BOARD_SPACING
    
    # Info background with rounded corners
      info_rect = pygame.Rect(
            self.MARGIN,
            info_y,
            self.WINDOW_WIDTH - 2 * self.MARGIN,
            self.INFO_HEIGHT - 20  # Reduced padding
        )
      pygame.draw.rect(self.screen, self.INFO_BG, info_rect, border_radius=12)
      pygame.draw.rect(self.screen, self.ACCENT_COLOR, info_rect, 3, border_radius=12)
    
    # Stats
      stats_y = info_y + 10
    
    # Current move
      move_text = f"Move: {self.current_step + 1} / {len(self.knight.path)}"
      self.draw_text_with_shadow(move_text, self.font_info, 
                                  self.ACCENT_COLOR, 
                                  self.MARGIN + 20, stats_y)
    
    # Fitness
      fitness_text = f"Squares Visited: {len(self.visited_squares)} / 64"
      fitness_x = self.WINDOW_WIDTH // 2 + 20
      self.draw_text_with_shadow(fitness_text, self.font_info, 
                                  self.ACCENT_COLOR, 
                                  fitness_x, stats_y)
    
    # Progress bar
      progress_y = stats_y + 30
      bar_width = self.WINDOW_WIDTH - 2 * self.MARGIN - 40
      bar_height = 15
      bar_x = self.MARGIN + 20
    
    # Background
      bar_bg_rect = pygame.Rect(bar_x, progress_y, bar_width, bar_height)
      pygame.draw.rect(self.screen, (25, 28, 40), bar_bg_rect, border_radius=8)
      pygame.draw.rect(self.screen, (60, 60, 80), bar_bg_rect, 2, border_radius=8)
    
    # Progress fill
      if len(self.knight.path) > 1:
            progress_ratio = self.current_step / (len(self.knight.path) - 1)
            progress_width = int((bar_width - 4) * progress_ratio)
        
            if progress_width > 0:
                progress_rect = pygame.Rect(bar_x + 2, progress_y + 2, 
                                           progress_width, bar_height - 4)
            
            # Gradient progress bar
                self.draw_gradient_rect(self.screen, 
                                       self.TITLE_GRADIENT_TOP,
                                       self.ACCENT_COLOR,
                                       progress_rect)
                pygame.draw.rect(self.screen, self.ACCENT_COLOR, 
                               progress_rect, 2, border_radius=6)
    
        # Instructions - compact
      inst_y = progress_y + 25
      instructions = "ENTER: Next  |  SPACE: Auto  |  R: Restart  |  ESC: Exit"
    
        # Center instructions
      inst_surface = self.font_instructions.render(instructions, True, (180, 180, 200))
      inst_x = (self.WINDOW_WIDTH - inst_surface.get_width()) // 2
      self.draw_text_with_shadow(instructions, self.font_instructions, 
                                  (180, 180, 200), inst_x, inst_y, shadow=False)


    def draw_completion_banner(self):
        """Draw completion message with close button"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), 
                                pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Banner
        banner_rect = pygame.Rect(
            self.WINDOW_WIDTH // 4,
            self.WINDOW_HEIGHT // 2 - 60,
            self.WINDOW_WIDTH // 2,
            120
        )
        
        pygame.draw.rect(self.screen, (255, 255, 255), banner_rect, border_radius=15)
        pygame.draw.rect(self.screen, self.ACCENT_COLOR, banner_rect, 5, border_radius=15)
        
        # Close button (X) in top-right corner
        close_button_size = 24  # Smaller size
        close_button_rect = pygame.Rect(
            banner_rect.right - close_button_size - 8,
            banner_rect.top + 8,
            close_button_size,
            close_button_size
        )
        
        # Draw simple X symbol
        x_font = pygame.font.Font(None, 32)  # Simple font
        x_text = x_font.render('×', True, (120, 120, 120))  # Gray X
        x_rect = x_text.get_rect(center=close_button_rect.center)
        self.screen.blit(x_text, x_rect)
        
        # Store close button rect for click detection
        self.close_button_rect = close_button_rect
        
        # Text
        complete_font = pygame.font.Font(None, 48)
        complete_text = " COMPLETE! "
        text_surf = complete_font.render(complete_text, True, (50, 150, 50))
        text_rect = text_surf.get_rect(center=banner_rect.center)
        self.screen.blit(text_surf, text_rect)
        
        # Subtext
        sub_font = pygame.font.Font(None, 24)
        sub_text = f"All 64 squares visited in {len(self.knight.path)} moves!"
        sub_surf = sub_font.render(sub_text, True, (80, 80, 80))
        sub_rect = sub_surf.get_rect(center=(banner_rect.centerx, banner_rect.centery + 30))
        self.screen.blit(sub_surf, sub_rect)


    def next_step(self):
        """Advance to next step"""
        if self.current_step < len(self.knight.path) - 1:
            self.current_step += 1
            pos = self.knight.path[self.current_step]
            self.visited_squares.add(pos)
    
    def auto_play(self):
        """Toggle auto-play"""
        self.animating = not self.animating
        self.last_update = time.time()
    
    def restart(self):
        """Restart visualization"""
        self.current_step = 0
        self.visited_squares = {(0, 0)}
        self.animating = False
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # ADD THIS NEW SECTION ↓
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if clicked on close button when completion banner is shown
                    if self.current_step == len(self.knight.path) - 1:
                        if hasattr(self, 'close_button_rect') and self.close_button_rect.collidepoint(event.pos):
                            # Hide banner by moving to previous step and back
                            # This is a trick to dismiss the banner
                            self.banner_dismissed = True
                # END NEW SECTION ↑
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # ENTER
                        self.next_step()
                    
                    elif event.key == pygame.K_SPACE:
                        self.auto_play()
                    
                    elif event.key == pygame.K_r:
                        self.restart()
                    
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            # Animation
            if self.animating:
                current_time = time.time()
                if current_time - self.last_update >= self.animation_speed:
                    if self.current_step < len(self.knight.path) - 1:
                        self.next_step()
                        self.last_update = current_time
                    else:
                        self.animating = False
            
            # Drawing
            self.screen.fill(self.BACKGROUND)
            self.draw_title_bar()
            self.draw_board()
            self.draw_knight()
            self.draw_info_panel()
            
            # Show completion message
            if self.current_step == len(self.knight.path) - 1 and not self.banner_dismissed:
                self.draw_completion_banner()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()


def visualize_solution(knight):
    """
    Create and show beautiful visualization
    
    Args:
        knight: Knight object with completed path
    """
    visualizer = KnightTourVisualizer(knight)
    visualizer.run()


def print_board(knight):
    """
    Print text representation of the board
    """
    board = [[' ' for _ in range(8)] for _ in range(8)]
    
    for i, (row, col) in enumerate(knight.path):
        board[row][col] = str(i + 1)
    
    print("\n" + "="*70)
    print("KNIGHT'S TOUR - TEXT REPRESENTATION")
    print("="*70)
    print("\n     " + "   ".join([str(i) for i in range(8)]))
    print("   +" + "-----+" * 8)
    
    for i, row in enumerate(board):
        print(f" {i} |", end="")
        for cell in row:
            if cell == ' ':
                print(f"  .  |", end="")
            else:
                print(f" {cell:>2s}  |", end="")
        print()
        print("   +" + "-----+" * 8)
    print()
