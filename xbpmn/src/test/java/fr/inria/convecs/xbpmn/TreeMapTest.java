package fr.inria.convecs.xbpmn;

import java.util.ArrayList;
import java.util.Date;
import java.util.Map;
import java.util.TreeMap;

public class TreeMapTest {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		TreeMap<Date, Integer> testTreeMap = new TreeMap<Date, Integer>();
		for(int i =0; i < 9; i++) {
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			testTreeMap.put(new Date(), i);
		}
		
		
//		Long tempdate =  testTreeMap.lastKey().getTime();
//		Integer  tempInteger = testTreeMap.get(tempdate);
//		testTreeMap.put(new Date().getTime() + 1000L, tempInteger);
//		
		System.out.println(testTreeMap.size());
		System.out.println("First:" + testTreeMap.firstKey());
		System.out.println("Last:" + testTreeMap.lastKey());
//		System.out.println(testTreeMap.lastKey() - testTreeMap.firstKey());
		
//		ArrayList<Long> arrayList = new ArrayList<>(); 
//		ArrayList<Integer> arrayList1 = new ArrayList<>(); 
//		ArrayList<Long> arrayList2 = new ArrayList<>(); 
//		
//		arrayList.addAll(testTreeMap.keySet());
//		arrayList1.addAll(testTreeMap.values());
//		
//		Long current = arrayList.get(0);
//		Long temp = 0L;
//		
//		for(int i = 1; i< arrayList.size(); i ++) {
//			temp = arrayList.get(i) - current;
//			current = arrayList.get(i);
//			System.out.println(temp);
//			
//			arrayList2.add(temp);
//		}
//		
//		System.out.println(arrayList);
//		System.out.println(arrayList1);
//		System.out.println(arrayList2);
//		System.out.println(arrayList1.subList(0, arrayList1.size() -1));
//		for(Long date : testTreeMap.keySet())
//			System.out.println(date);
		
//		System.out.println(getResourceUsage(testTreeMap));
		
		
//		Date date = new Date();
//		Date date1 = new Date();
//		if(date1.getTime() > date.getTime()) {
//			System.out.println("Yes");
//			System.out.println(date);
//			System.out.println(date1);
//		}else{
//			
//			System.out.println("No");
//			System.out.println(date);
//			System.out.println(date1);
//		}
	}
	
	
	
	
	public static Long getResourceUsage(TreeMap<Date, Integer> testTreeMap) {
		TreeMap<Date, Integer> traces = new TreeMap<>();
		traces.putAll(testTreeMap);
		
		Long duration = 0L;
		
		
		if(traces.size() == 1) {
			Long endtime = new Date().getTime();
			Long firstTime = traces.firstKey().getTime();
			
			Integer number = traces.firstEntry().getValue();
			duration = (endtime - firstTime) * number;
			
		}else {
			traces.put(new Date(), 0);
			ArrayList<Date> traceKeys = new ArrayList<>(); 
			ArrayList<Integer> traceValues = new ArrayList<>(); 
			
			traceKeys.addAll(traces.keySet());
			traceValues.addAll(traces.values());
			
			Long currentTime = traceKeys.get(0).getTime();
			
			for(int i = 1; i < traceKeys.size(); i++) {
				Long tempTime = traceKeys.get(i).getTime();
				
				duration += (tempTime - currentTime) * traceValues.get(i - 1);
				
				
				
				System.out.println("+" + i + ":");
				System.out.println("tempTime:" + tempTime + ", currentTime:"  + currentTime + ", Total:" + (tempTime - currentTime));
				System.out.println(traceValues.get(i - 1));
				
				currentTime = tempTime;
			}
			
		}
		
		return duration;
		
	}

}
