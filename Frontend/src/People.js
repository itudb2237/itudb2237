import {Table} from "./Table";
import {default as url} from "./backendurl";
import {useEffect, useState} from "react";

export function People(){
    let [response, setResponse] = useState({"data": [], "header": []})

    useEffect(() => {
        async function fetchAndWrite() {
            let response = await fetch(url + "/getPeople").then((response) => response.json());
            console.log(response);
            setResponse(response);
        }
        fetchAndWrite();
    } , [])
    return (<><h1>People Table Page</h1><Table data={response.data} header={response.header}/></>);
}