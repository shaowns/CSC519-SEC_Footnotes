import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;

public class Test
{
	public static void main(String args[])
	{
		int lport=5659;
        String rhost="152.1.26.121";
        String host="152.1.26.121";
        int rport=3306;
        String user="team4";
        String password="tS7?^T*N";
        String dbuserName = "team4";
        String dbpassword = "team4";
        String url = "jdbc:mysql://localhost:"+lport+"/sec";
        String driverName="com.mysql.jdbc.Driver";
        Connection conn = null;
        Session session= null;
	        try{
	            //Set StrictHostKeyChecking property to no to avoid UnknownHostKey issue
	            java.util.Properties config = new java.util.Properties(); 
	            config.put("StrictHostKeyChecking", "no");
	            JSch jsch = new JSch();
	            session=jsch.getSession(user, host, 22);
	            session.setPassword(password);
	            session.setConfig(config);
	            session.connect();
	            System.out.println("Connected");
	            int assinged_port=session.setPortForwardingL(lport, rhost, rport);
	            System.out.println("localhost:"+assinged_port+" -> "+rhost+":"+rport);
	            System.out.println("Port Forwarded");
	             
	            //mysql database connectivity
	            Class.forName(driverName).newInstance();
	            conn = DriverManager.getConnection (url, dbuserName, dbpassword);
	            
	            
	        }catch(Exception e){
	            e.printStackTrace();
	        }finally{
	            try {
					if(conn != null && !conn.isClosed()){
					    System.out.println("Closing Database Connection");
					    conn.close();
					}
				} catch (SQLException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
	            if(session !=null && session.isConnected()){
	                System.out.println("Closing SSH Connection");
	                session.disconnect();
	            }
	        }

	        
	}
}