import React, { Component } from "react";
import { Route, Switch } from "react-router-dom";
import Graph from "./pages/abstractGraph";
import AddPO from "./pages/addPO";
import AddTask from "./pages/addTask";
import PO from "./pages/po";
import Tasks from "./pages/tasks";

import SideBar from "./components/Dashboard";
import theme from "./styles/Theme";
import { ThemeProvider } from "@material-ui/core";
import { TasksProvider } from "./context/taskContext";
import { CoupleProvider } from "./context/coupleContext";
/**
 * Principal page with the routes of the pages
 */
class App extends Component {
  render() {
    const App = () => {
      return (
        <CoupleProvider>
          <TasksProvider>
            <ThemeProvider theme={theme}>
              <Switch>
                <Route path="/abstractgraph">
                  <Graph />
                </Route>

                <Route path="/addpo">
                  <SideBar>
                    <AddPO />
                  </SideBar>
                </Route>

                <Route path="/addtask">
                  <SideBar>
                    <AddTask />
                  </SideBar>
                </Route>
                <Route path="/partialo">
                  <SideBar>
                    <h1>Partial Order</h1>
                    <PO />
                  </SideBar>
                </Route>
                <Route path="/tasks">
                  <SideBar>
                    <h1>Tasks</h1>
                    <Tasks />
                  </SideBar>
                </Route>
                <Route path="/">
                  <SideBar>
                    <AddTask />
                  </SideBar>
                </Route>
              </Switch>
            </ThemeProvider>
          </TasksProvider>
        </CoupleProvider>
      );
    };
    return (
      <Switch>
        <App />
      </Switch>
    );
  }
}
export default App;
