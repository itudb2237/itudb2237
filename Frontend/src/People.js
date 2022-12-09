import {Table} from "./Table";
import {default as url} from "./backendurl";
import {useEffect, useState} from "react";
import {PageNumber} from "./PageNumber";

export function People(){
    let [response, setResponse] = useState({"data": [], "header": [], maxPageCount:0})
    let [page, setPage] = useState(1);

    useEffect(() => {
        async function fetchAndWrite() {
            let response = await fetch(url + "/getPeople").then((response) => response.json());
            setResponse(response);
        }
        fetchAndWrite();
    } , [])
    return (
        <>
            <h1>People Table Page</h1>
            <PageNumber page={page} pageCount={response.maxPageCount} setPage={setPage}/>
            <Table data={response.data} header={response.header}/>
        </>);
}