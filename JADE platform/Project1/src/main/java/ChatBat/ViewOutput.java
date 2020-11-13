package src.main.java.ChatBat;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class ViewOutput  extends View<ControllerOutput>  {
    private JLabel label;
    private JScrollBar sBar;
    private Integer isNeedBottom = 0;
    private String message = "<div style='color:blue'>Christopher:</div>" + "My pleasure to serve for you.";
    private Integer message_index = 0;
    public ViewOutput(Model m, ControllerOutput c) {
        super(m, c);
        m.addListener(this);
        this.setTitle("Chat Window");
        this.setSize(1250, 520);
        this.setLocationRelativeTo(null); //Make the window locate in the center
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setResizable(false); //Forbid changing the size of window
        Container container = getContentPane();
        container.setLayout(new FlowLayout(FlowLayout.RIGHT)); //The flow layout, align left

        label = new JLabel();  //Label
        label.setOpaque(true); //Make the background not transparent to see the color
        label.setBackground(Color.WHITE); //background color
        label.setVerticalAlignment(JLabel.TOP); //set the text to the top
        JScrollPane js2 = new JScrollPane(label); //Slide bar for pulling up and down
        Font f=new Font(Font.DIALOG,Font.BOLD,16);//The font size in the window
        label.setFont(f);//Add the font size property to the label

        sBar = js2.getVerticalScrollBar(); //get the JScrollBar

        js2.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
        js2.setPreferredSize(new Dimension(970,320));
        update();

        // Initialize the label using the model.
        JTextArea jt1 = new JTextArea();
        jt1.setRows(7);
        jt1.setColumns(136);
        JScrollPane js1 = new JScrollPane(jt1); //Slide bar for pulling up and down

        JButton buttonSend = new JButton("Send");   // Button
        buttonSend.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                c.output(jt1.getText());
                jt1.setText(""); //Clean the input window after finishing sending message

                // The roll bar to the bottom to see the latest message
                js2.getVerticalScrollBar().addAdjustmentListener(event -> {
                    JViewport vp = js2.getViewport();
                    if (vp.getView().getHeight() > vp.getHeight() + vp.getViewPosition().y) {
                        sBar.setValue(sBar.getMaximum()); //Set the location of roll bar to the bottom
                    }
                });
                // The roll bar to the bottom to see the latest message
            }
        });
        buttonSend.setSize(200,30);

        JLabel image_label = new JLabel();
        image_label.setSize(250,250);
        Icon icon = new ImageIcon("src/main/java/ChatBot/robot.jpg");//Load the image of AI robot
        image_label.setIcon(icon);

        container.add(js2);
        container.add(image_label);
        container.add(js1);
        container.add(buttonSend); //Add a JButton.
        this.setVisible(true);
    }
    // When notified of a change by the model, the view gets the new
    // value of the counter from the model, and updates its label.
    @Override  public void update() {
        label.setText("<html>"+message);
        while(m.getMessage()[message_index]!=null){
            message = message + "<br>" + m.getMessage()[message_index];
            message_index++;
        }
    }
}
