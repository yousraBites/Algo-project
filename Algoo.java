import java.util.Random;

public class Algoo {


    private Node root;
    private char[][] maze;
    private Random rand = new Random();

    public Algoo(int height, int width) {
        maze = new char[height][width];
        for (int i=0; i<height; i++) {
            for (int j=0; j<width; j++) maze[i][j] = ' '; //empty maze
        }
        root = new Node(0, 0, width, height);
        divide(root);
        drawBorders();
    }

    /** Divide recursively */
    private void divide(Node node) {
        if (node.width < 4 || node.height < 4) return; // stop condition

        boolean horizontal = node.width < node.height; 
        node.orientation = horizontal ? 'H' : 'V';

        if (horizontal) {
            int wallY = node.y + rand.nextInt(node.height-2) + 1;
            for (int j=node.x; j<node.x+node.width; j++) maze[wallY][j] = '#';
            node.trapdoor = node.x + rand.nextInt(node.width-2) + 1;
            maze[wallY][node.trapdoor] = ' '; // trapdoor
            node.left  = new Node(node.x, node.y, node.width, wallY-node.y);
            node.right = new Node(node.x, wallY+1, node.width,
                                   node.y+node.height-wallY-1);
        } else {
            int wallX = node.x + rand.nextInt(node.width-2) + 1;
            for (int i=node.y; i<node.y+node.height; i++) maze[i][wallX] = '#';
            node.trapdoor = node.y + rand.nextInt(node.height-2) + 1;
            maze[node.trapdoor][wallX] = ' '; // trapdoor
            node.left  = new Node(node.x, node.y, wallX-node.x, node.height);
            node.right = new Node(wallX+1, node.y,
                                   node.x+node.width-wallX-1, node.height);
        }

        // recurse on children
        divide(node.left);
        divide(node.right);
    }

    /** Draw outer borders */
    private void drawBorders() {
        int h = maze.length, w = maze[0].length;
        for (int i=0; i<h; i++) {
            maze[i][0] = '#';
            maze[i][w-1] = '#';
        }
        for (int j=0; j<w; j++) {
            maze[0][j] = '#';
            maze[h-1][j] = '#';
        }
        // create one exit randomly on the border
        int exitSide = rand.nextInt(4);
        switch (exitSide) {
            case 0: maze[0][rand.nextInt(w-2)+1] = ' '; break;
            case 1: maze[h-1][rand.nextInt(w-2)+1] = ' '; break;
            case 2: maze[rand.nextInt(h-2)+1][0] = ' '; break;
            case 3: maze[rand.nextInt(h-2)+1][w-1] = ' '; break;
        }
    }

    /** Print the maze */
    public void print() {
        for (char[] row : maze) {
            for (char c : row) System.out.print(c);
            System.out.println();
        }
    }

    public static void main(String[] args) {
        Algoo m = new Algoo(20, 40);
        m.print();
    }
}
