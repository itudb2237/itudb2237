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

export function AddPersonOverlay(props) {

	return (
		<OverlayPage
			setTrigger={props.setTrigger}
			triggerNewValue={false}
		>
			<form style={{display: "flex",justifyContent: "space-between", flexDirection: "column", height: "100%"}}>
				{props.allColumns.map((column) => {
					return (
						<div key={column["name"] + "_addperson"}>
							<label>{column["name"] + ": "}</label>
							{column["type"] == "INTEGER" ?
								<input type="number" name={column}/> :
								(column["possibleValues"] == null ?
									<input type="text" name={column}/> :
								 	<select name={column}>
										{["NULL", ...column["possibleValues"].slice(3)].map((value) => {
											return <option value={value}>{value}</option>
										})}
									 </select>
								)
							}
						</div>
					)
				})}
				<button type="submit">Submit</button>
			</form>
		</OverlayPage>
	);
}

export function People(){
	// Variable declarations
	let [page, setPage] = useState(1);
	let [order, setOrder] = useState("ASC");
	let [isAddPersonOverlayOpen, setIsAddPersonOverlayOpen] = useState(false);
	let [columns, setColumns] = useState([{}]);
	let [entryPerPage, setEntryPerPage] = useState(100);
	let [orderBy, setOrderBy] = useState("CASE_NUMBER");
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
		let filters = (requestedColumns.filter(a => a["filter"] != null && (a["type"] != "INTEGER" || a["filter"].every(b => b != ""))).map(a => {
			if(a["type"] == "INTEGER"){
				return "filter" + a["name"] + "=" + a["filter"].join(",");
			}
			return "filter" + a["name"] + "=" + a["filter"] })).join("&")
		fetchAndWrite(setResponse, url + "/getPeople?pageNumber=" + page + "&rowPerPage=" + entryPerPage +
			(requestedColumns.length != 0 ? "&requestedColumns=" + requestedColumns.map(a => a["name"]).join(",") : "")
			+ (filters.length > 0 ? "&" + filters : "") + "&orderBy=" + orderBy + "&order=" + order)
	} , [page, entryPerPage, requestedColumns, order, orderBy])
	return (
		<>
			<h1>People Table Page</h1>
			{isAddPersonOverlayOpen && <AddPersonOverlay setTrigger={setIsAddPersonOverlayOpen} allColumns={columns}/>}
			<button style={{float: "right"}} onClick={() => setIsAddPersonOverlayOpen(true)}>Add Person</button>
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
			<Table
				header={requestedColumns}
				setHeader={setRequestedColumns}
				data={response.data}
			/>
		</>);
}
