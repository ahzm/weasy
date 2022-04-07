package fr.inria.convecs.rbpmn.deploy;

import java.util.Map;

public class BPMNController {
	private BPMNProcess bpmnProcess;
	private DeploymentProcess dp;
	private CreateInstances instances;
	
	public BPMNController(String processId, String processName){
		this.bpmnProcess = new BPMNProcess(processId, processName);
		this.dp = new DeploymentProcess(this.bpmnProcess);
		this.instances = new CreateInstances(this.bpmnProcess);
	}
	
	public BPMNProcess getBpmnProcess() {
		return bpmnProcess;
	}

	public void setBpmnProcess(BPMNProcess bpmnProcess) {
		this.bpmnProcess = bpmnProcess;
	}

	public void bpmnDeployment() {
		this.dp.Deployment();
	}
	public boolean generateInstances(int nbrInstance) {
		this.instances.generateInstances(nbrInstance);
		return true;
	}
	
	public boolean generateInstance(int nbrInstance, Map<String, Object> bpmnVariables) {
		this.instances.generateInstances(nbrInstance, bpmnVariables);
		return true;
	}
}
