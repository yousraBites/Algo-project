public class Node {
    int x, y;           
    int width, height;  
    char orientation;   
    int trapdoor;       
    Node left, right;   

    public Node(int x, int y, int w, int h) {
        this.x = x;
        this.y = y;
        this.width = w;
        this.height = h;
    }
}
