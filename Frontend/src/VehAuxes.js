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

export function AddVehAuxOverlay(props) {

	return (
		<OverlayPage
			setTrigger={props.setTrigger}
			triggerNewValue={false}
		>
			<form
				style={{display: "flex",justifyContent: "space-between", flexDirection: "column", height: "100%"}}
				action={url + "/addVehAux"} method={"POST"}
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

export function UpdateVehAuxOverlay(props) {
	let [vehAux, setVehAux] = useState([]);

	useEffect(() => {
		fetchAndWrite(setVehAux, url + "/getVehAux/" + props.vehAuxData[0] + "/" + props.vehAuxData[1]);
	}, [])

	return (
		<OverlayPage
			setTrigger={props.setTrigger}
			triggerNewValue={[]}
		>
			<form
				style={{display: "flex",justifyContent: "space-between", flexDirection: "column", height: "100%"}}
				action={url + "/updateVehAux"} method={"POST"}
			>
				{props.allColumns.map((column, index) => {
					let isDisabled = ["CASE_NUMBER", "VEHICLE_NUMBER"].some((value) => value == column["name"]);
					return (
						<div key={column["name"]+"_input_div"}>
							<label style={{display: "inline"}} key={column["name"]+"_label"}>{column["name"] + ": "}</label>
							{column["type"] == "INTEGER" ?
								<input type="number"
									   name={column["name"]}
									   style={{display: "inline"}}
									   key={column["name"]+"_input"}
									   defaultValue={vehAux[index]}
									   readOnly={isDisabled}
								/>
								:
								(column["possibleValues"] == null ?
										<input
											type="text"
											name={column["name"]}
											style={{display: "inline"}}
											key={column["name"]+"_input"}
											defaultValue={vehAux[index]}
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
												return <option value={value} key={value+"_option"} selected={vehAux[index] == value}>{value}</option>
											})}
										</select>
								)
							}
						</div>
					)
				})}
				<input type="submit" value="Submit" style={{position: "absolute", bottom: "50px", width: "100%"}}/>
			</form>
			<button style={{position: "absolute", bottom: "0px", width: "100%"}} onClick={() => {
				fetch(url + "/deleteVehAux/" + props.vehAuxData[0] + "/" + props.vehAuxData[1], {method: "POST"});
			}
			}>Delete this vehAux</button>
		</OverlayPage>
	);
}

export function VehAuxes(){
	// Variable declarations
	let [page, setPage] = useState(1);
	let [order, setOrder] = useState("ASC");
	let [reload, setReload] = useState(false);
	let [columns, setColumns] = useState([{}]);
	let [caseView, setCaseView] = useState([]);
	let [vehicleView, setVehicleView] = useState([]);
	let [updateVehAux, setUpdateVehAux] = useState([]);
	let [entryPerPage, setEntryPerPage] = useState(100);
	let [orderBy, setOrderBy] = useState("CASE_NUMBER");
	let [requestedColumns, setRequestedColumns] = useState([]);
	let [response, setResponse] = useState({"data": [], maxPageCount:0})
	let [isAddVehAuxOverlayOpen, setIsAddVehAuxOverlayOpen] = useState(false);
	// Runs once on page load
	useEffect(() => {
		fetchAndWrite(setColumns, url + "/getVehAuxHeader").then((resp) => {
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
		fetchAndWrite(setResponse, url + "/getVehAuxes?pageNumber=" + page + "&rowPerPage=" + entryPerPage +
			(requestedColumns.length != 0 ? "&requestedColumns=" + requestedColumns.map(a => a["name"]).join(",") : "")
			+ (filters.length > 0 ? "&" + filters : "") + "&orderBy=" + orderBy + "&order=" + order)
	} , [page, entryPerPage, requestedColumns, order, orderBy, reload])
	return (
		<>
			<h1>VehAuxes Table Page</h1>
			{isAddVehAuxOverlayOpen && <AddVehAuxOverlay setTrigger={setIsAddVehAuxOverlayOpen} allColumns={columns}/>}
			{updateVehAux.length != 0 && <UpdateVehAuxOverlay setTrigger={setUpdateVehAux} allColumns={columns} vehAuxData={updateVehAux}/>}
			<button style={{float: "right"}} onClick={() => setIsAddVehAuxOverlayOpen(true)}>Add VehAux</button>
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
				foreignKeys={{CASE_NUMBER: setCaseView, VEHICLE_NUMBER: setUpdateVehAux}}
			/>
		</>);
}