import {Table} from "./Table";
import {default as url} from "./backendurl";
import {useEffect, useState} from "react";
import {TableManager} from "./TableManager";
import {OverlayPage} from "./OverlayPage";

async function fetchAndWrite(setValue, requestUrl) {
    let resp = await fetch(requestUrl).then((response) => response.json());
    setValue(resp);
    return resp;
}

export function AddAccidentOverlay(props) {

    return (
        <OverlayPage
            setTrigger={props.setTrigger}
            triggerNewValue={false}
        >
            <form
                style={{display: "flex",justifyContent: "space-between", flexDirection: "column", height: "100%"}}
                action={url + "/addAccident"} method={"POST"}
            >
                {props.allColumns.map((column) => {
                    return (
                        <div key={column["name"]+"_input_div"}>
                            <label style={{display: "inline"}} key={column["name"]+"_label"}>{column["name"] + ": "}</label>
                            {column["type"] == "INTEGER" ?
                                <input type="number" name={column["name"]} style={{display: "inline"}} key={column["name"]+"_input"}/> :
                                (column["possibleValues"] == null ?
                                        <input type="text" name={column["name"]} style={{display: "inline"}} key={column["name"]+"_input"}/> :
                                        <select name={column["name"]} style={{display: "inline"}} key={column["name"]+"_select"}>
                                            {["NULL", ...column["possibleValues"].slice(3)].map((value) => {
                                                return <option value={value} key={value+"_option"}>{value}</option>
                                            })}
                                        </select>
                                )
                            }
                        </div>
                    )
                })}
                <input type="submit" value="Submit"/>
            </form>
        </OverlayPage>
    );
}

export function UpdateAccidentOverlay(props) {
    let [accident, setAccident] = useState([]);

    useEffect(() => {
        fetchAndWrite(setAccident, url + "/getAccident/" + props.caseData[props.allColumns.map(a => a["name"]).findIndex((a) => a == "CASE_NUMBER")]);
    }, [])

    return (
        <OverlayPage
            setTrigger={props.setTrigger}
            triggerNewValue={[]}
        >
            <form
                style={{display: "flex",justifyContent: "space-between", flexDirection: "column", height: "80%"}}
                action={url + "/updateAccident"} method={"POST"}
            >
                {props.allColumns.map((column, index) => {
                    let isDisabled = ["CASE_NUMBER"].some((value) => value == column["name"]);
                    return (
                        <div key={column["name"]+"_input_div"}>
                            <label style={{display: "inline"}} key={column["name"]+"_label"}>{column["name"] + ": "}</label>
                            {column["type"] == "INTEGER" ?
                                <input type="number"
                                       name={column["name"]}
                                       style={{display: "inline"}}
                                       key={column["name"]+"_input"}
                                       defaultValue={accident[index]}
                                       readOnly={isDisabled}
                                />
                                :
                                (column["possibleValues"] == null ?
                                        <input
                                            type="text"
                                            name={column["name"]}
                                            style={{display: "inline"}}
                                            key={column["name"]+"_input"}
                                            defaultValue={accident[index]}
                                            readOnly={isDisabled}
                                        />
                                        :
                                        <select
                                            name={column["name"]}
                                            style={{display: "inline"}}
                                            key={column["name"]+"_select"}
                                            readOnly={isDisabled}
                                        >
                                            {["NULL", ...column["possibleValues"].slice(3)].map((value) => {
                                                return <option value={value} key={value+"_option"} selected={accident[index] == value}>{value}</option>
                                            })}
                                        </select>
                                )
                            }
                        </div>
                    )
                })}
                <input type="submit" value="Submit"/>
            </form>
            <button style={{position: "absolute", bottom: "0px", width: "100%"}} onClick={() => {
                fetch(url + "/deleteAccident/" + props.caseData[0], {method: "POST"});
            }
            }>Delete this accident</button>
        </OverlayPage>
    );
}

export function Accidents(){
    // Variable declarations
    let [page, setPage] = useState(1);
    let [order, setOrder] = useState("ASC");
    let [reload, setReload] = useState(false);
    let [columns, setColumns] = useState([{}]);
    let [updateCase, setUpdateCase] = useState([]);
    let [entryPerPage, setEntryPerPage] = useState(100);
    let [orderBy, setOrderBy] = useState("CASE_NUMBER");
    let [requestedColumns, setRequestedColumns] = useState([]);
    let [response, setResponse] = useState({"data": [], maxPageCount:0})
    let [isAddCaseOverlayOpen, setIsAddCaseOverlayOpen] = useState(false);
    // Runs once on page load
    useEffect(() => {
        fetchAndWrite(setColumns, url + "/getAccidentHeader").then((resp) => {
            setRequestedColumns(resp);
        })
    }, [])
    // Runs when page, entryPerPage, or requestedColumns changes (i.e. when the table needs to be updated) or when the page is first loaded
    useEffect(() => {
        let filters = (requestedColumns.filter(a => a["filter"] != null && (a["type"] != "INTEGER" || a["filter"].every(b => b != ""))).map(a => {
            if(a["type"] == "INTEGER"){
                return "filter" + a["name"] + "=" + a["filter"].join(",");
            }
            return "filter" + a["name"] + "=" + a["filter"] })).join("&")
        fetchAndWrite(setResponse, url + "/getAccidents?pageNumber=" + page + "&rowPerPage=" + entryPerPage +
            (requestedColumns.length != 0 ? "&requestedColumns=" + requestedColumns.map(a => a["name"]).join(",") : "")
            + (filters.length > 0 ? "&" + filters : "") + "&orderBy=" + orderBy + "&order=" + order)
    } , [page, entryPerPage, requestedColumns, order, orderBy, reload])
    return (
        <>
            <h1>Accident Table Page</h1>
            {isAddCaseOverlayOpen && <AddAccidentOverlay setTrigger={setIsAddCaseOverlayOpen} allColumns={columns}/>}
            {updateCase.length != 0 && <UpdateAccidentOverlay setTrigger={setUpdateCase} allColumns={columns} caseData={updateCase}/>}
            <button style={{float: "right"}} onClick={() => setIsAddCaseOverlayOpen(true)}>Add Accident</button>
            <TableManager
                page={page}
                pageCount={response.maxPageCount}
                setPage={setPage}
                entryPerPage={entryPerPage}
                setEntryPerPage={setEntryPerPage}
                allColumns={columns}
                requestedColumns={requestedColumns}
                setRequestedColumns={setRequestedColumns}
                orderBy={orderBy}
                setOrderBy={setOrderBy}
                order={order}
                setOrder={setOrder}
                reload={reload}
                setReload={setReload}
            />
            <Table
                header={requestedColumns}
                setHeader={setRequestedColumns}
                data={response.data}
                foreignKeys={{CASE_NUMBER: setUpdateCase}}
            />
        </>);
}
