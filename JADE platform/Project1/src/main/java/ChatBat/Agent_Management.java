package src.main.java.ChatBat;
import jade.core.Agent;
import jade.core.behaviours.SimpleBehaviour;

public class Agent_Management extends Agent{
    @Override
    protected void setup() {
        SimpleBehaviour sb = new SimpleBehaviour() {
            @Override
            public void action() {
                System.out.println("Agent_Management is launching, choose the agent to execute.");
            }
            @Override
            public boolean done() {
                return true;
            }
        };
        this.addBehaviour(sb);
    }
}
