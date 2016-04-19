import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;


public class mysqlConnection {

	public Connection getConnection() 
	{
		int lport=5656;
        String rhost="152.1.26.121";
        String host="152.1.26.121";
        int rport=3306;
        String user="";
        String password="";
        String dbuserName = "";
        String dbpassword = "";
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
	            
	            return conn;
	            
	        }catch(Exception e){
	            e.printStackTrace();
	        }
	        return conn;
	}
}
