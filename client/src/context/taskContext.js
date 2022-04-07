import React,{useState} from 'react';
 
/**
 * Set of task to get and set in all the context proyect
 */
export const TaskContext = React.createContext([]);
export const TasksProvider=(props)=>{
    /**
     * @param tasks tasks to set in array of json
     * @returns array tasks (in array of jsons)
     */
    const[tasks,setTasks]=useState([]);
    return(<TaskContext.Provider value={[tasks,setTasks]}>
        {props.children}
    </TaskContext.Provider>)
}
