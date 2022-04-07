package fr.inria.convecs.rbpmn.common;

public class MVCPatternDemo {
	
	   public static void main(String[] args) {
	 
	      //从数据库获取学生记录
		   Resource model  = retrieveStudentFromDatabase();
	 
	      //创建一个视图：把学生详细信息输出到控制台
		   ResourceView view = new ResourceView();
	 
	      ResourceController controller = new ResourceController(model, view);
	 
	      controller.updateView();
	 
	      //更新模型数据
	      controller.setResourceId("John");
	 
	      controller.updateView();
	   }
	 
	   private static Resource retrieveStudentFromDatabase(){
		  Resource student = new Resource("Robert", 10);
	      return student;
	   }
	}