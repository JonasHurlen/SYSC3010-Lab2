
import java.net.*;
import java.util.Scanner;

public class UDPSender {
    private final static int PACKETSIZE = 100 ;

    public static void main(String[] args) {
        // Check the arguments
        if (args.length != 3) {
            System.out.println("usage: java UDPSender host port message number");
            return;
        }
        DatagramSocket socket = null;
        try {
            // Convert the arguments first, to ensure that they are valid
            InetAddress host = InetAddress.getByName(args[0]);
            int port = Integer.parseInt(args[1]);
            int msg_count = Integer.parseInt(args[2]);
            socket = new DatagramSocket();

            if (msg_count == 1) { // standard single message sending
                Scanner in;
                in = new Scanner(System.in);
                String message = null;
                while (true) {
                    System.out.println("Enter text to be sent, ENTER to quit ");
                    message = in.nextLine();
                    if (message.length() == 0) {
                        break;
                    }
                    byte[] data = message.getBytes();
                    DatagramPacket packet = new DatagramPacket(data, data.length, host, port);
                    socket.send(packet);
                }
                System.out.println("Closing down");
            } else {// sends n messages and recieves confirmation
                DatagramPacket packet;
                for (int msg_sent = 0; msg_sent < msg_count; msg_sent++) {
                    
                    String message = "Message " + String.valueOf(msg_sent);
                    byte[] data = message.getBytes();
                    packet = new DatagramPacket(data, data.length, host, port);
                    socket.send(packet);
                    

                    packet = new DatagramPacket( new byte[PACKETSIZE], PACKETSIZE ) ;
	            socket.receive( packet ) ;
                    System.out.println( packet.getAddress() + " " + packet.getPort() + ": " + new String(packet.getData()).trim() ) ;

                }
            }

        } catch (Exception e) {
            System.out.println(e);
        } finally {
            if (socket != null) {
                socket.close();
            }
        }
    }
}
