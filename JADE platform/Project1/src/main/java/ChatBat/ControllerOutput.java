package src.main.java.ChatBat;

public class ControllerOutput extends Controller{
    public ControllerOutput(Model m) {
        super(m);
    }
    public void output(String input_message){
        m.setMessage(input_message);
    }
}
