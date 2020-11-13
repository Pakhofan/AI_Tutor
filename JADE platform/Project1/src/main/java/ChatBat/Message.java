package src.main.java.ChatBat;

public class Message {
    public String sender;
    public String content;

    public Message(String input_sender, String input_content) {
        sender = input_sender;
        content = input_content;
    }

    public String getSender() {
        return sender;
    }

    public String getContent() {
        return content;
    }
}
