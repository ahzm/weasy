package fr.inria.convecs.rbpmn.common;

public class ResourceController {
	private Resource resource;
	private ResourceView view;

	public ResourceController(Resource resource, ResourceView view) {

		this.resource = resource;
		this.view = view;

	}

	public void setResourceName(String name) {
		resource.setName(name);
	}

	public String getResourceName() {
		return resource.getName();
	}

	public void setResourceId(String resourceId) {
		resource.setId(resourceId);
	}

	public String getResourceID() {
		return resource.getId();
	}
	
	public synchronized boolean addResource() {
		
		int addNumber = resource.getNumber() + 1;
		resource.setNumber(addNumber);
		return true;
	}
	
	public synchronized boolean reduceResource() {
		
		int currentNbr = resource.getNumber();
		
		if (currentNbr - 1 > 1) {
			currentNbr -= 1;
			resource.setNumber(currentNbr);
			return true;
		}
		return false;	
	}
	

	public void updateView() {
		view.printResourceDetails(resource.getId(), resource.getNumber());
	}
}
