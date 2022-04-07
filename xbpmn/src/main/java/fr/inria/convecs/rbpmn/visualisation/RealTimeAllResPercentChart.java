package fr.inria.convecs.rbpmn.visualisation;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.ValueAxis;
import org.jfree.chart.plot.XYPlot;
import org.jfree.data.time.Millisecond;
import org.jfree.data.time.TimeSeries;
import org.jfree.data.time.TimeSeriesCollection;

import com.google.protobuf.Duration;

import fr.inria.convecs.rbpmn.calcul.CalculExecutionTimeByTasks;
import fr.inria.convecs.rbpmn.calcul.CalculResourcesUsageByTasks;
import fr.inria.convecs.rbpmn.common.Resource;
import fr.inria.convecs.rbpmn.deploy.BPMNProcess;

@SuppressWarnings("serial")
public class RealTimeAllResPercentChart extends ChartPanel implements Runnable {
	//private static TimeSeries timeSeries;
	private static HashMap<Resource, TimeSeries> timeSeriesList;
	//private long nbrInstances = 0;
	private BPMNProcess bpmnProcess;
	
	public  void SetProcessKey(BPMNProcess bpmnProces) {
		this.bpmnProcess  = bpmnProces;
	}

	public RealTimeAllResPercentChart(String chartContent, String title, String yaxisName, ArrayList<Resource> resources) {
		
		super(createChart(chartContent, title, yaxisName, resources));
	}

	private static JFreeChart createChart(String chartContent, String title, String yaxisName, ArrayList<Resource> resources) {
		//创建时序图对象
		timeSeriesList = new HashMap<>();
		for (Resource keyRes: resources) {
			timeSeriesList.put(keyRes, new TimeSeries(keyRes.getName()));
		}
		
		TimeSeriesCollection timeseriescollection = new TimeSeriesCollection();
		for(Resource resKey : timeSeriesList.keySet()) {
			timeseriescollection.addSeries(timeSeriesList.get(resKey));
		}
		
		JFreeChart jfreechart = ChartFactory.createTimeSeriesChart(title, "Realtime", yaxisName, timeseriescollection,
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
				for(Resource resKey : timeSeriesList.keySet()) {
					timeSeriesList.get(resKey).add(new Millisecond(), randomNum(resKey));
				}
				//timeSeries.add(new Millisecond(), randomNum());
				Thread.sleep(3000);
			} catch (InterruptedException e) {
			}
		}
	}

	//private long randomNum() {
	private double randomNum(Resource keyRes) {
		//CalculExecTime calExecTime = new CalculExecTime(this.processKey);
		keyRes.getId();
		Long duation  = keyRes.getDuration(2);
		CalculResourcesUsageByTasks usageRes = new CalculResourcesUsageByTasks(this.bpmnProcess);
		
		if (usageRes.calculTotalRes().containsKey(keyRes.getId())) {
			
			double result = usageRes.calculTotalRes(2).get(keyRes.getId()).doubleValue() * 1000 / duation.doubleValue();
			if(result > 0.70) {
				keyRes.addResource();
			}else if (result < 0.5) {
				keyRes.reduceResource();
			}
			
			return usageRes.calculTotalRes(2).get(keyRes.getId()).doubleValue() * 1000 / duation.doubleValue();
		}else {
			return 0.0;
		}
		
		//Integer nbrUsage = usageRes.calculTotalRes();
		//return nbrUsage.doubleValue() / duation.doubleValue();
		
//		CalculResUsage calResUsage = new CalculResUsage(this.processKey);
//		LocalResources resources = new LocalResources();
//		if(calResUsage.getALLResUsage(resources.getResources()) != null) {
//			System.out.println("---***---:"+ calResUsage.getALLResUsage(resources.getResources()));
//			if(calResUsage.getALLResUsage(resources.getResources()).containsKey(keyRes)){
//				return calResUsage.getALLResUsage(resources.getResources()).get(keyRes) * 100;
//			}else {
//				return 0.0;
//			}
//		}
//		return 0.0;
		
	}
	
}
