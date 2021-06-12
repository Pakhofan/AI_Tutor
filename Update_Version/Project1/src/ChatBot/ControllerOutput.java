package ChatBot;

public class ControllerOutput extends Controller{
    public ControllerOutput(Model m) {
        super(m);
    }
    public void output(String input_message){
        m.setMessage(input_message);
    }
}
