import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Card, CardContent, Typography, IconButton } from "@material-ui/core";
import DeleteIcon from "@material-ui/icons/Delete";
import ArrowForwardIcon from "@material-ui/icons/ArrowForward";
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
 *  Component that shows each couple
 * @example ./po.md
 */

function Couples({ c1, c2, couple, deleteCouple }) {
  const classes = useStyles();
  return (
    <Card className={classes.root} variant="outlined">
      <CardContent>
        <Typography className={classes.pos} variant="h5" component="h2">
          <IconButton onClick={deleteCouple}>
            <DeleteIcon color="primary" />
          </IconButton>
          {c1} <ArrowForwardIcon color="primary" /> {c2}
        </Typography>
      </CardContent>
    </Card>
  );
}
export default Couples;
Couples.propTypes = {
  /** Description of first couple */
  c1: PropTypes.string,
  /** Description of second couple */
  c2: PropTypes.string,
  /** Array of Couple for do tests*/
  couple: PropTypes.array,
  /** Function for delete any couple */
  deleteCouple: PropTypes.func,
};
