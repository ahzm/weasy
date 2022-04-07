package fr.inria.convecs.rbpmn.main;

import java.util.ArrayList;

import fr.inria.convecs.rbpmn.calcul.CalculResourcesUsageByTasks;
import fr.inria.convecs.rbpmn.common.*;
import fr.inria.convecs.rbpmn.deploy.*;
import fr.inria.convecs.rbpmn.multithreads.ExecuteRuntimeTasks;
import fr.inria.convecs.rbpmn.visualisation.CreateChart;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class MainExecute {
	
	private static final Logger logger = LoggerFactory.getLogger(MainExecute.class);

	public static void main(String[] agrs) {

//		logger.warn("This is warn message.");
//		logger.info("This is info message.");
//		logger.error("This is error message.");

		String processID = "SchedulingEx01";
		String processName = "SchedulingEx01";

		BPMNController bpmn = new BPMNController(processID, processName);
		bpmn.bpmnDeployment();
//		
		bpmn.generateInstances(2);

		ArrayList<Resource> initResources = new ArrayList<>();
		initResources.add(new Resource("res01", "humain", 2));
		initResources.add(new Resource("res02", "drone", 3));

		BPMNResources allResources = new BPMNResources(initResources);
		//System.out.println(allResources);
		ExecuteRuntimeTasks executeTask = new ExecuteRuntimeTasks(bpmn.getBpmnProcess(), allResources);
		
		
		CreateChart createChart = new CreateChart(bpmn.getBpmnProcess());
		createChart.showAETChart();
		createChart.showNbrDuplicaResChart(initResources);
		createChart.showResPercentChart(initResources);
		
		int nbrOfInstance = 0;
		while(true) {
			
		executeTask.executeTasks(bpmn);
		
//		nbrOfInstance = 1 + (int)(Math.random()*(10-2)); 
//		bpmn.generateInstances(nbrOfInstance);
		}

	}
}
