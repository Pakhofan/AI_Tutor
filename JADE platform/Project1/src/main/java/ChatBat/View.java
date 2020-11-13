package src.main.java.ChatBat;

import javax.swing.*;

public abstract class View<T extends Controller> extends JFrame implements ModelListener {
    protected Model m;
    protected T c;
    public View(Model m, T c) {
        this.m = m;
        this.c = c;
        m.addListener(this);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }
    @Override
    public abstract void update();
}
