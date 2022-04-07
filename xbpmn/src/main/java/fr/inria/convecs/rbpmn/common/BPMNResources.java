package fr.inria.convecs.rbpmn.common;

import java.util.ArrayList;

public class BPMNResources {
	
	private ArrayList<Resource> resources;
	
	public BPMNResources(ArrayList<Resource> resources) {
		this.resources = new ArrayList<>();
		this.resources.addAll(resources);	
	}
	
	public ArrayList<Resource> getAllResource() {
		return resources;
	}

	@Override
	public String toString() {
		return "ModelResources [resources=" + resources + "]";
	}
	
}
