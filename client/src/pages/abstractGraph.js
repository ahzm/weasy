//graph plus simple pas sub graph
import React, { useState, useEffect, useContext } from "react";
import { TaskContext } from "../context/taskContext";
import { CoupleContext } from "../context/coupleContext";
import DiagramComp from "../helper/api";
import "../index.css";
import { PointSpreadLoading } from "react-loadingg";
/**
 * 
 * @returns render of the abstract graph 
 */
function Graph() {
  const [tasks ] = useContext(TaskContext);
  const [couples] = useContext(CoupleContext);
  const [response, setRes] = useState({});
  const [nodes, setNodes] = useState([]);
  const [arcs, setArcs] = useState([]);
  const [active, setActive] = useState(false);
  const [succ, setSucc] = useState(false);
  const [initialGraph, setInitialGraph] = useState({});
// eslint-disable-next-line
/**
 * function to call after component mount and calls api for get the python object to render abstract graph
 */
  useEffect(() => {
    document.title = "Abstract Graph ";
    const reqOp = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tasks: tasks, couples: couples }),
    };
    fetch("http://localhost:3001/abstgraph", reqOp).then((res) => {
      res.json().then((data) => {
        setRes(data);
        setNodes(data.nodes);
        setArcs(data.arcs);
      });
    });
    // eslint-disable-next-line
  }, []);
  
  useEffect(() => {
    if (nodes.length !== 0 && arcs.length !== 0) {
      setInitialGraph(makeNodes(nodes, tasks, arcs));
      setSucc(true);
    }
  }, [nodes, arcs]);
  const makeSubgraph = (subgraph, tasks) => {
    if (Object.entries(subgraph).length !== 0) {
      return makeNodes(subgraph.nodes, tasks, subgraph.arcs);
    }
    return {};
  };
  /**
   * format nodes for the api 
   * @param {array} nodes every node in array is a json
   * @param {array} tasks every task in arry is a json
   * @param {arry} arcs every arc in arry is an array 
   * @returns nodes and links 
   */
  const makeNodes = (nodes, tasks, arcs) => {
    let x = 20;
    let y = 0;
    let ns = [];
    let as = [];
    let subgraph = {};
    nodes.map((node) => {
      const act = [];
      node.list_activities.forEach((activi) => {
        const cont = tasks.filter((task) => task.id === activi);
        act.push(cont[0]);
      });
      subgraph = makeSubgraph(node.subgraph, tasks);
      ns = [
        ...ns,
        {
          id: node.ident,
          content: act,
          coordinates: [x, y],
          subgraph: subgraph,
        },
      ];
      x = x + 500;
      y = y + 60;
    });
    as = arcs.map((arc) => {
      let source = nodes.filter((node) => node.ident === arc.source_node)[0];
      let target = nodes.filter((node) => node.ident === arc.target_node)[0];
      return {
        source: source,
        target: target,
      };
    });
    return {
      nodes: ns,
      links: as,
    };
  };
  return (
    <>
      <div style={{ margin: "40px" }}>{succ ? (
          <DiagramComp
            initialGraph={initialGraph}
            response={response}
            tasks={tasks}
            active={active}
            setActive={setActive}
            setInitialGraph={setInitialGraph}
          />
        ) : (
          <PointSpreadLoading size={"large"} color={"#7E6383"} />
        )}</div>
    </>
  );
}

export default Graph;
