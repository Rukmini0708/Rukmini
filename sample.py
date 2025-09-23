import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.Random;

public class SnakeGame extends JFrame {
    public SnakeGame() {
        setTitle("Snake Game - Multithreading");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setResizable(false);
        add(new GamePanel());
        pack();
        setLocationRelativeTo(null);
        setVisible(true);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(SnakeGame::new);
    }
}

class GamePanel extends JPanel implements Runnable, KeyListener {
    private static final int TILE_SIZE = 20;
    private static final int WIDTH = 30;
    private static final int HEIGHT = 20;
    private static final int DELAY = 120; // ms

    private ArrayList<Point> snake;
    private Point food;
    private String direction = "RIGHT";
    private boolean running = true;
    private boolean grow = false;

    private Thread gameThread;
    private Thread inputThread;

    public GamePanel() {
        setPreferredSize(new Dimension(WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE));
        setBackground(Color.BLACK);
        setFocusable(true);
        addKeyListener(this);

        initGame();

        // Game loop thread
        gameThread = new Thread(this);
        gameThread.start();

        // Input handling thread (simulated to show multithreading)
        inputThread = new Thread(() -> {
            while (running) {
                try {
                    Thread.sleep(10);
                } catch (InterruptedException e) { e.printStackTrace(); }
            }
        });
        inputThread.start();
    }

    private void initGame() {
        snake = new ArrayList<>();
        for (int i = 4; i >= 0; i--) {
            snake.add(new Point(i, HEIGHT / 2));
        }
        placeFood();
    }

    private void placeFood() {
        Random rand = new Random();
        while (true) {
            Point p = new Point(rand.nextInt(WIDTH), rand.nextInt(HEIGHT));
            if (!snake.contains(p)) {
                food = p;
                break;
            }
        }
    }

    @Override
    public void run() {
        while (running) {
            moveSnake();
            checkCollision();
            repaint();

            try {
                Thread.sleep(DELAY);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    private void moveSnake() {
        Point head = snake.get(0);
        Point newHead = new Point(head);

        switch (direction) {
            case "UP": newHead.y--; break;
            case "DOWN": newHead.y++; break;
            case "LEFT": newHead.x--; break;
            case "RIGHT": newHead.x++; break;
        }

        snake.add(0, newHead);
        if (newHead.equals(food)) {
            grow = true;
            placeFood();
        }

        if (!grow) {
            snake.remove(snake.size() - 1);
        } else {
            grow = false;
        }
    }

    private void checkCollision() {
        Point head = snake.get(0);

        // Border collision
        if (head.x < 0 || head.x >= WIDTH || head.y < 0 || head.y >= HEIGHT) {
            running = false;
        }

        // Self collision
        for (int i = 1; i < snake.size(); i++) {
            if (head.equals(snake.get(i))) {
                running = false;
            }
        }
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        if (running) {
            // Draw food
            g.setColor(Color.RED);
            g.fillOval(food.x * TILE_SIZE, food.y * TILE_SIZE, TILE_SIZE, TILE_SIZE);

            // Draw snake
            for (int i = 0; i < snake.size(); i++) {
                if (i == 0) g.setColor(Color.GREEN);
                else g.setColor(Color.YELLOW);
                g.fillRect(snake.get(i).x * TILE_SIZE, snake.get(i).y * TILE_SIZE, TILE_SIZE, TILE_SIZE);
            }
        } else {
            g.setColor(Color.WHITE);
            g.setFont(new Font("Arial", Font.BOLD, 28));
            g.drawString("GAME OVER", getWidth() / 2 - 80, getHeight() / 2);
            g.drawString("Score: " + (snake.size() - 5), getWidth() / 2 - 60, getHeight() / 2 + 40);
        }
    }

    // KeyListener methods
    @Override
    public void keyPressed(KeyEvent e) {
        int key = e.getKeyCode();

        if (key == KeyEvent.VK_UP && !direction.equals("DOWN")) direction = "UP";
        if (key == KeyEvent.VK_DOWN && !direction.equals("UP")) direction = "DOWN";
        if (key == KeyEvent.VK_LEFT && !direction.equals("RIGHT")) direction = "LEFT";
        if (key == KeyEvent.VK_RIGHT && !direction.equals("LEFT")) direction = "RIGHT";
        if (key == KeyEvent.VK_Q) running = false;
    }

    @Override public void keyReleased(KeyEvent e) {}
    @Override public void keyTyped(KeyEvent e) {}
}
