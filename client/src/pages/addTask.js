import React, { useContext, useEffect, useState } from "react";
import { Grid, TextField, Button, IconButton } from "@material-ui/core/";
import { Alert, AlertTitle } from "@material-ui/lab";
import { TaskContext } from "../context/taskContext";
import Tasks from "./tasks";
import makeid from "../helper/makeId";
import FastForwardIcon from "@material-ui/icons/FastForward";
import { Link } from "react-router-dom";
import Tooltip from "@material-ui/core/Tooltip";
/**
 * 
 * @returns component form for adding new task
 */
function AddTask() {
  const [desc, setDesc] = useState("");
  const [dura, setDura] = useState([null, null]);
  // eslint-disable-next-line
  const [tasks, setTasks] = useContext(TaskContext);
  const [disabled, setDisabled] = useState(true);
  // eslint-disable-next-line
  const [id, setId] = useState("");
  const [success, setSuccess] = useState(false);
   /**
   * check if the inputs are empty
   */
  // eslint-disable-next-line
  useEffect(() => {
    document.title = "Add task";
    if (desc !== "" && dura[0] !== "" && dura[1] !== "") {
      setDisabled(false);
    } else {
      setDisabled(true);
    }
  });
/**
 * 
 * @param {object} e default event of input for description
 */
  const handleDescription = (e) => {
    setDesc(e.target.value);
  };
  /**
   * handle the input of minumum duration
   * @param {*} e default event of input for Minimum duration of task
   */
  const handleDuraMin = (e) => {
    const copyDura = dura.slice();
    copyDura[0] = parseInt(e.target.value, 10);
    setDura(copyDura);
  };
  /**
   * handle the input of maximum duration
   * @param {*} e default event of input for maximum duration of task
   */
  const handleDuraMax = (e) => {
    const copyDura = dura.slice();
    copyDura[1] = parseInt(e.target.value, 10);
    setDura(copyDura);
  };
  /**
   * handle submit button of form
   * @param {object} e default event of button 
   */
  const handleSubmit = (e) => {
    e.preventDefault();
    const obj = {
      id: makeid(8),
      desc: desc,
      dura: dura,
    };
    setTasks((prevTasks) => [...prevTasks, obj]);
    setId(makeid(8));
    setDesc("");
    setDura([0, 0]);
    setDisabled(true);
    setSuccess(true);
    setTimeout(() => {
      setSuccess(false);
    }, 1900);
  };
  /**
   * Component alert 
   * @returns alert component when added task
   */
  const AlertTask = () => {
    if (success) {
      return (
        <Alert severity="success">
          <AlertTitle>Added task</AlertTitle>
        </Alert>
      );
    } else {
      return null;
    }
  };
  return (
    <>
      <h1>Add task</h1>
      <Grid
        container
        direction="row"
        justify="center"
        alignItems="flex-start"
        spacing={7}
      >
        <Grid item>
          <TextField
            id="Description"
            label="Description"
            variant="outlined"
            value={desc}
            onChange={handleDescription}
          />
        </Grid>
        <Grid item>
          <TextField
            id="minTime"
            label="Min. Time (unit of time)"
            variant="outlined"
            value={dura[0]}
            type="number"
            onChange={handleDuraMin}
          />
        </Grid>
        <Grid item>
          <TextField
            id="maxTime"
            label="Max. Time (unit of time)"
            variant="outlined"
            value={dura[1]}
            type="number"
            onChange={handleDuraMax}
          />
        </Grid>
        <Grid item>
          <Button
            variant="contained"
            color="primary"
            style={{ padding: "18px" }}
            disabled={disabled ? true : false}
            onClick={handleSubmit}
          >
            Add task
          </Button>
        </Grid>
        <Grid item>
          <Tooltip title="Add couples">
            <IconButton
              aria-label="next"
              variant="contained"
              component={Link}
              to={"/addpo"}
            >
              <FastForwardIcon fontSize="large" />
            </IconButton>
          </Tooltip>
        </Grid>
      </Grid>
      <AlertTask />

      <Tasks />
    </>
  );
}

export default AddTask;
