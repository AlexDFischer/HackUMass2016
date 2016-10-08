import java.io.IOException;
import com.leapmotion.leap.*;

class Sample {
    public static void main(String[] args) {
        //Create a sample listener and controller
        SampleListener listener = new SampleListener();
        Controller controller = new Controller();
    
        //Have the sample listener receive events from the controller
        controller.addListener(listener);

        //Keep this process running until enter is pressed
        System.out.println("Press enter to quit...");
        try {
            System.in.read();
        } catch (IOException e) {
            e.printStackTrace();
        }

        //Remove the sample listener when done
        controller.removeListener(listener);
    }
}

class SampleListener extends Listener {
    
    public void onConnect(Controller controller) {
        System.out.println("Connected");
        controller.enableGesture(Gesture.Type.TYPE_SWIPE);
    }

    public void onFrame(Controller controller) {
        System.out.println("Frame available");
        Frame frame = controller.frame();
        
        HandList hands = frame.hands();
        Hand firstHand = hands.get(0);
        float pitch = firstHand.direction().pitch();
        float yaw = firstHand.direction().yaw();
        float roll = firstHand.palmNormal().roll();
        
        
        System.out.println("Frame id: " + frame.id()
        + ", timestamp: " + frame.timestamp()
        + ", hands: " + frame.hands().count()
        + ", fingers: " + frame.fingers().count()
        + ", tools: " + frame.tools().count()
        + ", gestures " + frame.gestures().count()
        + ", pitch " + pitch
        + ", yaw " + yaw
        + ", roll " + roll);
    }
}
