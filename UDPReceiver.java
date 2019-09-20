

import java.net.*;

public class UDPReceiver {

	private final static int PACKETSIZE = 100 ;

	public static void main( String args[] )
	{ 
	    // Check the arguments
            
        //Commented out for testing
	    if( args.length != 1 )
	    {
	        System.out.println( "usage: UDPReceiver port" ) ;
	        return ;
	    }
             
		// Construct the socket
		DatagramSocket socket = new DatagramSocket( port ) ;
		try
		{
			// Convert the argument to ensure that is it valid
			int port = Integer.parseInt( args[0] ) ;
			//int port = 1226;//test purposes
			
			while(true) // broken only by keyboard interrupt.
			{
				System.out.println( "Receiving on port " + port ) ;
				DatagramPacket packet = new DatagramPacket( new byte[PACKETSIZE], PACKETSIZE ) ;
				socket.receive( packet ) ;

				System.out.println( packet.getAddress() + " " + packet.getPort() + ": " + new String(packet.getData()).trim() ) ;
					
				//socket = null;
				String message = "ACK:" + new String(packet.getData()).trim();
				byte[] data = message.getBytes();
				
				socket.send(new DatagramPacket(data, data.length, packet.getAddress(), packet.getPort()));
					
			}  
		}
		catch( Exception e )
		{
			System.out.println( e ) ;
		} 
		finally 
		{
			socket.close();
		}
  }
}

