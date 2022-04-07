package fr.inria.convecs.rbpmn.deploy;

import org.activiti.engine.ProcessEngine;
import org.activiti.engine.ProcessEngines;
import org.activiti.engine.RepositoryService;
import org.activiti.engine.repository.Deployment;

public class DeploymentProcess {
	
	private BPMNProcess process;
	
	public DeploymentProcess(BPMNProcess process) {
		super();
		this.process = process;
		//this.Deployment();
	}
	
	public void Deployment() {
		
		System.out.println("Deployment: " + this.process.getBpmnName() + ".bpmn; ID: " + this.process.getProcessId());

		ProcessEngine engine = ProcessEngines.getDefaultProcessEngine();
		RepositoryService service = engine.getRepositoryService();
		Deployment deploy = service.createDeployment().addClasspathResource("BPMN/" + this.process.getBpmnName() + ".bpmn")
				.name(this.process.getProcessId()).deploy();
		System.out.println(" -- Deployment Success -- ");
		System.out.println("Process Id: " + deploy.getId() + "; Process Name: " + deploy.getName());
	}
	
	
	@Override
	public String toString() {
		return "DeploymentProcess [processID=" + this.process.getProcessId() + ", processName=" + this.process.getBpmnName() + "]";
	}
	
	
}
