package fr.inria.convecs.xbpmn;

import java.util.Date;

public class TimerTest {

	public int a = 2;
	private Date date;
	
	public TimerTest() {
		this.date = new Date();
	}
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		
		
		TimerTest tt = new TimerTest();
		Date newDate = new Date(tt.date.getTime() + 1000L);
		System.out.println(tt.a);
		tt.add(1, newDate);
		System.out.println(tt.a);

	}
	
	
	public void add(int temp, Date date) {
		System.out.println(date.getTime());
		System.out.println(this.date.getTime());
		if((date.getTime()) - this.date.getTime()>= 1000L) {
			this.a += temp;
		}
		
		
	}

}
