import {Table} from "./Table";
import {default as url} from "./backendurl";
import {useEffect, useState} from "react";
import {PageManager} from "./PageManager";

export function People(){
    let [response, setResponse] = useState({"data": [], "header": [], maxPageCount:0})
    let [page, setPage] = useState(1);
    let [entryPerPage, setEntryPerPage] = useState(100);

    useEffect(() => {
        async function fetchAndWrite() {
            let response = await fetch(url + "/getPeople?pageNumber=" + page + "&rowPerPage=" + entryPerPage).then((response) => response.json());
            setResponse(response);
        }
        fetchAndWrite();
    } , [page, entryPerPage])
    return (
        <>
            <h1>People Table Page</h1>
            <PageManager page={page} pageCount={response.maxPageCount} setPage={setPage} entryPerPage={entryPerPage} setEntryPerPage={setEntryPerPage}/>
            <Table data={response.data} header={response.header}/>
        </>);
}