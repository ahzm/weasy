package fr.inria.convecs.rbpmn.common;

import java.util.ArrayList;
import java.util.Date;
import java.util.TreeMap;

public class Resource {
	
	private String id;
	private String name;
	private int number;
	private int nbrDuplica;
	private TreeMap<Date, Integer> usageTraces;
	private Long duration;
	private Date addReduceTimestamps;
	//private Date reduceTimestamps;
	private int controleDuration;
	
	
	public Resource(String id, int number) {
		this.id = id;
		this.number = number;
		this.nbrDuplica = number;
		this.duration = 0L;
		
		this.addReduceTimestamps = new Date();
		//this.reduceTimestamps = new Date();
		this.controleDuration = 1;
		
		usageTraces = new TreeMap<>();
		usageTraces.put(new Date(), number);
	}
	
	public Resource(String id, String name, int number) {
		this.id = id;
		this.name = name;
		this.number = number;
		this.duration = 0L;
		this.nbrDuplica = number;
		
		this.addReduceTimestamps = new Date();
		//this.reduceTimestamps = new Date();
		this.controleDuration = 1;
		
		
		usageTraces = new TreeMap<>();
		usageTraces.put(new Date(), number);
	}
	
	
	public TreeMap<Date, Integer> getUsageTrace(){
		return this.usageTraces;
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public int getNumber() {
		return number;
	}

	public void setNumber(int number) {
		this.number = number;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
	
	
	public synchronized boolean addResource() {
		
		if(this.controleLimite()) {
			int addNumber = this.getNumber() + 1;
			this.setNumber(addNumber);
			this.setNbrDuplica(this.nbrDuplica + 1);
			usageTraces.put(new Date(), this.nbrDuplica);
			
			this.addReduceTimestamps = new Date();
			return true;
		}else {
			return false;
		}
		
	}
	
	public synchronized boolean reduceResource() {
		
		if(this.controleLimite()) {
			int currentNbr = this.getNumber();
			
			if (currentNbr - 1 > 0) {
				currentNbr -= 1;
				this.setNumber(currentNbr);
				this.setNbrDuplica(this.getNbrDuplica() - 1);
				usageTraces.put(new Date(), this.getNbrDuplica());
				
				this.addReduceTimestamps = new Date();
				return true;
			}
			return false;	
		}else {
			return false;
		}
		
	}

	@Override
	public String toString() {
		return "Resource [id=" + id + ", name=" + name + ", number=" + number + "]";
	}
	
	
	public Long getDuration() {
		return calculResourceUsage();
	}
	
	public Long getDuration(int minutes) {
		return calculResourceUsage(minutes);
	}

	private Long calculResourceUsage() {
		TreeMap<Date, Integer> traces = new TreeMap<>();
		traces.putAll(this.getUsageTrace());
		
		//Long duration = 0L;
		
		if(traces.size() == 1) {
			
			Long endtime = new Date().getTime();
			Long firstTime = traces.firstKey().getTime();
			
			Integer number = traces.firstEntry().getValue();
			duration = (endtime - firstTime) * number;
			
			System.out.println("duration:" + duration);
			
		}else {
			
			duration = 0L;
			Date temp = new Date();
			traces.put(new Date(), 0);
			ArrayList<Date> traceKeys = new ArrayList<>(); 
			ArrayList<Integer> traceValues = new ArrayList<>();
			
			for(Date tracekey : traces.keySet()) {
//				if (tracekey.getTime() > this.addReduceTimestamps.getTime()) {
					traceKeys.addAll(traces.keySet());
					traceValues.addAll(traces.values());
//				}
			}
			
			
			Long currentTime = traceKeys.get(0).getTime();
			
			for(int i = 1; i < traceKeys.size() ; i++) {
				Long tempTime = traceKeys.get(i).getTime();
				
				duration += (tempTime - currentTime) * traceValues.get(i - 1);
				
				currentTime = tempTime;
			}
			traces.remove(temp);
		}
		
		
		System.out.println("*******:" + duration);
		
		return duration;
		
	}
	
	
	private Long calculResourceUsage(int minutes) {
		TreeMap<Date, Integer> traces = new TreeMap<>();
		traces.putAll(this.getUsageTrace());
		
		//Long duration = 0L;
		
		if(traces.size() == 1) {
			
			Long endtime = new Date().getTime();
			Long firstTime = traces.firstKey().getTime();
			
			Integer number = traces.firstEntry().getValue();
			
			duration = (endtime - firstTime) * number;
			
			Long duration_temp = minutes * 60000L * number;
			
			if(duration < duration_temp) {
				System.out.println("duration:" + duration);
				return duration;
			}else {
				return duration_temp;
			}
			
			
		}else {
			
			duration = 0L;
			Date temp = new Date();
			
			traces.put(temp, 0);
			Long condition = temp.getTime() - minutes * 60000L;
			
			ArrayList<Date> traceKeys = new ArrayList<>(); 
			ArrayList<Integer> traceValues = new ArrayList<>();
			
			//Date tempDate = new Date();
			int tempValue = 0;
			for(Date tracekey : traces.keySet()) {
				if (tracekey.getTime() < condition) {
					//tempDate = tracekey;
					tempValue = traces.get(tracekey);
					
				}else{
					break;
				}
			}
			if(tempValue != 0) {
				traceKeys.add(new Date(condition));
				traceValues.add(tempValue);
			}
			
			
			for(Date tracekey : traces.keySet()) {
				if (tracekey.getTime() >= condition) {
					traceKeys.add(tracekey);
					traceValues.add(traces.get(tracekey));
				}
			}
			
			
			
			Long currentTime = traceKeys.get(0).getTime();
			
			Long realDuration = 0L;
			
			for(int i = 1; i < traceKeys.size() ; i++) {
				Long tempTime = traceKeys.get(i).getTime();
				
				duration += (tempTime - currentTime) * traceValues.get(i - 1);
				realDuration += (tempTime - currentTime);
				
				currentTime = tempTime;
			}
			traces.remove(temp);
			
			System.out.println("+++++++++++++++++++++++++++++realDuration: " + realDuration);
			return duration;
		}
		
		//System.out.println("*******:" + duration);
		
		//return duration;
		
	}
	
	private boolean controleLimite() {
		Long limiteTime = this.controleDuration * 60000L;
		if((new Date().getTime() - this.addReduceTimestamps.getTime())>= limiteTime) {
			return true;
		}else {
			return false;
		}
		
	}
	
	private boolean controleLimite(int minutes) {
		Long limiteTime = this.controleDuration * minutes * 60000L;
		if((new Date().getTime() - this.addReduceTimestamps.getTime())>= limiteTime) {
			return true;
		}else {
			return false;
		}
		
	}

	public int getNbrDuplica() {
		return nbrDuplica;
	}

	public void setNbrDuplica(int nbrDuplica) {
		this.nbrDuplica = nbrDuplica;
	}

}
