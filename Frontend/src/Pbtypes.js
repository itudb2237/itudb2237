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

export function AddPbtypeOverlay(props) {

	return (
		<OverlayPage
			setTrigger={props.setTrigger}
			triggerNewValue={false}
		>
			<form
				style={{display: "flex",justifyContent: "space-between", flexDirection: "column", height: "100%"}}
				action={url + "/addPbtype"} method={"POST"}
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

export function UpdatePbtypeOverlay(props) {
	let [pbtype, setPbtype] = useState([]);

	useEffect(() => {
		fetchAndWrite(setPbtype, url + "/getPbtype/" + props.pbtypeData[0] + "/" + props.pbtypeData[1] + "/" + props.pbtypeData[2]);
	}, [])

	return (
		<OverlayPage
			setTrigger={props.setTrigger}
			triggerNewValue={[]}
		>
			<form
				style={{display: "flex",justifyContent: "space-between", flexDirection: "column", height: "100%"}}
				action={url + "/updatePbtype"} method={"POST"}
			>
				{props.allColumns.map((column, index) => {
					let isDisabled = ["CASE_NUMBER", "VEHICLE_NUMBER", "PERSON_NUMBER"].some((value) => value == column["name"]);
					return (
						<div key={column["name"]+"_input_div"}>
							<label style={{display: "inline"}} key={column["name"]+"_label"}>{column["name"] + ": "}</label>
							{column["type"] == "INTEGER" ?
								<input type="number"
									   name={column["name"]}
									   style={{display: "inline"}}
									   key={column["name"]+"_input"}
									   defaultValue={pbtype[index]}
									   readOnly={isDisabled}
								/>
								:
								(column["possibleValues"] == null ?
										<input
											type="text"
											name={column["name"]}
											style={{display: "inline"}}
											key={column["name"]+"_input"}
											defaultValue={pbtype[index]}
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
												return <option value={value} key={value+"_option"} selected={pbtype[index] == value}>{value}</option>
											})}
										</select>
								)
							}
						</div>
					)
				})}
				<input type="submit" value="Submit"/>
			</form>
			<button onClick={() => {
				fetch(url + "/deletePbtype/" + props.pbtypeData[0] + "/" + props.pbtypeData[1] + "/" +
					props.pbtypeData[2], {method: "DELETE"});
			}
			}>Delete this pbtype</button>
		</OverlayPage>
	);
}

export function Pbtypes(){
	// Variable declarations
	let [page, setPage] = useState(1);
	let [order, setOrder] = useState("ASC");
	let [reload, setReload] = useState(false);
	let [columns, setColumns] = useState([{}]);
	let [caseView, setCaseView] = useState([]);
	let [vehicleView, setVehicleView] = useState([]);
	let [updatePbtype, setUpdatePbtype] = useState([]);
	let [entryPerPage, setEntryPerPage] = useState(100);
	let [orderBy, setOrderBy] = useState("CASE_NUMBER");
	let [requestedColumns, setRequestedColumns] = useState([]);
	let [response, setResponse] = useState({"data": [], maxPageCount:0})
	let [isAddPbtypeOverlayOpen, setIsAddPbtypeOverlayOpen] = useState(false);
	// Runs once on page load
	useEffect(() => {
		fetchAndWrite(setColumns, url + "/getPbtypeHeader").then((resp) => {
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
		fetchAndWrite(setResponse, url + "/getPbtypes?pageNumber=" + page + "&rowPerPage=" + entryPerPage +
			(requestedColumns.length != 0 ? "&requestedColumns=" + requestedColumns.map(a => a["name"]).join(",") : "")
			+ (filters.length > 0 ? "&" + filters : "") + "&orderBy=" + orderBy + "&order=" + order)
	} , [page, entryPerPage, requestedColumns, order, orderBy, reload])
	return (
		<>
			<h1>Pbtypes Table Page</h1>
			{isAddPbtypeOverlayOpen && <AddPbtypeOverlay setTrigger={setIsAddPbtypeOverlayOpen} allColumns={columns}/>}
			{updatePbtype.length != 0 && <UpdatePbtypeOverlay setTrigger={setUpdatePbtype} allColumns={columns} pbtypeData={updatePbtype}/>}
			<button style={{float: "right"}} onClick={() => setIsAddPbtypeOverlayOpen(true)}>Add Pbtype</button>
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
				foreignKeys={{CASE_NUMBER: setCaseView, VEHICLE_NUMBER: setVehicleView, PERSON_NUMBER: setUpdatePbtype}}
			/>
		</>);
}
