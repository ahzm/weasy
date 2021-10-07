import BpmnViewer from "bpmn-js";
import React, { Component } from "react";
import { IconButton } from "@material-ui/core";
import GetAppIcon from "@material-ui/icons/GetApp";
import DescriptionIcon from "@material-ui/icons/Description";
/**
 * Class for render bpmn diagram with the bpmn.io library
 */
class bpmnViewer extends Component {
  /**
   * 
   * @param {string} props string of xml for the bpmn
   */
  constructor(props) {
    super(props);
    this.viewer = new BpmnViewer();
    this.downloadSVG = this.downloadSVG.bind(this);
    this.downloadXML = this.downloadXML.bind(this);
  }
  /**
   * 
   * @returns render the bpmn with the download xml and svg of bpmn
   */
  render() {
    return (
      <>
        <IconButton
          aria-label="download svg"
          color="primary"
          onClick={this.downloadSVG}
        >
          <GetAppIcon fontSize="large" />
          Download SVG
        </IconButton>
        <IconButton arial-label="download xml" onClick={this.downloadXML}>
          <DescriptionIcon fontSize="large" />
          Download XML
        </IconButton>
        <div
          id="diagram"
          style={{
            height: "90%",
          }}
        ></div>
      </>
    );
  }
  /**
   * Download xml 
   */
    downloadXML() {
    this.viewer.saveXML({ format: true }, function (error, xml) {
      if (error) {
        return;
      }
      var xmlBlob = new Blob([xml], {
        type: "text/xml",
      });
      var fileName = Math.random(36).toString().substring(7) + ".bpmn";
      var downloadLink = document.createElement("a");
      downloadLink.download = fileName;
      downloadLink.innerHTML = "get";
      downloadLink.href = window.URL.createObjectURL(xmlBlob);
      downloadLink.onclick = function (event) {
        document.body.removeChild(event.target);
      };
      downloadLink.style.visibility = "hidden";
      document.body.appendChild(downloadLink);
      downloadLink.click();
    });
  }
  /**
   * Downlaad svg
   */
  downloadSVG() {
    this.viewer.saveSVG({ format: true }, function (error, svg) {
      if (error) {
        return;
      }
      var svgBlob = new Blob([svg], {
        type: "image/svg+xml",
      });
      var fileName = Math.random(36).toString().substring(7) + ".svg";
      var downloadLink = document.createElement("a");
      downloadLink.download = fileName;
      downloadLink.innerHTML = "get";
      downloadLink.href = window.URL.createObjectURL(svgBlob);
      downloadLink.onclick = function (event) {
        document.body.removeChild(event.target);
      };
      downloadLink.style.visibility = "hidden";
      document.body.appendChild(downloadLink);
      downloadLink.click();
    });
  }
  /**
   * Function call when component mount 
   */
  componentDidMount() {
    this.viewer.attachTo("#diagram");
    /**
     * Function for call function to render bpmn with bpmn.io library
     * @param {string} xml of bpmn
     * @param {object} Viewer object of html were the bpmn is going to render
     */
    function importXML(xml, Viewer) {
      Viewer.importXML(xml, function (err) {
        if (err) {
          return console.error("could not import BPMN 2.0 ", err);
        }
        var canvas = Viewer.get("canvas");
        canvas.zoom("fit-viewport");
      });
    }
    importXML(this.props.xml, this.viewer);
  }
}
export default bpmnViewer;
