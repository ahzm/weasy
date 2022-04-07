package fr.inria.convecs.xbpmn;

import java.util.ArrayList;

public class testList {
	public static void main(String[] args) {
		
	ArrayList<Integer> test1 = new ArrayList<>();
	test1.add(10);
	test1.add(20);
	test1.add(30);
	
	test1.add(40);
	
	ArrayList<Integer> test2 = new ArrayList<>();
	test2.add(1);
	test2.add(2);
	test2.add(3);
	
	int firstValue = test1.get(0);
	int result = 0;
	for(int i = 1; i< test1.size(); i++) {
		int currentValue = test1.get(i);
		
		result += (currentValue - firstValue) * test2.get(i - 1);
		firstValue = currentValue;
		
	}
	System.out.println(result);
	
	}
	
		
}
