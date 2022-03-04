import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Card, CardContent, Typography, IconButton } from "@material-ui/core";
import DeleteIcon from "@material-ui/icons/Delete";
import PropTypes from "prop-types";
const useStyles = makeStyles({
  root: {
    minWidth: 275,
  },
  bullet: {
    display: "inline-block",
    margin: "0 2px",
    transform: "scale(0.8)",
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
});
/**
 * Component that shows each task in the add task and tasks pages
 * @example ./task.md
 */
export default function Task({ desc, dura, id, deleteTask }) {
  const classes = useStyles();
  return (
    <Card className={classes.root} variant="outlined">
      <CardContent>
        {/* <Typography className={classes.title} color="textSecondary" gutterBottom>
          {id}
        </Typography> */}

        <Typography className={classes.pos} variant="h5" component="h2">
          <IconButton onClick={deleteTask}>
            <DeleteIcon color="primary" />
          </IconButton>
          {desc}
        </Typography>
        <Typography variant="body2" component="p" color="textSecondary">
          Min. time: {dura[0]}; Max. time: {dura[1]}
        </Typography>
      </CardContent>
    </Card>
  );
}
Task.propTypes = {
  /** Description of the task */
  desc: PropTypes.string,
  /** Array of time duration max time, min time */
  dura: PropTypes.array,
  /** Id of the task */
  id: PropTypes.string,
  /** function for delete the task*/
  deleteTask: PropTypes.func,
};
