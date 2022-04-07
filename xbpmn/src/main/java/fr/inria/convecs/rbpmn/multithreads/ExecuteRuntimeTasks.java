package fr.inria.convecs.rbpmn.multithreads;

import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import org.activiti.engine.ProcessEngine;
import org.activiti.engine.ProcessEngines;
import org.activiti.engine.TaskService;
import org.activiti.engine.task.Task;

import fr.inria.convecs.rbpmn.calcul.CalculResourcesUsageByTasks;
import fr.inria.convecs.rbpmn.common.*;
import fr.inria.convecs.rbpmn.deploy.*;
import fr.inria.conves.rbpmn.bpmntask.BPMNTask;
import fr.inria.conves.rbpmn.bpmntask.TaskController;

public class ExecuteRuntimeTasks {

	private BPMNProcess process;
	private BPMNResources resources;
	private int nbrThreadPool;

	public ExecuteRuntimeTasks(BPMNProcess process, BPMNResources resources) {
		this.process = process;
		this.resources = resources;
		this.nbrThreadPool = 10;

	}

	public ExecuteRuntimeTasks(BPMNProcess process, BPMNResources resources, int nbrThreadPool) {
		this.process = process;
		this.resources = resources;
		this.nbrThreadPool = nbrThreadPool;
	}

	public void executeTasks(BPMNController bpmn) {
		
		ExecutorService es = Executors.newFixedThreadPool(this.nbrThreadPool);

		ProcessEngine engine = ProcessEngines.getDefaultProcessEngine();
		TaskService taskService = engine.getTaskService();

		List<Task> tasks = taskService.createTaskQuery().processDefinitionKey(this.process.getProcessId()).list();

		CalculResourcesUsageByTasks crs = new CalculResourcesUsageByTasks(this.process, this.resources);
		
		TaskController taskController = new TaskController(this.resources);
		
		System.out.println("tasks size:" + tasks.size());
		
		CalculResourcesUsageByTasks usageRes = new CalculResourcesUsageByTasks(this.process);
		
		if(tasks.size() == 0) {
			bpmn.generateInstances(5);
		}
		
		do {

			CountDownLatch endGate = new CountDownLatch(tasks.size());
			
			int nbrOfInstance = 0;
			if(Math.random() < 0.3) {
				nbrOfInstance = 1 + (int)(Math.random()*(10-2)); 
				//bpmn.generateInstances(nbrOfInstance);
			}
			
			
			for (Task task : tasks) {
				if (nbrOfInstance > 0) {
					bpmn.generateInstances(1);
					nbrOfInstance--;
				}
				BPMNTask bpmnTask = new BPMNTask(task);
				
				bpmnTask.storeTaskInfos();
				
				System.out.println("Resources:" + this.resources);
				
				Runnable run = new Runnable() {

					@Override
					public void run() {
						// TODO Auto-generated method stub
						try {
							long start = System.currentTimeMillis();
							System.out.println("Task: " + bpmnTask.getId() + ", is executing.");

							taskController.takeResource(bpmnTask);
							taskController.executeCourrentTask(bpmnTask);
							long end = System.currentTimeMillis();

							taskController.putResource(bpmnTask);

							System.out.println("\u001b[35;1m --- " + bpmnTask.getId() + " End ---\u001b[0m");
							System.out.println("|* Id: " + task.getId() + ", Execution time:"
									+ Long.toString(end - start) + " *|");
							crs.calculTotalRes();
							//crs.calculTotalRes(1);
							
							
							for(Resource resource : resources.getAllResource()) {
								Long duation = resource.getDuration(2);
								double result = 0.0;
								if (usageRes.calculTotalRes().containsKey(resource.getId())) {
									result = usageRes.calculTotalRes(2).get(resource.getId()).doubleValue() * 1000 / duation.doubleValue();
									System.out.println("NbrDuplica:" +  resource.getNbrDuplica() + ", result:" +  result);
									System.out.println();
//									if(result > 0.7) {
//										resource.addResource();
//									}else if(result < 0.5) {
//										resource.reduceResource();
//									}
								}
							}
							
						} catch (Exception e) {
							
							e.printStackTrace();
							
						} finally {
							
							endGate.countDown();
						}
					}

					// System.out.println(taskController);
				};
				
				es.submit(run);
				tasks = taskService.createTaskQuery().processDefinitionKey(this.process.getProcessId()).list();

			}

			try {
				endGate.await();
			} catch (InterruptedException e) {

				e.printStackTrace();
			}
			
		tasks = taskService.createTaskQuery().processDefinitionKey(this.process.getProcessId()).list();
		
		} while (!tasks.isEmpty());
		es.shutdown();
	}

}
