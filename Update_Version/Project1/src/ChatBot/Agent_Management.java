package ChatBot;
import jade.core.Profile;
import jade.core.ProfileImpl;
import jade.core.Runtime;
import jade.wrapper.AgentContainer;
import jade.wrapper.AgentController;
import jade.wrapper.StaleProxyException;

public class Agent_Management{
    public static void main( String[] args ) {
            try {
                System.out.println("Agent management is launching");
                Runtime rt = Runtime.instance();
                rt.setCloseVM(true);
                Profile profileMain = new ProfileImpl(null, 8888, null);
                AgentContainer ac = rt.createMainContainer(profileMain);

                AgentController agent1 = ac.createNewAgent("Extraction_agent", "src.ChatBot.Extraction_agent", null);
                agent1.start();
                Thread.sleep(10000);
                AgentController agent2 = ac.createNewAgent("QA_agent", "src.ChatBot.QA_agent", null);
                agent2.start();

            } catch (StaleProxyException | InterruptedException e) {
                e.printStackTrace();
            }
    }
}
