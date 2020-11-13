package src.main.java.ChatBat;
import jade.core.Agent;
import jade.core.behaviours.SimpleBehaviour;

public class QA_agent extends Agent {
    @Override
    protected void setup() {
        SimpleBehaviour sb = new SimpleBehaviour() {
            @Override
            public void action() {
                System.out.println("QA_agent is launching");
                javax.swing.SwingUtilities.invokeLater(new Runnable() {
                    @Override
                    public void run() {
                        Model m = new Model(); // Single shared model.
                        ControllerOutput c1 = new ControllerOutput(m);
                        ViewOutput v1 = new ViewOutput(m, c1);
                    }
                });
            }
            @Override
            public boolean done() {
                return true;
            }
        };
        this.addBehaviour(sb);
    }
}
