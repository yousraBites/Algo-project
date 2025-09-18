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


#Modifications made :
# First obviously before the way we represented the binary tree was very bad, now its much better, only leaf node are sections of the final maze (no more useless nodes), and each leaf is connected to it's parent node (which is the passage that contains it) (this makes it way easier for applying the solving algorithm later on) , especially for backtracking to find the path
# also the exit doesnt have to be on the root node anymore, it can be anywhere or even as a trapdoor inside the maze , its basically just a cell like any other cell in the maze
# Second, i added a check to avoid placing walls that would block existing trapdoors (this was a tricky one to implement but it works well now) , finnally got it working after almost a week of trying different things
# Third, i changed the way we pick wall positions, now we first create a list of valid positions to place the wall (that doesnt block existing trapdoors) , and then we pick one randomly from that list (this avoids the problem of getting stuck in an infinite loop if we keep picking random positions that are invalid)
#I have made sure to comment everything properly so its easy to understand
# I might add a maze solving algorithm later on (probably backtracking) , but for now this is all i can do for today
import random

class Node:
    def __init__(self, height, width, start_row=0, start_col=0):
        self.height = height
        self.width = width
        self.start_row = start_row
        self.start_col = start_col
        self.wall_position = None  # where we cut this rectangle
        self.shared_trapdoor = None  # connects the two halves
        self.orientation = None  # horizontal or vertical cut
        self.left = None
        self.right = None
        self.is_leaf = False  # true when too small to cut
        
    def __repr__(self):
        if self.is_leaf:
            return f"Leaf(h={self.height}, w={self.width}, pos=({self.start_row},{self.start_col}))"
        else:
            return f"Node(h={self.height}, w={self.width}, pos=({self.start_row},{self.start_col}), trapdoor={self.shared_trapdoor})"

def print_maze(maze):
    # using unicode blocks looks better than # and spaces
    for row in maze:
        display_row = []  
        for cell in row:
            if cell == '#':
                display_row.append('█')
            elif cell == ' ':
                display_row.append('·')
            else:
                display_row.append(cell)
        print(''.join(display_row))

def generate_maze(height, width):
    # root node is the whole inside area (not counting border)
    root = Node(height-2, width-2, start_row=1, start_col=1)
    
    # put exit on right side (for now)
    exit_position = (height-2, width-1)
    
    # create maze: walls on border, empty inside
    maze = [['#' for _ in range(width)] for _ in range(height)] 
    maze[exit_position[0]][exit_position[1]] = ' '
    for i in range(1, height-1): 
        for j in range(1, width-1):
            maze[i][j] = ' '
    
    divide(root, maze)
    
    return maze, root



def would_block_trapdoors(wall_positions, existing_trapdoors, orientation):
    # check if new wall would block existing trapdoors
    # blocking = trapdoor right next to wall end
    if not existing_trapdoors or not wall_positions:
        return False
    #basically this will check if any existing trapdoor is adjacent to the new wall
    for trapdoor_row, trapdoor_col in existing_trapdoors:
        if orientation == "horizontal": 
            wall_row = wall_positions[0][0]
            if trapdoor_row == wall_row: # this means they are on the same row (now we check if they are adjacent)
                wall_start_col = min(pos[1] for pos in wall_positions) #leftmost column of the wall
                wall_end_col = max(pos[1] for pos in wall_positions) #rightmost column of the wall
                if trapdoor_col == wall_start_col - 1 or trapdoor_col == wall_end_col + 1: #adjacent to left or right end of the wall
                    return True
        else:  # vertical (same logic but for columns)
            wall_col = wall_positions[0][1]
            if trapdoor_col == wall_col:
                wall_start_row = min(pos[0] for pos in wall_positions)
                wall_end_row = max(pos[0] for pos in wall_positions)
                if trapdoor_row == wall_start_row - 1 or trapdoor_row == wall_end_row + 1:
                    return True
    
    return False

def divide(node, maze, existing_trapdoors=None):
    # recursively split rectangles until they're too small
    if existing_trapdoors is None:
        existing_trapdoors = set() # set of (row, col) for existing trapdoors , we track them to avoid blocking them with new walls
    
    # stop if area is too small (can be adjusted (for now this works good))
    if node.height <= 3 or node.width <= 3:
        node.is_leaf = True
        return
    
    # choose cut direction based on shape
    if node.height > node.width:
        node.orientation = "horizontal"
    elif node.width > node.height:
        node.orientation = "vertical"
    else:
        node.orientation = random.choice(["horizontal", "vertical"])  # square = random
    
    if node.orientation == "horizontal":
        # horizontal wall splits into top/bottom
        #basically i decided to keep a list of valid positions to place the wall (so we dont have to keep picking random positions until we find a valid one) , and then we pick one randomly from that list;
        #the condition for a valid position is that it should not block existing trapdoors and should not overlap existing walls
        valid_positions = []
        for pos in range(2, node.height - 2): # leave space at edges
            wall_row = node.start_row + pos 
            
            # get all wall positions
            wall_positions = []
            for j in range(node.start_col, node.start_col + node.width): # all columns in this row
                wall_positions.append((wall_row, j)) 
            
            # don't block existing trapdoors 
            # we basically check if any existing trapdoor is adjacent to the new wall (took a while to figure this one out !!)
            would_block = (would_block_trapdoors(wall_positions, existing_trapdoors, "horizontal"))
            
            if not would_block:
                valid_positions.append(pos) #result is a list of valid positions (perfect stuff(Big Brain))
        
        if not valid_positions: # no valid positions to place wall (this should be rare) 
            node.is_leaf = True
            return
            
        wall_position = random.choice(valid_positions) #pick one randomly from the valid positions (i decided to still keep a bit of randomness rather than always picking a fixed one)
        node.wall_position = wall_position
        
        #END OF PICKING WALL POSITION
        
        # pick trapdoor position (not at edges)
        trapdoor_position = random.randint(1, node.width - 2)
        wall_row = node.start_row + wall_position
        trapdoor_col = node.start_col + trapdoor_position
        node.shared_trapdoor = (wall_row, trapdoor_col) 
        
        existing_trapdoors.add(node.shared_trapdoor) # add this new trapdoor to the set of existing ones (this way we have a record of all existing trapdoors (and we can avoid blocking them later))
        
        # draw wall
        for j in range(node.start_col, node.start_col + node.width):
            maze[wall_row][j] = '#'
        maze[wall_row][trapdoor_col] = ' '  # make hole
        
        # create children
        top = Node(wall_position, node.width, node.start_row, node.start_col)
        bottom = Node(node.height - wall_position - 1, node.width, wall_row + 1, node.start_col)
        
        node.left = top
        node.right = bottom
        
        # keep going
        divide(top, maze, existing_trapdoors)
        divide(bottom, maze, existing_trapdoors)
        
    else:  # vertical
        # vertical wall splits into left/right
        #Same stuff here
        valid_positions = []
        for pos in range(2, node.width - 2):
            wall_col = node.start_col + pos
            
            wall_positions = []
            for i in range(node.start_row, node.start_row + node.height):
                wall_positions.append((i, wall_col))
            
            would_block = (would_block_trapdoors(wall_positions, existing_trapdoors, "vertical"))
            
            if not would_block:
                valid_positions.append(pos)
        
        if not valid_positions:
            node.is_leaf = True
            return
            
        wall_position = random.choice(valid_positions)
        node.wall_position = wall_position
        
        trapdoor_position = random.randint(1, node.height - 2)
        wall_col = node.start_col + wall_position
        trapdoor_row = node.start_row + trapdoor_position
        node.shared_trapdoor = (trapdoor_row, wall_col)
        
        existing_trapdoors.add(node.shared_trapdoor)
        
        for i in range(node.start_row, node.start_row + node.height):
            maze[i][wall_col] = '#'
        maze[trapdoor_row][wall_col] = ' '
        
        left = Node(node.height, wall_position, node.start_row, node.start_col)
        right = Node(node.height, node.width - wall_position - 1, node.start_row, wall_col + 1)
        
        node.left = left
        node.right = right
        
        divide(left, maze, existing_trapdoors)
        divide(right, maze, existing_trapdoors)
        
# maze solving - maybe later
def solve_maze(maze, start, end):
    return

if __name__ == "__main__":
    maze_result, root_node = generate_maze(12, 24)
    
    print("Generated Maze:")
    print_maze(maze_result)
    
    empty_cells = sum(row.count(' ') for row in maze_result)
    print(f"\nMaze statistics:")
    print(f"Total empty cells: {empty_cells}")
    print(f"Maze dimensions: {len(maze_result)} x {len(maze_result[0])}")
    
    