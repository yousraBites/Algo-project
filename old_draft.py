#Create a binary tree maze where we start by an empty box (width and height) and we randomly divide it into two parts
#by drawing a wall either horizontally or vertically. We repeat this process recursively for each of the two parts until we reach a minimum size (to be determined).
#We then create a passage between the two parts by removing a wall segment.(trapdoor) 
#The trapdoor location is gonna be equal to an integer random number between 1 and the size of the wall -1 (to avoid creating a passage at the edge of the wall).
#The maze is represented as a 2D array of characters, where '#' represents a wall and ' ' represents a passage.
#The algorithm starts with a single node representing the entire maze area
#Each node in the binary tree represents a rectangular area of the maze, and the leaves represent the final passages.
#Node contents:
#height: height of the node
#width: width of the node
#trapdoor: location of the trapdoor
#orientation: orientation of the wall (horizontal or vertical)
#left: left child node
#right: right child node
import random

class Node:
    def __init__(self, height, width, start_row=0, start_col=0):
        self.height = height
        self.width = width
        self.start_row = start_row
        self.start_col = start_col
        self.trapdoor = None
        self.orientation = None
        self.left = None
        self.right = None
        self.is_leaf = False
        
    def __repr__(self):
        return f"Node(h={self.height}, w={self.width}, pos=({self.start_row},{self.start_col}))"

division_step = 0

def print_maze_with_step(maze, step_info=""):
    """Print the maze with step information using better characters"""
    global division_step
    division_step += 1
    print(f"\n--- Step {division_step}: {step_info} ---")
    for row in maze:
        # Convert characters for better visualization
        display_row = []
        for cell in row:
            if cell == '#':
                display_row.append('█')  # Full block for walls
            elif cell == ' ':
                display_row.append('·')  # Middle dot for passages
            else:
                display_row.append(cell)
        print(''.join(display_row))
    print()

def generate_maze(height, width):
    global division_step
    division_step = 0
    
    # Root covers the inner area only (excluding border walls)
    #the root should have an exit which is a passage in one of the walls(trapdoor)
    
    root = Node(height-2, width-2, start_row=1, start_col=1)
    #deterùmine trapdoor position
    rng = random.Random()
    #the exit will be on the edges
    root.trapdoor = (rng.randint(0, height-1), 0)  # Left wall exit
    #or could be on any wall (TODO)
    print(f"Chosen trapdoor position for root: {root.trapdoor}")
    # Start with outer walls and empty interior
    maze = [['#' for _ in range(width)] for _ in range(height)] 
    maze[root.trapdoor[0]][root.trapdoor[1]] = ' '
    for i in range(1, height-1): 
        for j in range(1, width-1):
            maze[i][j] = ' '
    
    
    print("Initial maze:")
    # Display with better characters
    for row in maze:
        display_row = []
        for cell in row:
            if cell == '#':
                display_row.append('█')  # Full block for walls
            elif cell == ' ':
                display_row.append('·')  # Middle dot for passages
            else:
                display_row.append(cell)
        print(''.join(display_row))
    print()
    

    print(f"Root node: {root}")
    
    divide(root, maze)
    
    return maze

def divide(node, maze):
    """
    Recursively divide the maze area represented by the node.
    """
    
    # Stop condition - ensure minimum space AND prevent tiny areas
    if node.height <= 2 or node.width <= 2:
        node.is_leaf = True
        return
    
    # Choose orientation
    if node.height > node.width:
        node.orientation = "horizontal"
    elif node.width > node.height:
        node.orientation = "vertical"
    else:
        node.orientation = random.choice(["horizontal", "vertical"])
    
    if node.orientation == "horizontal":
        # Find all valid wall positions
        valid_positions = []
        for pos in range(2, node.height - 2):  # Leave more space - start at 2, end at height-2
            wall_row = node.start_row + pos
            
            # Check if row is empty
            is_empty = True
            for j in range(node.start_col, node.start_col + node.width):
                if maze[wall_row][j] == '#':
                    is_empty = False
                    break
            
            # More thorough adjacent check - look 2 rows up and down
            blocks_passage = False
            
            # Check 2 rows above and below to ensure we don't block passages
            #this check is not enough, we need to check more thoroughly
            #for example 
            for offset in [-2, -1, 1, 2]:
                check_row = wall_row + offset
                if (check_row >= node.start_row and 
                    check_row < node.start_row + node.height):
                    for j in range(node.start_col, node.start_col + node.width):
                        if maze[check_row][j] == '#':
                            blocks_passage = True
                            break
                    if blocks_passage:
                        break
            
            if is_empty and not blocks_passage:
                valid_positions.append(pos)
        
        if not valid_positions:
            node.is_leaf = True
            return
        
        wall_position = random.choice(valid_positions)
        
        #what if we decide to put the wall not randomly but in a more clever way?
        #for example, we can put it in the middle but still in a valid position
        #wall_position = valid_positions[len(valid_positions)//2]

        trapdoor_position = random.randint(0, node.width - 1)
        
        
        wall_row = node.start_row + wall_position
        trapdoor_col = node.start_col + trapdoor_position
        
        # Draw wall with trapdoor
        for j in range(node.start_col, node.start_col + node.width):
            maze[wall_row][j] = '#'
        maze[wall_row][trapdoor_col] = ' '
        
        print_maze_with_step(maze, f"Horizontal wall at row {wall_row}, trapdoor at col {trapdoor_col}")
        
        # Create children
        top = Node(wall_position, node.width, node.start_row, node.start_col)
        bottom = Node(node.height - wall_position - 1, node.width, wall_row + 1, node.start_col)
        
        node.left = top
        node.right = bottom
        
        divide(top, maze)
        divide(bottom, maze)
        
    else:  # vertical
        # Find all valid wall positions
        valid_positions = []
        for pos in range(2, node.width - 2):  # Leave more space - start at 2, end at width-2
            wall_col = node.start_col + pos
            
            # Check if column is empty
            is_empty = True
            for i in range(node.start_row, node.start_row + node.height):
                if maze[i][wall_col] == '#':
                    is_empty = False
                    break
            
            # More thorough adjacent check - look 2 columns left and right
            blocks_passage = False
            
            # Check 2 columns left and right to ensure we don't block passages
            for offset in [-2, -1, 1, 2]: #is this check enough?
                
                check_col = wall_col + offset
                if (check_col >= node.start_col and 
                    check_col < node.start_col + node.width):
                    for i in range(node.start_row, node.start_row + node.height):
                        if maze[i][check_col] == '#':
                            blocks_passage = True
                            break
                    if blocks_passage:
                        break
            
            if is_empty and not blocks_passage:
                valid_positions.append(pos)
        
        if not valid_positions:
            node.is_leaf = True
            return
        
        wall_position = random.choice(valid_positions)
        trapdoor_position = random.randint(0, node.height - 1)
        
        wall_col = node.start_col + wall_position
        trapdoor_row = node.start_row + trapdoor_position
        
        # Draw wall with trapdoor
        for i in range(node.start_row, node.start_row + node.height):
            maze[i][wall_col] = '#'
        maze[trapdoor_row][wall_col] = ' '
        
        print_maze_with_step(maze, f"Vertical wall at col {wall_col}, trapdoor at row {trapdoor_row}")
        
        # Create children
        left = Node(node.height, wall_position, node.start_row, node.start_col)
        right = Node(node.height, node.width - wall_position - 1, node.start_row, wall_col + 1)
        
        node.left = left
        node.right = right
        
        divide(left, maze)
        divide(right, maze)

# Test
if __name__ == "__main__":
    print("=== GENERATING MAZE ===")
    maze_result = generate_maze(12, 24)
    
    print("\n=== FINAL MAZE ===")
    for row in maze_result:
        display_row = []
        for cell in row:
            if cell == '#':
                display_row.append('█')  # Full block for walls
            elif cell == ' ':
                display_row.append('·')  # Middle dot for passages
            else:
                display_row.append(cell)
        print(''.join(display_row))
    
    # Simple connectivity test
    def count_empty_cells(maze):
        count = 0
        for row in maze:
            for cell in row:
                if cell == ' ':
                    count += 1
        return count
    
    empty_cells = count_empty_cells(maze_result)
    print(f"\nMaze statistics:")
    print(f"Total empty cells: {empty_cells}")
    print(f"Maze dimensions: {len(maze_result)} x {len(maze_result[0])}")

