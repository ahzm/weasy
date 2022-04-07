package fr.inria.conves.rbpmn.bpmntask;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

import org.activiti.engine.ProcessEngine;
import org.activiti.engine.ProcessEngines;
import org.activiti.engine.TaskService;

import fr.inria.convecs.rbpmn.common.BPMNResources;
import fr.inria.convecs.rbpmn.common.Resource;

public class TaskController {
	
	@Override
	public String toString() {
		return "TaskController [resources=" + resources + ", task]";
	}

	private BPMNResources resources;
	//private BPMNTask task;
	
	public TaskController(BPMNResources resources) {
		this.resources = resources;
	}
	
	
public synchronized void takeResource(BPMNTask task) {
		
		boolean flag = false;
		
		Map<String, Integer> taskResources = new ConcurrentHashMap<String, Integer>();
		taskResources.putAll(task.getTaskResources());
		
		for(String taskResKey: taskResources.keySet()) {
			for(Resource res: resources.getAllResource()) {
				if(res.getId().equals(taskResKey)) {
					int currentResource = res.getNumber();
					int requiredResource = taskResources.get(taskResKey);
					if(currentResource <= requiredResource) {
						flag = true;
					}
				}
			}
		}
		
		while (flag) {
			try {
				System.out.println("\u001b[33m Warnning: Task ID: " + task.getTask().getId() + " is waitting \u001b[0m");
				
				this.wait();
				// Thread.sleep(2000);

				List<Boolean> list_flag = new CopyOnWriteArrayList<>();
				
				for (String taskResKey: taskResources.keySet()) {
					for(Resource res: resources.getAllResource()) {
						if(res.getId().equals(taskResKey)) {
							int currentResource = res.getNumber();
							int requiredResource = taskResources.get(taskResKey);
							if(currentResource >= requiredResource) {
								list_flag.add(false);
							}else {
								list_flag.add(true);
							}
						}
					}
					
				}

				if (list_flag.contains(true)) {
					flag = true;
				} else {
					flag = false;
				}

			} catch (InterruptedException e) {
				e.printStackTrace();

				//System.out.println("flag");
			}
		}
		
		try {
			Thread.sleep(10);
		} catch (InterruptedException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
		
		for(String taskResKey: taskResources.keySet()) {
			for(Resource res: resources.getAllResource()) {
				
				if(res.getId().equals(taskResKey)) {
					System.out.println("\u001b[36;1m Current Resources : Key:" + taskResKey + ", value:" + res.getNumber()
					+ "\u001b[0m");
					int currentResource = res.getNumber();
					int requiredResource = taskResources.get(taskResKey);
					res.setNumber(currentResource - requiredResource);
					System.out.println("\u001b[31m " + task.getTask().getId() + " After assigning Resources -: Key:" + taskResKey
							+ ",value:" + res.getNumber() + "\u001b[0m");
				}
				
			}
		}
		
		this.notifyAll();
			
		}
	
	public void executeCourrentTask(BPMNTask task) {

		ProcessEngine engine = ProcessEngines.getDefaultProcessEngine();
		TaskService taskService = engine.getTaskService();
		try {
			Thread.sleep(10);
			System.out.println("\u001b[35;1m" + task.getId() + " Executing duration:" + task.getDuration() + "\u001b[0m");
			Thread.sleep(task.getDuration() * 1000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		
		if (Math.random() > 0.8) {
			try {
				Thread.sleep(10);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		} 

		synchronized(this) {
			taskService.complete(task.getId());
		}
		
		System.out.println("----------------------");

	}
	
	public synchronized void putResource(BPMNTask task) {
		
		for(String taskResKey: task.getTaskResources().keySet()) {
			for(Resource res: resources.getAllResource()) {
				
				if(res.getId().equals(taskResKey)) {
					System.out.println("\u001b[36;1m Current Resources : Key:" + taskResKey + ",value:" + res.getNumber()
					+ "\u001b[0m");
					int currentResource = res.getNumber();
					int requiredResource = task.getTaskResources().get(taskResKey);
					res.setNumber(currentResource + requiredResource);
					System.out.println("\u001b[31m " + task.getTask().getId() + " Release resources -: Key:" + taskResKey
							+ ",value:" + res.getNumber() + "\u001b[0m");
				}
				
			}
		}
		this.notifyAll();
	}
}
