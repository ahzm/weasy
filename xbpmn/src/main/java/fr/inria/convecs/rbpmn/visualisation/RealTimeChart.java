package fr.inria.convecs.rbpmn.visualisation;

import java.awt.BorderLayout;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.JFrame;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.ValueAxis;
import org.jfree.chart.plot.XYPlot;
import org.jfree.data.time.Millisecond;
import org.jfree.data.time.TimeSeries;
import org.jfree.data.time.TimeSeriesCollection;

import fr.inria.convecs.rbpmn.calcul.CalculExecutionTimeByInstances;
import fr.inria.convecs.rbpmn.deploy.BPMNProcess;


@SuppressWarnings("serial")
public class RealTimeChart extends ChartPanel implements Runnable {
	private static TimeSeries timeSeries;
	//private long nbrInstances = 0;
	private BPMNProcess bpmnProcess;
	
	public void SetProcessKey(BPMNProcess processKey) {
		this.bpmnProcess  = processKey;
	}

	public RealTimeChart(String chartContent, String title, String yaxisName) {
		super(createChart(chartContent, title, yaxisName));
	}

	private static JFreeChart createChart(String chartContent, String title, String yaxisName) {
		//创建时序图对象
		timeSeries = new TimeSeries(chartContent);
		TimeSeriesCollection timeseriescollection = new TimeSeriesCollection(timeSeries);
		JFreeChart jfreechart = ChartFactory.createTimeSeriesChart(title, "Time", yaxisName, timeseriescollection,
				true, true, false);
		XYPlot xyplot = jfreechart.getXYPlot();
		//纵坐标设定
		ValueAxis valueaxis = xyplot.getDomainAxis();
		//自动设置数据轴数据范围
		valueaxis.setAutoRange(true);
		//数据轴固定数据范围 30s
		//valueaxis.setFixedAutoRange(30000D);

		valueaxis = xyplot.getRangeAxis();
		//valueaxis.setRange(0.0D,200D); 

		return jfreechart;
	}

	public void run() {
		while (true) {
			try {
				timeSeries.add(new Millisecond(), randomNum());
				Thread.sleep(10000);
			} catch (InterruptedException e) {
			}
		}
	}

	private long randomNum() {
//		CalculExecTime calExecTime = new CalculExecTime(this.processKey);
//		return calExecTime.getAvgExecutionTime();
		CalculExecutionTimeByInstances calExecTime = new CalculExecutionTimeByInstances(this.bpmnProcess);
		int lastNbrInstance = 5;
		return calExecTime.getAverageExecutionTime(lastNbrInstance);
//		while(true) {
//			if(calExecTime.getNbrFinishedInstance() > nbrInstances) {
//				nbrInstances = calExecTime.getNbrFinishedInstance();
//				return calExecTime.getRealExecutionTime();
//			}else {
//				try {
//					Thread.sleep(1000);
//				} catch (InterruptedException e) {
//					// TODO Auto-generated catch block
//					e.printStackTrace();
//				}
//			}
//		}
		
		//return calExecTime.getRealExecutionTime();
		//System.out.println((Math.random() * 20));
		//return (long) (Math.random() * 20);
		
	}
	
}
