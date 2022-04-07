const spawn = require("child_process").spawn;
const cors = require("cors");
const bodyParser = require("body-parser");
const express = require("express"),
  app = express();
app.use(cors());
app.use(bodyParser.json());
require("dotenv").config();
app.set("view engine", "ejs");
app.use("/", require("./routes/hello"));
const PORT = process.env.PORT || 3001;

app.listen(PORT, () => {
  console.log(`Server working ${PORT}`);
});
// Get Abstract Graph
app.post("/abstgraph", (req, res) => {
  let po = req.body;
  //-----python------
  const pyProcess = spawn("python", [
    "./python/AbstractToBPMN/src/apiGet.py",
    JSON.stringify(po.tasks),

    JSON.stringify(po.couples),
  ]);
  pyProcess.stdout.on("data", (data) => {
	console.log(String(data))
    res.json(JSON.parse(String(data)));
  });
});
// New Max time and new Min Time
app.post("/modgraph", (req, res) => {
  let gph = req.body;

  //------P+Y+T+H+O+N--------
  const pyProcess = spawn("python", [
    "./python/AbstractToBPMN/src/getNewMaxMin.py",
    JSON.stringify(gph.tasks),
    JSON.stringify(gph.links),
    JSON.stringify(gph.nodespy),
  ]);
  pyProcess.stdout.on("data", (data) => {
    res.json(JSON.parse(String(data)));
  });
});

//get XML for bpmn diagram
app.post("/genbpmn", (req, res) => {
  let gph = req.body;
  const pyProcess = spawn("python", [
    "./python/AbstractToBPMN/src/getBPMN.py",
    JSON.stringify(gph.tasks),
    JSON.stringify(gph.links),
    JSON.stringify(gph.nodespy),
  ]);
  pyProcess.stdout.on("data", (data) => {
    
    res.json(String(data));
  });
});

// check if there is a loop
app.post("/isloop", (req, res) => {
  let gph = req.body;
  const pyProcess = spawn("python", [
    "./python/AbstractToBPMN/src/getLoop.py",
    JSON.stringify(gph.tasks),
    JSON.stringify(gph.links),
    JSON.stringify(gph.nodespy),
  ]);
  pyProcess.stdout.on("data", (data) => {
    res.json(String(data));
  });
});

// check if start node exist
app.post("/getstart", (req, res) => {
  let gph = req.body;
  const pyProcess = spawn("python", [
    "./python/AbstractToBPMN/src/getStartNode.py",
    JSON.stringify(gph.tasks),
    JSON.stringify(gph.links),
    JSON.stringify(gph.nodespy),
  ]);
  pyProcess.stdout.on("data", (data) => {
    res.json(String(data));
  });
});
