import React, { useContext } from "react";
import { TaskContext } from "../context/taskContext";
import { CoupleContext } from "../context/coupleContext";
import Couples from "../components/po";
import { Grid } from "@material-ui/core";
/**
 * 
 * @returns page/component of all the partial orders 
 * call the partial order card component
 */
function PO() {
  document.title = "Partial Order";
  const [tasks] = useContext(TaskContext);
  const [couples, setCouples] = useContext(CoupleContext);
  return (
    <>
      <Grid container spacing={3}>
        {couples.map((couple) => {
          const c1 = tasks.find((task) => task.id === couple[0]);
          const c2 = tasks.find((task) => task.id === couple[1]);

          return (
            <Grid item xs={3}>
              <Couples
                key={couple[0] + couple[1]}
                c1={c1.desc}
                c2={c2.desc}
                couple={couple}
                deleteCouple={() => {
                  let newCouples = [...couples];
                  newCouples.filter((c, i) => {
                    if (c[1] === couple[1] && c[0] === couple[0]) {
                      if (i > -1) {
                        newCouples.splice(i, 1);
                      }
                      return c;
                    }
                    return false;
                  });
                  setCouples(newCouples);
                }}
              />
            </Grid>
          );
        })}
      </Grid>
    </>
  );
}
export default PO;
