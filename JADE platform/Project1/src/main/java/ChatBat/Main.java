package src.main.java.ChatBat;

public class Main {
    public static void main(String[] args) {
        javax.swing.SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                Model m = new Model(); // Single shared model.
                ControllerOutput c1 = new ControllerOutput(m);
                ViewOutput v1 = new ViewOutput(m, c1);
            }
        });

    }
}
