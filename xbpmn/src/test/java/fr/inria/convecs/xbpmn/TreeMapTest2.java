package fr.inria.convecs.xbpmn;

import java.util.ArrayList;
import java.util.Date;
import java.util.TreeMap;

public class TreeMapTest2 {
	
	public static void main(String[] args) {
		TreeMap<Date, Integer> traces = new TreeMap<>();
		traces.put(new Date(), 5);
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		traces.put(new Date(), 6);
		
		System.out.println(traces);
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		traces.put(new Date(), 0);
		ArrayList<Date> traceKeys = new ArrayList<>(); 
		ArrayList<Integer> traceValues = new ArrayList<>(); 
		
		traceKeys.addAll(traces.keySet());
		traceValues.addAll(traces.values());
		System.out.println("key:");
		System.out.println(traceKeys);
		System.out.println(traceValues);
		Long currentTime = traceKeys.get(0).getTime();
		
		Long duration = 0L;
		for(int i = 1; i < traceKeys.size(); i++) {
			Long tempTime = traceKeys.get(i).getTime();
			
			System.out.println("+++++++");
			System.out.println((tempTime - currentTime));
			System.out.println((tempTime - currentTime) * traceValues.get(i - 1));
			duration += (tempTime - currentTime) * traceValues.get(i - 1);
			
			currentTime = tempTime;
		}
		
		System.out.println("duration:" + duration);
		
		
	}
}
