import React,{useState} from 'react';
/**
 * Set of couples save in all the context of the project
 */
export const CoupleContext = React.createContext([]);
export const CoupleProvider=(props)=>{
     /**
     * @param couples couples to set in array of json
     * @returns array couples (in array of jsons)
     */
    const[couples,setCouples]=useState([]);
    return(<CoupleContext.Provider value={[couples,setCouples]}>
        {props.children}
    </CoupleContext.Provider>)
}