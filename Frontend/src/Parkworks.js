import {TableForParkwork} from "./TableForParkwork";
import {default as url} from "./backendurl";
import {useEffect, useState} from "react";
import {TableManager} from "./TableManager";

async function fetchAndWrite(setValue, requestUrl) {
	let resp = await fetch(requestUrl).then((response) => response.json());
	setValue(resp);
	return resp;
}

export function Parkworks(){
	// Variable declarations
	let [page, setPage] = useState(1);
	let [order, setOrder] = useState("AZB");
	let [orderBy, setOrderBy] = useState("CASE_NUMBER");
	let [requestedColumns, setRequestedColumns] = useState([]);
	let [columns, setColumns] = useState([{}]);
	let [response, setResponse] = useState({"data": [], maxPageCount:0})
	let [entryPerPage, setEntryPerPage] = useState(100);

	useEffect(() => {
		fetchAndWrite(setColumns, url + "/getParkworkHeader").then((resp) => {
			setRequestedColumns(resp);
		})
	}, [])

	useEffect(() => {
		let filters = (requestedColumns.filter(a => a["filter"] != null && (a["type"] != "INTEGER" || a["filter"].every(b => b != ""))).map(a => {
			if(a["type"] == "INTEGER"){
				return "filter" + a["name"] + "=" + a["filter"].join(",");
			}
			return "filter" + a["name"] + "=" + a["filter"] })).join("&")
		fetchAndWrite(setResponse, url + "/getParkworks?pageNumber=" + page + "&rowPerPage=" + entryPerPage +
			(requestedColumns.length != 0 ? "&requestedColumns=" + requestedColumns.map(a => a["name"]).join(",") : "")
			+ (filters.length > 0 ? "&" + filters : "") + "&orderBy=" + orderBy + "&order=" + order)
	} , [page, entryPerPage, requestedColumns, order, orderBy])
	
    return (
		<>
			<h1>Parkwork Table Page</h1>
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
			/>
			<TableForParkwork
				header={requestedColumns}
				setHeader={setRequestedColumns}
				data={response.data}
			/>
		</>);
}