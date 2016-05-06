

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;

/**
 * Servlet implementation class companyDetails
 */
@WebServlet("/companyDetails")
public class companyDetails extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public companyDetails() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		PrintWriter pw = response.getWriter();
		response.setContentType("text/html");
		// TODO Auto-generated method stub
		System.out.println("asjfdkaslfd");
		String cName = request.getParameter("cName");
		int year = Integer.parseInt(request.getParameter("year"));
		int quarter = Integer.parseInt(request.getParameter("quarter"));
		String anti_flag = request.getParameter("anti_rule");
		String flag_rule = request.getParameter("flag_rule");
		String highlight = request.getParameter("highlight");
		String values = request.getParameter("values").substring(1);
		String[] parameters = values.split(",");
//		Connection conn = new Test().getConn();
		HashMap<Integer, String> filter_id_name = new HashMap<Integer, String>();
		HashMap<Integer,ArrayList<Integer>> filter_rules = new HashMap<Integer, ArrayList<Integer>>();
		HashMap<Integer, HashMap<Integer, String>> footNotes_rule_data  = new HashMap<Integer, HashMap<Integer,String>>();
		HashMap<Integer, HashMap<Integer, String>> mainDoc_rule_data  = new HashMap<Integer, HashMap<Integer,String>>();
//		
		mysqlConnection mC = new mysqlConnection();
		Connection conn = mC.getConnection();
		try {
			PreparedStatement stmt = conn.prepareStatement("select file_id from files_info where c_id in (select c_id from companies where c_name = ?) and year = ? and quarter = ?");
			stmt.setString(1,cName);
			stmt.setInt(2, year);
			ArrayList<Integer> f_ids = new ArrayList<Integer>();
			stmt.setInt(3, quarter);
			ResultSet rs = stmt.executeQuery();
			System.out.println("rs: "+rs);
			int file_id = 0;
			if(rs.next())
			{
				file_id = Integer.parseInt(rs.getString(1));
				System.out.println("file id: "+file_id);
			}
			else
			{
				System.out.println("Not present");
			}
			
			for(String filterName : parameters)
			{
				stmt = conn.prepareStatement("select f_id from filters where f_name = ?");
				stmt.setString(1,filterName);
				rs = stmt.executeQuery();
				while(rs.next())
				{
					int f_id = rs.getInt(1);
					f_ids.add(f_id);
					filter_id_name.put(f_id, filterName);
				}
			}
			
			String r_ids = "";
			for(int f_id : f_ids)
			{
				System.out.println("fid = " + f_id);
				stmt = conn.prepareStatement("select r_ids from filter_rules where f_id = ?");
				stmt.setInt(1, f_id);
				rs = stmt.executeQuery();
				while(rs.next())
				{
					String r_id_str = rs.getString(1);
					r_ids = r_ids + "," + r_id_str;
					System.out.println("rid here: " + r_id_str);
				}
				r_ids = r_ids.substring(1);
				//System.out.println("r_ids = " + r_ids);
				String[] r_array = r_ids.split(",");
				ArrayList<Integer> rid_list = new ArrayList<Integer>();
				for(String r_id : r_array)
				{
					if(r_id != null){
						System.out.println("r_id = " + r_id);
						rid_list.add(Integer.parseInt(r_id));
					}
				}
				filter_rules.put(f_id, rid_list);
				
			}
			HashSet<Integer> rid_set = new HashSet<Integer>();
			//r_ids = r_ids.substring(1);
			String[] r_array = r_ids.split(",");
			for(String r_id : r_array)
			{
				System.out.print("rid = " + r_id);
				if(r_id != null && r_id != "")
					rid_set.add(Integer.parseInt(r_id));
			}
			
			ArrayList<Integer> flag_rids = new ArrayList<Integer>();
			for(int r_id : rid_set)
			{
				stmt = conn.prepareStatement("select r_id from rules where is_flag= 1 and r_id = ?");
				stmt.setInt(1,r_id);
				
				rs = stmt.executeQuery();
				while(rs.next())
				{
					flag_rids.add(rs.getInt(1));
				}
			}
			
			System.out.println();
			for(int r_id : rid_set)
			{
				PreparedStatement stmt1 = conn.prepareStatement("select start, end from offsets where file_id = ?");
				//stmt1.setInt(1, r_id);
				stmt1.setInt(1, file_id);
				ResultSet rs2 = stmt1.executeQuery();
				int start = 0;
				int end = 0;
				while(rs2.next())
				{
					start = rs2.getInt(1);
					
					end = rs2.getInt(2);
				}
				System.out.println("start :" + start);
				System.out.println("end :" + end);
				stmt = conn.prepareStatement("select offset, value from rule_data where r_id = ? and file_id = ?");
				stmt.setInt(1,r_id);
				stmt.setInt(2, file_id);
				rs = stmt.executeQuery();
				while(rs.next())
				{
					int offset = rs.getInt(1);
					String value = rs.getString(2);
					if( start<offset && end > offset)
					{
						HashMap<Integer, String> temp = footNotes_rule_data.get(r_id);
						if(temp == null)
						{
							temp = new HashMap<Integer,String>();
													
						}
						temp.put(offset, value);
						footNotes_rule_data.put(r_id, temp);
					}
					else
					{
						HashMap<Integer, String> temp = mainDoc_rule_data.get(r_id);
						if(temp == null)
						{
							temp = new HashMap<Integer,String>();
													
						}
						temp.put(offset, value);
						mainDoc_rule_data.put(r_id, temp);
					}
						
				}
				System.out.println("footnotessss :" + footNotes_rule_data);
				System.out.println("footnotessss :" + mainDoc_rule_data);
				
				
				
			}
			conn.close();
			
			
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
//		mysqlConnection mC = new mysqlConnection();
//		Connection conn = mC.getConnection();
//		try {
//			PreparedStatement preparedStatement = conn.prepareStatement("select ");
//		} catch (SQLException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
		
		pw.println("<html><head>");
		pw.println("<link href='" + request.getContextPath() +"/dist/css/vendor/bootstrap/css/bootstrap.min.css' rel='stylesheet'><link href='" + request.getContextPath() +"/dist/css/flat-ui.css' rel='stylesheet'><link href='" + request.getContextPath() +"/docs/assets/css/demo.css' rel='stylesheet'>");
		pw.println("<h2 demo-section-title><center>Results - SEC Footnotes</center></h2></head></html>");
		pw.println("<body>");
		
		if(highlight.equalsIgnoreCase("on")){
			pw.println("<h3 demo-panel-title><center>Validated Rules Hits<center></h3>");
			pw.println("<table class='table table-striped' align = center><tr>");
			pw.println("<td><ul><li>Filter</li><li>Offset, Footnote Data</li></ul></td>");
			pw.println("<td><ul><li>Filter</li><li>Offset, Main Document Data</li></ul></td>");
			pw.println("</tr>");
			
			for(Map.Entry<Integer, String> entry : filter_id_name.entrySet()){
				//pw.println("<tr>");				
				int id = entry.getKey();
				String name = entry.getValue();
				System.out.println("Name is: " + name);
				System.out.println("Values is: " + values);
				
				//for(Map.Entry<Integer, ArrayList<Integer>> entry2 : filter_rules.entrySet()){
				ArrayList<Integer> ruleList = filter_rules.get(id);
				if(ruleList != null){
					
					for(int rid : ruleList){
						//pw.println("<tr><td>");
					//for(Map.Entry<Integer, HashMap<Integer, String>> entry3 : footNotes_rule_data.entrySet()){
						//System.out.println("rid = "+rid);
						//System.out.println("footnote : "+mainDoc_rule_data);
						HashMap<Integer, String> off_data_map = footNotes_rule_data.get(rid);
						HashMap<Integer, String> off_data_map2 = mainDoc_rule_data.get(rid);
						System.out.println("Hashmap" + off_data_map);
						if(off_data_map != null && off_data_map2 != null){
							pw.println("<tr><td>");
							pw.println("<ul>");

							for(Map.Entry<Integer, String> entry4 : off_data_map.entrySet()){
								int off = entry4.getKey();
								String data = entry4.getValue();
								System.out.println("off = "+off);
								System.out.println("data" + data);
								pw.println("<li>" + name + "</li><li>" + off +", " + data + "</li>");
							}
							pw.println("</ul></td>");
							
							pw.println("<td><ul>");
							for(Map.Entry<Integer, String> entry4_2 : off_data_map2.entrySet()){
								int off = entry4_2.getKey();
								String data = entry4_2.getValue();
								pw.println("<li>" + name + "</li><li>" + off +", " + data + "</li>");
							}	
							pw.println("</ul><td></tr>");
							

						}
						else{							
							//pw.println("<tr><td><ul></ul></td></tr>");
						}
						//pw.println("</td><td>");
						/*HashMap<Integer, String> off_data_map2 = mainDoc_rule_data.get(rid);						
						if(off_data_map2 != null){
							pw.println("<td><ul>");
							for(Map.Entry<Integer, String> entry4_2 : off_data_map2.entrySet()){
								int off = entry4_2.getKey();
								String data = entry4_2.getValue();
								pw.println("<li>" + name + "</li><li>" + off +", " + data + "</li>");
							}	
							pw.println("</ul><td>");

						}
						else{							
							pw.println("<td><ul></ul></td>");
						}*/
						//pw.println("</tr>");
					}
					//pw.println("</td>");
				}
				//pw.println("</tr>");
				
			}
			
			
			//pw.println("</tr>");
			pw.println("</table>");
			
		}
		if(anti_flag.equalsIgnoreCase("on")){
			
			pw.println("<table border = 10 align = center><tr>");
			pw.println("<td><ul><li>Filter</li><li>Offset, Offset Data</li></ul></td>");
			pw.println("<td><ul><li>Filter</li><li>Offset, Negated Data</li></ul></td>");
			pw.println("</tr>");
			
			for(Map.Entry<Integer, String> entry : filter_id_name.entrySet()){
				pw.println("<tr>");				
				int id = entry.getKey();
				String name = entry.getValue();
				System.out.println("id = " + id);
				System.out.println("name = "+name);
				//for(Map.Entry<Integer, ArrayList<Integer>> entry2 : filter_rules.entrySet()){
				ArrayList<Integer> ruleList = filter_rules.get(id);
				if(ruleList != null){
					for(int rid : ruleList){						
					//for(Map.Entry<Integer, HashMap<Integer, String>> entry3 : footNotes_rule_data.entrySet()){
						System.out.println("rid = "+rid);
						System.out.println("footnote : "+mainDoc_rule_data);
						HashMap<Integer, String> off_data_map = footNotes_rule_data.get(rid);
						System.out.println("Hashmap" + off_data_map);
						if(off_data_map != null){							
							for(Map.Entry<Integer, String> entry4 : off_data_map.entrySet()){
								int off = entry4.getKey();
								String data = entry4.getValue();
								System.out.println("off = "+off);
								System.out.println("data" + data);
								pw.println("<td><ul><li>" + name + "</li><li>" + off +", " + data + "</li></ul></td>");
							}							
						}
						else{							
							pw.println("<td></td>");
						}
						HashMap<Integer, String> off_data_map2 = mainDoc_rule_data.get(rid);
						if(off_data_map2 != null){						
							for(Map.Entry<Integer, String> entry4_2 : off_data_map.entrySet()){
								int off = entry4_2.getKey();
								String data = entry4_2.getValue();
								pw.println("<td><ul><li>" + name + "</li><li>" + off +", " + data + "</li></ul></td>");
							}							
						}
						else{							
							pw.println("<td></td>");
						}
						
					}
				}
				pw.println("</tr>");
				
			}
			
			
			//pw.println("</tr>");
			pw.println("</table>");
		}
		if(flag_rule.equals("on")){
			pw.println("<table border = 10 align = center><tr><td>Offset, Flagged Data</td>");
			
			pw.println("</tr></table>");
		}
		
		
		pw.println("</body>");
		pw.println("</html>");
		
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);
	}

}
