import {Table} from "./Table";
import {default as url} from "./backendurl";
import {useEffect, useState} from "react";
import {TableManager} from "./TableManager";

export function People(){
    let [response, setResponse] = useState({"data": [], "requestedHeaders": [], "allHeaders": [], maxPageCount:0})
    let [page, setPage] = useState(1);
    let [entryPerPage, setEntryPerPage] = useState(100);

    useEffect(() => {
        async function fetchAndWrite() {
            let response = await fetch(
                url + "/getPeople?pageNumber=" + page + "&rowPerPage=" + entryPerPage
                    )
                .then((response) => response.json());
            setResponse(response);
        }
        fetchAndWrite();
    } , [page, entryPerPage])
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
                        {response.allHeaders.map((i) =>
                            <div>
                                <input type={"checkbox"} id={i} name={i} value={i} checked={response.requestedHeaders.some(a => a == i)}/>
                                <label>{i}</label>
                            </div>)}
                    </div>
                </div>
            </TableManager>
            <Table
                data={response.data}
                header={response.requestedHeaders}
            />
        </>);
}
