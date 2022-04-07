package fr.inria.convecs.rbpmn.deploy;

public class BPMNProcess {
	private String processId;
	private String bpmnName;
	
	
	public BPMNProcess(String processId, String bpmnName) {
		super();
		this.processId = processId;
		this.bpmnName = bpmnName;
	}
	public String getProcessId() {
		return processId;
	}
	public void setProcessId(String processId) {
		this.processId = processId;
	}
	
	public String getBpmnName() {
		return bpmnName;
	}
	
	public void setBpmnName(String bpmnName) {
		this.bpmnName = bpmnName;
	}
	
	@Override
	public String toString() {
		return "Process [processId=" + processId + ", bpmnName=" + bpmnName + "]";
	}
	
	
}
