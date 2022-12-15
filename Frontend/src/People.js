import {Table} from "./Table";
import {default as url} from "./backendurl";
import {useEffect, useState} from "react";
import {TableManager} from "./TableManager";

async function fetchAndWrite(setValue, requestUrl) {
    let resp = await fetch(requestUrl).then((response) => response.json());
    setValue(resp);
    return resp;
}

export function People(){
    let [response, setResponse] = useState({"data": [], maxPageCount:0})
    let [page, setPage] = useState(1);
    let [entryPerPage, setEntryPerPage] = useState(100);
    let [columns, setColumns] = useState({});
    let [requestedColumns, setRequestedColumns] = useState([]);

    useEffect(() => {
        fetchAndWrite(setColumns, url + "/getPersonHeader").then((resp) => {
            setRequestedColumns(Object.keys(resp));
        })
    }, [])

    useEffect(() => {
        fetchAndWrite(setResponse, url + "/getPeople?pageNumber=" + page + "&rowPerPage=" + entryPerPage +
            (requestedColumns.length != 0 && "&requestedColumns=" + requestedColumns.join(",")));
    } , [page, entryPerPage, requestedColumns])
    return (
        <>
            <h1>People Table Page</h1>
            <TableManager
                page={page}
                pageCount={response.maxPageCount}
                setPage={setPage}
                entryPerPage={entryPerPage}
                setEntryPerPage={setEntryPerPage}
                allColumns={Object.keys(columns)}
                requestedColumns={requestedColumns}
                setRequestedColumns={setRequestedColumns}
            />
            <Table
                header={requestedColumns}
                data={response.data}
            />
        </>);
}
