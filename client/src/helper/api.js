import React, { Component } from "react";
import PropTypes from "prop-types";
import ReactDOM from "react-dom";

import { Prompt, useHistory } from "react-router-dom";
import { PointSpreadLoading } from "react-loadingg";

import ellipse from "../styles/node-32.png";
import trash from "../styles/trash.png";
import zoomin from "../styles/zoom-in.png";
import zoomout from "../styles/zoom-out.png";
import grid from "../styles/grid.gif";
import arrow from "../styles/arrow.png";
import "../index.css";

import {
  mxGraph,
  mxRubberband,
  mxPopupMenu,
  mxKeyHandler,
  mxClient,
  mxUtils,
  mxEvent,
  mxConstants,
  mxToolbar,
  mxDragSource,
  mxCell,
  mxGeometry,
  mxCellState,
  mxVertexHandler,
} from "mxgraph-js";

import { makeStyles } from "@material-ui/core/styles";
import {
  CssBaseline,
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Tooltip,
  Card,
  CardContent,
} from "@material-ui/core";
import CloseIcon from "@material-ui/icons/Close";
import AccessTimeIcon from "@material-ui/icons/AccessTime";
import AccountTreeIcon from "@material-ui/icons/AccountTree";
import ArrowBackIcon from "@material-ui/icons/ArrowBack";

import BpmnDiagram from "./getbpmn";
import ReactModal from "react-modal";
/**
 * Style for the top bar
 */
const useStyles = makeStyles((theme) => ({
  appBar: {
    transition: theme.transitions.create(["margin", "width"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
}));
/**
 * Card that shows the compute time of abstract graph
 * @param {max time, min time} props
 * @returns Card component
 */
function ComputeTime(props) {
  return (
    <div
      style={{
        position: "relative",
        height: window.innerHeight - 1000,
        width: window.innerWidth - 100,
      }}
    >
      {props.comp ? (
        <Card
          style={{
            color: "#ffffff",
            backgroundColor: "#3f3141",
            position: "absolute",
            bottom: 0,
            right: 0,
            zIndex: 99,
          }}
        >
          <CardContent>
            <Typography variant="h5" conponent="h2">
              <AccessTimeIcon fontSize="small" color="inherit" /> Compute Time
            </Typography>
            <Typography variant="body2" component="p">
              <strong>Max.</strong> Execution Time: <strong>{props.max}</strong> (<em>unit of time</em>)
            </Typography>
            <Typography variant="body2" component="p">
              <strong>Min.</strong> Execution Time: <strong>{props.min}</strong> (<em>unit of time</em>)
            </Typography>
          </CardContent>
        </Card>
      ) : null}
    </div>
  );
}
ComputeTime.propTypes = {
  /** Max time of the abstract graph */
  max: PropTypes.number,
  /** Min time of the abstracth graph */
  min: PropTypes.number,
};
/**
 * Top menu with the title abstract graph
 * @param {children} props Component that is show in the page (the abstract graph)
 * @returns page with the top menu and the abstract graph
 */
function Menu(props) {
  const classes = useStyles();
  let history = useHistory();
  function handleBack() {
    history.push("/");
  }
  return (
    <div className={classes.root}>
      <CssBaseline />
      <AppBar
        style={{ backgroundColor: "#7E6383" }}
        position="fixed"
        className={classes.appBar}
      >
        <Toolbar>
          <IconButton color="inherit" onClick={handleBack}>
            <Prompt message="Are you sure you want to go back? Warning: Your modifications in the abstract graph will be lost." />
            <ArrowBackIcon />
          </IconButton>
          <Typography variant="h6" noWrap>
            Abstract Graph
          </Typography>
        </Toolbar>
      </AppBar>

      <main style={{ marginTop: 50, marginLeft: 30 }}>{props.children}</main>
    </div>
  );
}
Menu.propTypes = {
  /** Component inside the menu*/
  children: PropTypes.elementType,
};
/**
 *  Default size of tasks
 */
let taskSize = 80;
/**
 * Class for render the abstract graph
 */
class DiagramComp extends Component {
  /**
   * Constructor of the class
   * @param {json} props  api response {"nodes": array,"arcs": array,"minTime": number,"maxTime": number}
   */
  constructor(props) {
    super(props);
    this.state = {
      showModal: false,
      comp: false,
      max: this.props.response.maxTime,
      min: this.props.response.minTime,
      menu: false,
      data: {},
      gnsp: null,
      bpmn: "",
    };
    this.LoadGraph = this.LoadGraph.bind(this);
    this.compute = this.compute.bind(this);
    this.generateBPMN = this.generateBPMN.bind(this);
    this.getObj = this.getObj.bind(this);
    this.handleCloseModal = this.handleCloseModal.bind(this);
    this.isLoop = this.isLoop.bind(this);
    this.noStart = this.noStart.bind(this);
  }
  /**
   * Frist function after mounting of the component
   */
  componentDidMount() {
    this.LoadGraph();
  }
  /**
   * Use MxGraph for render the abstract graph
   */
  LoadGraph() {
    var container = ReactDOM.findDOMNode(this.refs.divGraph);
    var tbContainer = ReactDOM.findDOMNode(this.refs.tbContainer);
    
    /* Connect
    // Defines a subclass for mxVertexHandler that adds a set of clickable
    // icons to every selected vertex.
    function mxVertexToolHandler(state) {
      mxVertexHandler.apply(this, arguments);
    }

    mxVertexToolHandler.prototype = new mxVertexHandler();
    mxVertexToolHandler.prototype.constructor = mxVertexToolHandler;

    mxVertexToolHandler.prototype.domNode = null;

    mxVertexToolHandler.prototype.init = function () {
      mxVertexHandler.prototype.init.apply(this, arguments);

    
      this.domNode = document.createElement("div");
      this.domNode.style.position = "absolute";
      this.domNode.style.whiteSpace = "nowrap";

      // Workaround for event redirection via image tag in quirks and IE8
      function createImage(src) {
        if (mxClient.IS_IE && !mxClient.IS_SVG) {
          var img = document.createElement("div");
          img.style.backgroundImage = "url(" + src + ")";
          img.style.backgroundPosition = "center";
          img.style.backgroundRepeat = "no-repeat";
          img.style.display = mxClient.IS_QUIRKS ? "inline" : "inline-block";

          return img;
        } else {
          return mxUtils.createImage(src);
        }
      }

      // Connect
      var img = createImage(arrow);
      img.setAttribute("title", "Connect");
      img.style.cursor = "pointer";
      img.style.width = "15px";
      img.style.height = "15px";
      mxEvent.addGestureListeners(
        img,
        mxUtils.bind(this, function (evt) {
          var pt = mxUtils.convertPoint(
            this.graph.container,
            mxEvent.getClientX(evt),
            mxEvent.getClientY(evt)
          );
          this.graph.connectionHandler.start(this.state, pt.x, pt.y);
          this.graph.isMouseDown = true;
          this.graph.isMouseTrigger = mxEvent.isMouseEvent(evt);
          mxEvent.consume(evt);
        })
      );
      this.domNode.appendChild(img);

      this.graph.container.appendChild(this.domNode);
     this.redrawTools();
    };
    mxVertexToolHandler.prototype.redraw = function () {
      mxVertexHandler.prototype.redraw.apply(this);
      this.redrawTools();
    };

    mxVertexToolHandler.prototype.redrawTools = function () {
      if (this.state != null && this.domNode != null) {
        var dy =
          mxClient.IS_VML && document.compatMode == "CSS1Compat" ? 20 : 4;
        this.domNode.style.left = this.state.x + this.state.width - 56 + "px";
        this.domNode.style.top = this.state.y + this.state.height + dy + "px";
      }
    }; 

    mxVertexToolHandler.prototype.destroy = function (sender, me) {
      mxVertexHandler.prototype.destroy.apply(this, arguments);

      if (this.domNode != null) {
        this.domNode.parentNode.removeChild(this.domNode);
        this.domNode = null;
      }
    }; */
    // Checks if the browser is supported
    if (!mxClient.isBrowserSupported()) {
      // Displays an error message if the browser is not supported.
      mxUtils.error("Browser is not supported!", 200, false);
    } else {
      // Disables the built-in context menu
      mxEvent.disableContextMenu(container);
      //Toolbar
      var toolbar = new mxToolbar(tbContainer);
      toolbar.enabled = true;
      // Creates the graph inside the given container
      var graph = new mxGraph(container);
      graph.dropEnabled = true;
      /* Connect
      mxDragSource.prototype.getDropTarget = function (graph, x, y) {
        var cell = graph.getCellAt(x, y);
        if (!graph.isValidDropTarget(cell)) {
          cell = null;
        }
        return cell;
      }; */
      // Enables rubberband selection
      new mxRubberband(graph);
      new mxPopupMenu(graph);
      /**
       * Key handler for delete objects in abstract graph
       */
      var keyHandler = new mxKeyHandler(graph);
      keyHandler.bindKey(46, function (evt) {
        if (graph.isEnabled()) {
          graph.removeCells();
        }
      });
      keyHandler.bindKey(8, function (evt) {
        if (graph.isEnabled()) {
          graph.removeCells();
        }
      });
      // Gets the default parent for inserting new cells. This is normally the first
      // child of the root (ie. layer 0).
      var parent = graph.getDefaultParent();

      // Enables tooltips, new connections and panning
      graph.setPanning(true);
      graph.setTooltips(true);
      graph.setConnectable(true);
      graph.setEnabled(true);
      graph.setEdgeLabelsMovable(false);
      graph.setVertexLabelsMovable(false);
      graph.setMultigraph(true);
      graph.setGridEnabled(true);
      graph.setAllowDanglingEdges(true);
      graph.getModel().beginUpdate();
      /*  Connect
      graph.connectionHandler.createEdgeState = function (me) {
        var edge = graph.createEdge(null, null, null, null, null);

        return new mxCellState(
          this.graph.view,
          edge,
          this.graph.getCellStyle(edge)
        );
      };
      graph.connectionHandler.createTarget = true;

      graph.createHandler = function (state) {
        if (state != null && this.model.isVertex(state.cell)) {
          return new mxVertexToolHandler(state);
        }

        return mxGraph.prototype.createHandler.apply(this, arguments);
      };
 */
/**
 * Styles for the node and task
 * Node = ROUNDES
 * Task= TASK
 */
      var style = new Object();
      style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_ELLIPSE;
      style[mxConstants.STYLE_FILL_OPACITY] = 30;
      style[mxConstants.STYLE_STROKECOLOR] = "#212F3D";
      style[mxConstants.STYLE_FILLCOLOR] = "#D5F5E3";
      style[mxConstants.STYLE_STROKEWIDTH] = 2;
      graph.getStylesheet().putCellStyle("ROUNDED", style);
      var styleTask = new Object();
      styleTask[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_HEXAGON;
      styleTask[mxConstants.STYLE_FILL_OPACITY] = 30;
      styleTask[mxConstants.STYLE_STROKECOLOR] = "#212F3D";

      styleTask[mxConstants.STYLE_FILLCOLOR] = "#D5F5E3";
      styleTask[mxConstants.STYLE_STROKE_OPACITY] = 50;
      styleTask[mxConstants.STYLE_STROKEWIDTH] = 1;
      graph.getStylesheet().putCellStyle("TASK", styleTask);
/** set default color for connection */
      graph.getStylesheet().getDefaultEdgeStyle()[
        mxConstants.STYLE_STROKECOLOR
      ] = "#212F3D";
/** Function for the drag node in the side menu */
      const addVertex = (icon, w, h, style) => {
        var vertex = new mxCell(null, new mxGeometry(0, 0, w, h), style);
        vertex.setVertex(true);
        addToolbarItem(graph, toolbar, vertex, icon);
      };
      try {
        addVertex(ellipse, 45, 45, "ROUNDED");

        toolbar.addLine();
        /**
         * Delete object in the abstract graph, side menu option
         */
        toolbar.addItem(
          "Delete" /* Title */,
          trash /* Icon */,
          function () {
            if (graph.isEnabled()) {
              graph.removeCells();
            }
          } /* function */,
          null /* pressed icon */,
          null /* style */,
          null /* factory Method */
        );

        toolbar.addLine();
        /** Zoom in the abstract graph */
        toolbar.addItem("Zoom In", zoomin, function () {
          graph.zoomIn();
        });
        toolbar.addLine();
        /** Zoom out the abstract graph */
        toolbar.addItem("Zoom Out", zoomout, function () {
          graph.zoomOut();
        });
        toolbar.addLine();

        //mxGrapg component
        var doc = mxUtils.createXmlDocument();
        var node = doc.createElement("Node");
        let nodess = [];
        let linksCopy = [];
        /**
         * copy of links to build abstract graph
         * @param {array} links of original links 
         */
        const copyLinks = (links = [...this.props.initialGraph.links]) => {
          links.map((d) => {
            // linksCopy.push(d)
            linksCopy.push(d);
          });
        };
        copyLinks();
        node.setAttribute("ComponentID", "[P01]");
     /**
      * Build the abstract graph
      * @param {array} nodes 
      * @param {number} initX 
      * @param {number} initY 
      */
        const makeGraph = (nodes, initX = 0, initY = 20) => {
         
          nodes.map((node) => {
            // size node subgraph
            const getSize = (ns, w1, deep = 0) => {
              let w2 = w1;
              ns.forEach((n) => {
                w2 = n.content.length + w2;
                if (Object.entries(n.subgraph).length !== 0) {
                  w2 = getSize(n.subgraph.nodes, w2, deep + 1);
                }
              });
              return w2;
            };
            /**
             * 
             * @param {number} w 
             * @returns array with the space needed inside the node for the number of tasks 
             */
            const getSquare = (w) => {
              let sa = 0;
              if (!Number.isInteger(Math.sqrt(w))) {
                w = Math.pow(Math.ceil(Math.sqrt(w)), 2);
              }
              for (let i = 0; i < w + 1; i++) {
                sa = Math.PI * Math.pow(taskSize / 2, 2) + sa;
              }
              //taille Cote
              let l = Math.sqrt(sa);
              let d = Math.sqrt(Math.pow(l, 2) + Math.pow(l, 2));
              let pc = (d - l) / 2;
              return [l, d, pc];
            };
            /**
             * Function for get the Diametre of the node
             * @param {object} sg subgraph
             * @param {number} diametre of the circle
             * @returns 
             */
            const getDiametre = (sg, diametre = 0) => {
              diametre =
                sg.links.length * 30 +
                getSize(sg.nodes, 0) * taskSize * 1.5 +
                diametre;

              return diametre;
            };
            // initial size of node
            let w = node.content.length;
            // coordinates for the tasks and node
            let x = node.coordinates[0] / 2 + initX;
            let y = initY;
            let x2 = 0;
            let y2 = 0;
            let xs = [];
            let ys = [];
            // if node only has one task
            if (w === 1 && Object.entries(node.subgraph).length === 0) {
              w = w * taskSize * 1.75;
              x2 = x + w / 2 - taskSize / 2;
              y2 = y;
              ys = [y + w / 2 - taskSize / 2];
              xs = [x2];
            } 
            // if node has more that one task and no subgraph
            else if (w > 1 && Object.entries(node.subgraph).length == 0) {
              const [l, d, pc] = getSquare(w);
              x2 = x + pc;
              y2 = y + pc;
              let x2Copy = x2;
              node.content.map((n, i) => {
                xs.push(x2);
                ys.push(y2);
                x2 = x2 + taskSize;
                if (x2 > x2Copy + l) {
                  x2 = x2Copy;
                  y2 = y2 + taskSize;
                }
              });
              w = d;
            } 
            // if node has subgraph
            else {
              let [l, d, pc] = getSquare(w);

              d = getDiametre(node.subgraph) * 1.2;
              l = d * 0.707107;
              pc = (d - l) / 2;

              x2 = x + pc;
              y2 = y + pc;

              let x2Copy = x2;
              node.content.map(() => {
                xs.push(x2);
                ys.push(y2);
                x2 = x2 + taskSize;
                if (x2 > x2Copy + l) {
                  x2 = x2Copy;
                  y2 = y2 + taskSize;
                }
              });
              initX = x;

              w = d;
              let mitad = y + w / 2;
              initY = mitad - (taskSize + 15) / 2;
            }

            //render of nodes
            let content = graph.insertVertex(
              parent,
              node.id,
              null,
              x,
              y,
              w,
              w,
              "ROUNDED"
            );
            content.setConnectable(true);

            // render of tasks
            node.content.map((t, i) => {
              let tas = graph.insertVertex(
                parent,
                t.id,
                t.desc,
                xs[i],
                ys[i],
                taskSize,
                taskSize,
                "TASK"
              );
              tas.setConnectable(false);
            });
            // recursion if node has subgraph
            if (Object.entries(node.subgraph).length !== 0) {
              copyLinks(node.subgraph.links);
              makeGraph(node.subgraph.nodes, initX, initY);
            }
            nodess.push({ id: node.id, content: content });
          });
        };
        // make initial abstract graph
        makeGraph(this.props.initialGraph.nodes);
        nodess.map((node) => {
          linksCopy.forEach((d, i) => {
            if (d.source.ident === node.id || d.target.ident === node.id) {
              let source = nodess.filter(
                (node) => node.id === d.source.ident
              )[0];
              let target = nodess.filter(
                (node) => node.id === d.target.ident
              )[0];
              let arc = graph.insertEdge(
                parent,
                null,
                null,
                source.content,
                target.content,
                "strokeColor=#212F3D"
              );
              linksCopy.splice(i, 1);
            }
          });
        });
        //data
      } finally {
        // Updates the display
        graph.getModel().endUpdate();
        graph.fit();
        graph.view.rendering = true;
        graph.refresh();
        this.setState((prevState) => ({
          ...prevState,
          gnsp: graph,
        }));
      }

      // drag node
      function addToolbarItem(graph, toolbar, prototype, image) {
        var funct = function (graph, evt, cell) {
          graph.stopEditing(false);
          var pt = graph.getPointForEvent(evt);
          var vertex = graph.getModel().cloneCell(prototype);
          vertex.geometry.x = pt.x;
          vertex.geometry.y = pt.y;

          graph.setSelectionCells(graph.importCells([vertex], 0, 0, cell));
        };
        var img = toolbar.addMode(
          "Node",
          image,
          function (evt, cell) {
            var pt = this.graph.getPointForEvent(evt);
            funct(graph, evt, cell, pt.x, pt.y);
          },
          null,
          null /** style */,
          null
        );
        // Disables dragging if element is disabled. This is a workaround
        // for wrong event order in IE. Following is a dummy listener that
        // is invoked as the last listener in IE.
        mxEvent.addListener(img, "mousedown", function (evt) {
          // do nothing
        });
        // This listener is always called first before any other listener
        // in all browsers.
        mxEvent.addListener(img, "mousedown", function (evt) {
          if (img.enabled === false) {
            mxEvent.consume(evt);
          }
        });
        mxUtils.makeDraggable(img, graph, funct);

        return img;
      }
     
    }
  }
  /**
   * Close the modal of the bpmn diagram
   */
  handleCloseModal() {
    this.setState((prevState) => ({ ...prevState, showModal: false }));
  }
  /**
   *
   * @returns json of the abstract graph in screen
   */
  getObj() {
    /** Copy of the object graph */
    let copyCells = { ...this.state.gnsp.getModel().cells };
    let cells = [];
    let tasks = [];
    let nodes = [];
    let links = [];
    for (const [k, v] of Object.entries(copyCells)) {
      cells.push(v);
    }
    links = cells.filter((c) => c.source && c.target);
    links = links.map((l) => {
      return {
        source: l.source.id,
        target: l.target.id,
      };
    });
    /** Filter the component that matter (tasks, nodes, arcs) */
    cells = cells.filter((c) => c.style);

    tasks = cells.filter((c) => c.value);

    nodes = cells.filter((c) => c.style === "ROUNDED");
    /** Filter the tasks */
    let points = [];
    let close = [];
    tasks.map((task) => {
      /* 
        Relationship between nodes and task, to which it belongs and distance between them
      */
      let nodeBelongs = nodes.map((node) => {
        return {
          task: task,
          node: node,
          distance: Math.sqrt(
            Math.pow(task.geometry.x - node.geometry.x, 2) +
              Math.pow(task.geometry.y - node.geometry.y, 2)
          ),
          belongs:
            task.geometry.x + task.geometry.width / 2 > node.geometry.x &&
            task.geometry.x + task.geometry.width / 2 <
              node.geometry.x + node.geometry.width &&
            task.geometry.y + task.geometry.height / 2 > node.geometry.y &&
            task.geometry.y + task.geometry.height / 2 <
              node.geometry.y + node.geometry.height,
        };
      });

      points.push(nodeBelongs);
    });
    /** Node to witch task belongs */
    points = points.map((point) => point.filter((p) => p.belongs));
    /**  if there is more than one node to which the task belongs */
    points.map((point) => {
      close.push(
        point.filter((poi) => {
          return poi.distance === Math.min(...point.map((p) => p.distance));
        })[0]
      );
    });
    /** Filter the nodes and the tasks that it has */
    let updateNodes = nodes.map((node) => {
      let list_tasks = close
        .filter((task) => task.node.id === node.id)
        .map((task) => task.task.id);
      let updateTaks = [];
      this.props.tasks.map((task) => {
        list_tasks.forEach((id) => {
          if (id === task.id) {
            updateTaks.push({
              ...task,
              id: task.desc,
              desc: task.id,
            });
          }
        });
      });
      let listTest = nodes
        .filter(
          (n) =>
            node.geometry.x > n.geometry.x &&
            node.geometry.x < n.geometry.x + n.geometry.width &&
            node.geometry.y > n.geometry.y &&
            node.geometry.y < n.geometry.y + n.geometry.width
        )
        .map((n) => n.id);
      return {
        id: node.id,
        list_tasks: updateTaks,
        subgraph: listTest,
      };
    });

    const obj = {
      tasks: [...this.props.tasks],
      links: links,
      nodespy: updateNodes,
    };

    return obj;
  }
  /**
   * Call api for check if there is a loop in the abstact graph
   * @param {object} reqOP object for the api request
   * @returns json of boolean value
   */
  isLoop(reqOP) {
    return fetch("http://localhost:3001/isloop", reqOP)
      .then((res) => {
        if (res.ok) {
          return res.json();
        } else {
          throw new Error("No response");
        }
      })
      .then((json) => {
        return json;
      });
  }
  /**
   * Call api for check if there is a start node in the abstract graph
   * @param {object} reqOP object for the api request
   * @returns json of boolean value
   */
  noStart(reqOP) {
    return fetch("http://localhost:3001/getstart", reqOP)
      .then((res) => {
        if (res.ok) {
          return res.json();
        } else {
          throw new Error("No response");
        }
      })
      .then((json) => {
        return json;
      });
  }
  /**
   * Call api for render modal and the BPMN diagram
   * call and check if there is a start node
   */
  generateBPMN() {
    const obj = this.getObj();
    const reqOP = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(obj),
    };
    this.noStart(reqOP).then((start) => {
      start = JSON.parse(start.toLowerCase());
      if (start) {
        fetch("http://localhost:3001/genbpmn", reqOP).then((res) => {
          res.json().then((data) => {
            this.setState((prevState) => ({
              ...prevState,
              bpmn: data,
              comp: false,
              showModal: true,
            }));
          });
        });
      } else {
        alert("Please give me an initial node");
      }
    });
  }
  /**
   * Call api for check the new compute time
   */
  compute() {
    const obj = this.getObj();
    const reqOP = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(obj),
    };
    //loop is not working properly
    this.noStart(reqOP).then((start) => {
      this.isLoop(reqOP).then((loop) => {
        loop = JSON.parse(loop.toLowerCase());
        start = JSON.parse(start.toLowerCase());
        if (start) {
          if (!loop) {
            fetch("http://localhost:3001/modgraph", reqOP).then((res) => {
              res.json().then((data) => {
                this.setState((prevState) => ({
                  ...prevState,
                  max: data.maxTime,
                  min: data.minTime,
                  comp: !prevState.comp,
                }));
              });
            });
          } else {
            alert(
              "Watch out! , your abstract graph maybe has a loop, that’s a conflict"
            );
          }
        } else {
          alert("Please give me an initial node");
          this.setState((prevState) => ({
            ...prevState,
            comp: false,
          }));
        }
      });
    });
  }
/**
 * @returns render of the component abstract graph, side menu and modal for bpmn
 */
  render() {
    return (
      <>
        <div
          className="tbContainer"
          ref="tbContainer"
          id="tbContainer"
          style={{
            paddingRight: 100,
            color: "#000000",
            marginRight: 10,
            marginTop: 3,
            "& img": {
              padding: 100,
            },
          }}
        >
          <Tooltip title="Compute">
            <IconButton
              aria-label="Compute"
              onClick={this.compute}
              color="inherit"
              style={{ padding: 0, paddingBottom: 10 }}
            >
              <AccessTimeIcon fontSize="large" />
            </IconButton>
          </Tooltip>
          <Tooltip title="Generate BPMN">
            <IconButton
              arial-label="Generate BPMN"
              onClick={this.generateBPMN}
              color="inherit"
              style={{ padding: 0, paddingBottom: 10 }}
            >
              <AccountTreeIcon fontSize="large" />
            </IconButton>
          </Tooltip>
        </div>

        <Menu>
          <div style={{ paddingTop: 100 }}>
            <div
              className="graph-container"
              ref="divGraph"
              id="divGraph"
              style={{ paddingLeft: 30, backgroundImage: grid, margin: 30 }}
            />
            <ComputeTime
              comp={this.state.comp}
              max={this.state.max}
              min={this.state.min}
            />
          </div>

          <ReactModal
            isOpen={this.state.showModal}
            style={{
              overlay: {
                position: "fixed",
                top: "50px",
              },
            }}
            contentLabel="BPMN Diagram"
          >
            <IconButton
              aria-label="close"
              color="secondary"
              onClick={this.handleCloseModal}
            >
              <CloseIcon fontSize="large" />
            </IconButton>
            {this.state.bpmn !== "" ? (
              <BpmnDiagram xml={this.state.bpmn} />
            ) : (
              <PointSpreadLoading size={"large"} color={"#7E6383"} />
            )}
          </ReactModal>
        </Menu>
      </>
    );
  }
}
export default DiagramComp;
