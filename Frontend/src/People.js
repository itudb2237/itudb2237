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

/*export function AddPersonOverlay(props) {

	return (
		<OverlayPage
			/!*setTrigger={}
			triggerNewValue={}*!/
		>
			<form>
				<label>Case Number</label>
				<input type={"number"} id={"caseNumber"} name={"caseNumber"}/>
				<label>Vehicle Number</label>
				<input type={"number"} id={"vehicleNumber"} name={"vehicleNumber"}/>
				<label>Person Number</label>
				<input type={"number"} id={"personNumber"} name={"personNumber"}/>
				<label>Age</label>
				<input type={"number"} id={"age"} name={"age"}/>
				<label>Sex</label>
				<input type={}
			</form>
		</OverlayPage>
	);
}*/

export function People(){
	// Variable declarations
	let [page, setPage] = useState(1);
	let [columns, setColumns] = useState([{}]);
	let [entryPerPage, setEntryPerPage] = useState(100);
	let [requestedColumns, setRequestedColumns] = useState([]);
	let [response, setResponse] = useState({"data": [], maxPageCount:0})
	// Runs once on page load
	useEffect(() => {
		fetchAndWrite(setColumns, url + "/getPersonHeader").then((resp) => {
			setRequestedColumns(resp);
		})
	}, [])
	// Runs when page, entryPerPage, or requestedColumns changes (i.e. when the table needs to be updated) or when the page is first loaded
	useEffect(() => {
		let filters = (requestedColumns.filter(a => a["filter"] != null).map(a =>
			"filter" + a["name"] + "=" + a["filter"] )).join("&")
		fetchAndWrite(setResponse, url + "/getPeople?pageNumber=" + page + "&rowPerPage=" + entryPerPage +
			(requestedColumns.length != 0 ? "&requestedColumns=" + requestedColumns.map(a => a["name"]).join(",") : "")
			+ (filters.length > 0 ? "&" + filters : ""));
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
				allColumns={columns}
				requestedColumns={requestedColumns}
				setRequestedColumns={setRequestedColumns}
			/>
			<Table
				header={requestedColumns}
				setHeader={setRequestedColumns}
				data={response.data}
			/>
		</>);
}
