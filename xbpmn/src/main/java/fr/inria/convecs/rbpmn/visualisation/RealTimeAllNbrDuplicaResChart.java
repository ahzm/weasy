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

import fr.inria.convecs.rbpmn.common.Resource;
import fr.inria.convecs.rbpmn.deploy.BPMNProcess;

@SuppressWarnings("serial")
public class RealTimeAllNbrDuplicaResChart extends ChartPanel implements Runnable {
	//private static TimeSeries timeSeries;
	private static HashMap<Resource, TimeSeries> timeSeriesList;
	//private long nbrInstances = 0;
	private BPMNProcess bpmnProcess;
	
	public  void SetProcessKey(BPMNProcess bpmnProcess) {
		this.bpmnProcess  = bpmnProcess;
	}

	public RealTimeAllNbrDuplicaResChart(String chartContent, String title, String yaxisName, ArrayList<Resource> resources) {
		
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
	private int randomNum(Resource resource) {
		//CalculExecTime calExecTime = new CalculExecTime(this.processKey);
		return resource.getNbrDuplica();
		
	}
	
}
