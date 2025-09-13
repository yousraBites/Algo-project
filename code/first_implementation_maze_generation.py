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

maze = []
# Define the Node class to represent each section of the maze
class Node:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.trapdoor = None
        self.orientation = None
        self.left = None
        self.right = None
        self.is_leaf = False #to represent stop loss condition flag
        
    def __repr__(self):
        return f"Node(height={self.height}, width={self.width}, trapdoor={self.trapdoor}, orientation={self.orientation})"
# Maze generation function
def generate_maze(height, width):
    # Initialize the empty maze 
    maze = [['#' for _ in range(width)] for _ in range(height)]
    for i in range(1, height-1):
        for j in range(1, width-1):
            maze[i][j] = ' '
    for row in maze:
        print(''.join(row))
        
    # root node representing the entire maze area
    root = Node(height-2, width-2) # -2 for outer walls
    divide(root)
    print(root)
    return maze

# Recursive function to divide the maze area
# we dont use coordinates 
def divide(node):
    #Tasks tp be done:
    #1. Check the stop loss condition (if the node is too small to divide further
    #2. Decide the orientation of the wall (horizontal or vertical)
    #3. Draw the wall in the maze
    #4. Create a trapdoor in the wall
    #5. Create left and right child nodes
    #6. Recursively divide the left and right child nodes
    
    if node.height <=2 and node.width <=2: #Stop condition
        node.is_leaf = True
        return
    
    #Orientation rules: if height < width : vertical , else horizontal
    node.orientation = "horizontal" if node.height < node.width else "vertical"
    
    #possible values from 1 to Wall -2
    if node.orientation == "horizontal":
        wall_divider = random.randint(1, node.height -1)
        node.trapdoor = random.randint(1, node.width -1)
        
        #Creating the left and right node
        left = Node(wall_divider, node.width)
        right= Node(node.height - wall_divider, node.width)
        node.left = left
        node.right = right

        #Drawing the wall
        for i in range(node.height):
            if i == wall_divider:
                continue
            maze[i][node.trapdoor] = '#'
        maze[wall_divider][node.trapdoor] = ' ' #Creating the trapdoor

        #Recursive case
        
        divide(left)
        divide(right)
    else:
        wall_divider = random.randint(1,node.width - 2)
        node.trapdoor = random.randint(1,node.height - 2)
        
        #Creating the left and right node
        left = Node(node.height, wall_divider)
        right= Node(node.height, node.width - wall_divider)
        node.left = left
        node.right = right
        #Drawing the wall
        for j in range(node.width):
            if j == wall_divider:
                continue
            maze[node.trapdoor][j] = '#'
        maze[node.trapdoor][wall_divider] = ' ' #Creating the trapdoor
        #Recursive case
        divide(left)
        divide(right)
        
        
         
        
        
        
#test
generate_maze(10, 40)
    
    