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
            >
                <div
                    style={{display: "inline-block", outline: "none"}}
                    onMouseEnter={() => document.getElementById("headerselect").style.display = "block"}
                    onMouseLeave={() => document.getElementById("headerselect").style.display = "none"}
                >
                    <button>
                        Selected Headers
                    </button>
                    <div id={"headerselect"} style={{position: "absolute", display: "none", zIndex: "1", backgroundColor: '#f5f5f5'}}>
                        {Object.keys(columns).map((i) =>
                            <div key={i + "_selection_row"}>
                                <input
                                    type={"checkbox"}
                                    id={i + "_checkbox"}
                                    key={i + "_checkbox"}
                                    checked={requestedColumns.some(a => a == i)}
                                    onChange={(event) => setRequestedColumns(
                                        event.target.checked ?
                                            Object.keys(columns).filter(a => requestedColumns.some(b => b == a) || a == i) : requestedColumns.filter(a => a != i)
                                    )}
                                />
                                <label>{i}</label>
                            </div>)}
                    </div>
                </div>
            </TableManager>
            <Table
                header={requestedColumns}
                data={response.data}
            />
        </>);
}
