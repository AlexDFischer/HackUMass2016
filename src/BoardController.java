import java.io.*;
import java.net.Socket;
import java.util.Scanner;

import com.leapmotion.leap.*;

public class BoardController {
	static Socket socket;
	static String host; // 128.119.149.32
	static int port;
	static BufferedWriter piWriter;

	public static void main(String[] args) {
		// get host and port
		Scanner s = new Scanner(System.in);
		System.out.println("Hostname of pi: ");
		host = s.nextLine();
		System.out.println("Port to use: ");
		port = s.nextInt();
		s.nextLine();
		
		try
		{
			socket = new Socket(host, port);
			piWriter = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
			piWriter.write("maze\n"); // I think people are messing with me
		} catch (IOException e)
		{
			System.out.println("Error: unable to connect to RPi");
			e.printStackTrace();
			s.close();
			System.exit(1);
		}
		
		Controller controller = new Controller();
		Listener listener = new CustomListener();
		controller.addListener(listener);
		
		System.out.println("Press enter to quit...");
        s.nextLine();
        s.close();
	}
	private static class CustomListener extends Listener
	{
		public void onConnect(Controller controller)
		{
	        System.out.println("Connected");
		}
		
		public void onFrame(Controller controller) {
	        System.out.println("Frame available");
	        Frame frame = controller.frame();
	        
	        HandList hands = frame.hands();
	        if (hands.count() == 1)
	        {
	        	Hand hand = hands.get(0);
	        	float pitch = hand.direction().pitch();
	        	float roll = hand.palmNormal().roll();
	        	System.out.println("pitch=" + pitch + " roll=" + roll);
	        	try
	        	{
	        		piWriter.write(roll + "," + pitch+"\n");
	        		piWriter.flush();
	        	} catch (IOException e)
	        	{
	        		System.out.println("Error: unable to write to RPi");
	        		e.printStackTrace();
	        	}
	        } else
	        {
	        	System.out.print("need to have one hand");
	        	return;
	        }
		}
	}
}
