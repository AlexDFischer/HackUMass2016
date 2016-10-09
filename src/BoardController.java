import java.io.IOException;

import com.leapmotion.leap.*;
import java.io.*;
import java.net.*;
import java.util.Scanner;

class BoardController {

	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		MotionListener listener = new MotionListener();
		Controller controller = new Controller();
		Scanner in = new Scanner(System.in);
		System.out.println("Enter a number"); //STOPPED HERE
		
		controller.addListener(listener);
		
		System.out.println("Press enter to quit...");
        try {
            System.in.read();
        } catch (IOException e) {
            e.printStackTrace();
        }
	}
}

class MotionListener extends Listener {
	
	public void onConnect(Controller controller) {
        controller.enableGesture(Gesture.Type.TYPE_SWIPE);
    }

    public void onFrame(Controller controller) {
    	Frame frame = controller.frame();
        HandList hands = frame.hands();
        Hand hand = hands.get(0);
        float pitch = hand.direction().pitch();
        float roll = hand.palmNormal().roll();
    }
}


