import React, { useContext, useState, useEffect } from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Button, Grid, IconButton, TextField } from "@material-ui/core";
import Autocomplete from "@material-ui/lab/Autocomplete";
import { TaskContext } from "../context/taskContext";
import { CoupleContext } from "../context/coupleContext";
import FastForwardIcon from "@material-ui/icons/FastForward";
import { Link } from "react-router-dom";

import Tooltip from "@material-ui/core/Tooltip";
import ArrowForwardIcon from "@material-ui/icons/ArrowForward";
import PO from "./po";
// eslint-disable-next-line
const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
}));
/**
 * @returns component form for add partial order and cards of the partial orders
 */
function AddPO() {
  const [couple, setCouple] = useState(["", ""]);
  const [disabled, setDisabled] = useState(true);
  const [tasks] = useContext(TaskContext);
  // eslint-disable-next-line
  const [couples, setCouples] = useContext(CoupleContext);
  // eslint-disable-next-line
  /**
   * handler of the input for the frist couple in the partial order
   * @param {object} event default of the input 
   * @param {object} value value in the input
   */
  const handleCouple1 = (event, value) => {
    const copy = couple.slice();
    if (value !== null) {
      copy[0] = value.id;
      setCouple(copy);
    }
  };
  // eslint-disable-next-line
  /**
   * handler of the input for the second couple in the partial order
   * @param {object} event default of the input 
   * @param {object} value value in the input
   */
  const handleCouple2 = (event, value) => {
    const copy = couple.slice();
    if (value !== null) {
      copy[1] = value.id;
      setCouple(copy);
    }
  };
  /**
   * handeler for submit the form 
   * @param {object} e default event for the button for submit form
   */
  const handleSubmit = (e) => {
    e.preventDefault();
    setCouples((prevCouples) => [...prevCouples, couple]);
  };
  // eslint-disable-next-line
  /**
   * disable button if inputs are empty
   */
  useEffect(() => {
    document.title = "Add partial order";
    if (couple[0] !== "" && couple[1] !== "" && couple[0] !== couple[1]) {
      setDisabled(false);
    } else {
      setDisabled(true);
    }
  });
  return (
    <>
      <h1>Add partial order</h1>
      <Grid
        container
        direction="row"
        justify="center"
        alignItems="flex-start"
        spacing={7}
      >
        <Grid item>
          <Autocomplete
            id="couple-1-opt"
            options={tasks}
            getOptionLabel={(option) => option.desc}
            onChange={handleCouple1}
            renderInput={(params) => (
              <TextField {...params} label="Couple 1" variant="outlined" />
            )}
          />
        </Grid>
        <Grid item>
          <div style={{ padding: "18px" }}>
            <ArrowForwardIcon color="primary" fontSize="large" />
          </div>
        </Grid>
        <Grid item>
          <Autocomplete
            id="couple-1-opt"
            options={tasks}
            getOptionLabel={(option) => option.desc}
            onChange={handleCouple2}
            renderInput={(params) => (
              <TextField {...params} label="Couple 1" variant="outlined" />
            )}
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
            Add a couple
          </Button>
        </Grid>
        <Grid item>
          <Tooltip title="Abstract Graph">
            <IconButton
              aria-label="next"
              variant="contained"
              component={Link}
              to={"/abstractgraph"}
            >
              <FastForwardIcon fontSize="large" />
            </IconButton>
          </Tooltip>
        </Grid>
      </Grid>
      <PO />
    </>
  );
}
export default AddPO;
