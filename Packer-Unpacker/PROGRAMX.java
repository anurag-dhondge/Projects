import java.awt.*;
import java.awt.event.*;
import java.util.*;
import MarvellousPackerUnpacker.MarvellousPacker;
import MarvellousPackerUnpacker.MarvellousUnpacker;

public class PROGRAMX {
    Frame mainFrame;
    Label headerLabel;
    Label statusLabel;
    Panel controlPanel;

    public PROGRAMX() {
        mainFrame = new Frame("Marvellous Packer-Unpacker");
        mainFrame.setSize(500, 300);
        mainFrame.setLayout(new GridLayout(3, 1));

        mainFrame.addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                System.exit(0);
            }
        });

        headerLabel = new Label();
        headerLabel.setAlignment(Label.CENTER);

        statusLabel = new Label();
        statusLabel.setAlignment(Label.CENTER);
        statusLabel.setSize(400, 100);

        controlPanel = new Panel();
        controlPanel.setLayout(new FlowLayout());

        mainFrame.add(headerLabel);
        mainFrame.add(controlPanel);
        mainFrame.add(statusLabel);
        mainFrame.setVisible(true);
    }

    public static void main(String[] args) {
        PROGRAMX app = new PROGRAMX();  // Corrected constructor call
        app.Display();
    }

    private void Display() {
        headerLabel.setText("Select Operation");

        Button packButton = new Button("Pack Directory");
        Button unpackButton = new Button("Unpack File");

        packButton.setActionCommand("PACK");
        unpackButton.setActionCommand("UNPACK");

        packButton.addActionListener(new MyListener());
        unpackButton.addActionListener(new MyListener());

        controlPanel.add(packButton);
        controlPanel.add(unpackButton);

        mainFrame.setVisible(true);
    }

    private class MyListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            String command = e.getActionCommand();

            try {
                if (command.equals("PACK")) {
                    String dirName = prompt("Enter the name of the directory to pack:");
                    String packName = prompt("Enter the name of the packed file to create:");

                    MarvellousPacker mobj = new MarvellousPacker(packName, dirName);
                    mobj.PackingActivity();
                    statusLabel.setText("Packing completed: " + packName);

                } else if (command.equals("UNPACK")) {
                    String unpackFile = prompt("Enter the packed file name to unpack:");

                    MarvellousUnpacker mobj = new MarvellousUnpacker(unpackFile);
                    mobj.UnpackingActivity();
                    statusLabel.setText("Unpacking completed: " + unpackFile);
                }
            } catch (Exception ex) {
                statusLabel.setText("Operation failed: " + ex.getMessage());
            }
        }

        // Prompt dialog for user input
        private String prompt(String message) {
            return javax.swing.JOptionPane.showInputDialog(null, message);
        }
    }
}
