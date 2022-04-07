package fr.inria.convecs.rbpmn.visualisation;

import java.awt.BorderLayout;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.ArrayList;
import java.util.Set;

import javax.swing.JFrame;

import fr.inria.convecs.rbpmn.common.Resource;
import fr.inria.convecs.rbpmn.deploy.BPMNProcess;

public class CreateChart {
	
	private BPMNProcess bpmnProcess;
	public CreateChart(BPMNProcess bpmnProcess){
		this.bpmnProcess = bpmnProcess;
	}
	
	public void showAETChart() {
		JFrame frame = new JFrame("AET Chart");
		//RealTimeChart rtcp = new RealTimeChart("Random Data", "Random", "Value");
		RealTimeChart rtcp = new RealTimeChart(" AET Value", "AET (Average Execution Time) ", "AET (seconds)");
		rtcp.SetProcessKey(this.bpmnProcess);
		new BorderLayout();
		frame.getContentPane().add(rtcp, BorderLayout.CENTER);
		//frame.setBounds(200, 120, 10, 80);
		//frame.pack();
		frame.setSize(500, 400);
		frame.setVisible(true);
		(new Thread(rtcp)).start();
		frame.addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent windowevent) {
				System.exit(0);
			}

		});
	}
		
	public void showNbrDuplicaResChart(ArrayList<Resource> res) {
		JFrame frame = new JFrame("Resources Nbr Chart");
		//RealTimeChart rtcp = new RealTimeChart("Random Data", "Random", "Value");
		RealTimeAllNbrDuplicaResChart rtcp = new RealTimeAllNbrDuplicaResChart("res", "Resources", "Value", res);
		new BorderLayout();
		frame.getContentPane().add(rtcp, BorderLayout.CENTER);
		//frame.setBounds(200, 120, 10, 80);
		//frame.pack();
		frame.setSize(500, 400);
		frame.setVisible(true);
		(new Thread(rtcp)).start();
		frame.addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent windowevent) {
				System.exit(0);
			}

		});
	}
	
	public void showResPercentChart(ArrayList<Resource> res) {
		JFrame frame = new JFrame("Resources Percent Chart");
		//RealTimeChart rtcp = new RealTimeChart("Random Data", "Random", "Value");
		RealTimeAllResPercentChart rtcp = new RealTimeAllResPercentChart("res", "Resources(%)", "Value", res);
		rtcp.SetProcessKey(this.bpmnProcess);
		new BorderLayout();
		frame.getContentPane().add(rtcp, BorderLayout.CENTER);
		//frame.setBounds(200, 120, 10, 80);
		//frame.pack();
		frame.setSize(500, 400);
		frame.setVisible(true);
		(new Thread(rtcp)).start();
		frame.addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent windowevent) {
				System.exit(0);
			}

		});
	}
}
