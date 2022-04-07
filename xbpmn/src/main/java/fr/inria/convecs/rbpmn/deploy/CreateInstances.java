package fr.inria.convecs.rbpmn.deploy;

import java.util.HashMap;
import java.util.Map;

import org.activiti.engine.ProcessEngine;
import org.activiti.engine.ProcessEngines;
import org.activiti.engine.RuntimeService;
import org.activiti.engine.runtime.ProcessInstance;

public class CreateInstances {
	
	private BPMNProcess process;
	
	public CreateInstances(BPMNProcess process) {
		this.process = process;
	}
	
	public void generateInstances(int nbraInstance) {
		ProcessEngine engine = ProcessEngines.getDefaultProcessEngine();
		RuntimeService runtimeService = engine.getRuntimeService();

		String key = this.process.getProcessId();

		for (int i = 1; i <= nbraInstance; i++) {

//			System.out.println(i);

			//ProcessInstance processInstance = 
			runtimeService.startProcessInstanceByKey(key);

//			System.out.println("Process de finition ID：" + processInstance.getProcessDefinitionId());
//			System.out.println("Process Instance ID：" + processInstance.getId());
		}
	}
	
	public void generateInstances(int nbrInstance, Map<String, Object> bpmnVariables) {

		ProcessEngine engine = ProcessEngines.getDefaultProcessEngine();
		RuntimeService runtimeService = engine.getRuntimeService();

		Map<String, Object> variables = new HashMap<>();
		variables.putAll(bpmnVariables);

		String key = process.getProcessId();

		for (int i = 1; i <= nbrInstance; i++) {

			System.out.println("-" + i + "-:");

			ProcessInstance processInstance = runtimeService.startProcessInstanceByKey(key, variables);

			System.out.println("Process de finition ID：" + processInstance.getProcessDefinitionId());
			System.out.println("Process Instance ID：" + processInstance.getId());
		}
	}
}
