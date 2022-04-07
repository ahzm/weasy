import React, { useContext } from "react";
import { TaskContext } from "../context/taskContext";
import { CoupleContext } from "../context/coupleContext";
import Task from "../components/tasks";
import { Grid } from "@material-ui/core";
/**
 * 
 * @returns page/component of all the tasks in cards calling the task component
 */
function Tasks() {
  document.title = "Tasks";
  const [tasks, setTasks] = useContext(TaskContext);
  const [couples, setCouples] = useContext(CoupleContext);
  return (
    <>
      <Grid container spacing={3}>
        {tasks.map((task) => (
          <Grid item xs={3}>
            <Task
              desc={task.desc}
              dura={task.dura}
              key={task.id}
              id={task.id}
              deleteTask={() => {
                let newCouples = [...couples];
                newCouples = couples.filter(
                  (couple) => couple[0] !== task.id && couple[1] !== task.id
                );
                let newTasks = [...tasks];
                newTasks = tasks.filter((t) => t.id !== task.id);
                setCouples(newCouples);
                setTasks(newTasks);
              }}
            />
          </Grid>
        ))}
      </Grid>
    </>
  );
}
export default Tasks;
