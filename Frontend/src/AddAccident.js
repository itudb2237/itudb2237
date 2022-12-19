import {Table} from "./Table";
import {useEffect, useState} from "react";
import {AddPersonOverlay} from "./People";
import {default as url} from "./backendurl";
import { AddParkworkOverlay } from "./Parkworks";
import { AddAccidentForm} from "./Accidents";


async function fetchAndWrite(setValue, requestUrl) {
	let resp = await fetch(requestUrl).then((response) => response.json());
	setValue(resp);
	return resp;
}

export function AddAccident(){
	let [people, setPeople] = useState([]);
	let [peopleHeaders, setPeopleHeaders] = useState([]);
	let [parkworkHeaders, setParkworkHeaders] = useState([]);
	let [accidentHeaders, setAccidentHeaders] = useState([]);
	let [pbtypes, setPbtypes] = useState([]);
	let [cevents, setCevents] = useState([]);
	let [vehicles, setVehicles] = useState([]);
	let [parkworks, setParkworks] = useState([]);
	let [isAddPersonOverlayVisible, setAddPersonOverlayVisible] = useState(false);
	let [isAddPbtypeOverlayVisible, setAddPbtypeOverlayVisible] = useState(false);
	let [isAddCeventOverlayVisible, setAddCeventOverlayVisible] = useState(false);
	let [isAddVehicleOverlayVisible, setAddVehicleOverlayVisible] = useState(false);
	let [isAddParkworkOverlayVisible, setAddParkworkOverlayVisible] = useState(false);

	useEffect(() => {
		fetchAndWrite(setPeopleHeaders, url + "/getPersonHeader");
		fetchAndWrite(setParkworkHeaders, url + "/getParkworkHeader");
		fetchAndWrite(setAccidentHeaders, url + "/getAccidentHeader");
	}, []);

	return (
		<>
			<h1>Add Accident</h1>
			{isAddPersonOverlayVisible &&
				<AddPersonOverlay
					allColumns={peopleHeaders}
					setTrigger={setAddPersonOverlayVisible}
					onSubmit={(event) => {
						event.preventDefault();
						setPeople([...people, new FormData(event.target)]);
						return false;
					}}
				/>}
			{isAddParkworkOverlayVisible &&
				<AddParkworkOverlay
					allColumns={parkworkHeaders}
					setTrigger={setAddParkworkOverlayVisible}
					onSubmit={(event) => {
						event.preventDefault();
						setParkworks([...parkworks, new FormData(event.target)]);
						return false;
					}}
				/>}
			<AddAccidentForm onSubmit={() => {
				for (let person of people){
					fetch(url + "/addPerson", {
						method: "POST",
						body: person
					});
				}
				for (let parkwork of parkworks){
					fetch(url + "/addParkwork", {
						method: "POST",
						body: parkwork
					});
				}
			}}
			allColumns={accidentHeaders}>
				<h2 style={{display: "inline"}}>People</h2>
				<button onClick={() => setAddPersonOverlayVisible(true)} style={{float: "right", display: "inline"}}>Add Person</button>
				<Table
					header={peopleHeaders}
					data={(()=>{
						try{
							return people.map(a => Object.values(Object.fromEntries(a.entries())));
						}catch{
							return [];
						}})()}/>
				<h2 style={{display: "inline"}}>Parkwork</h2>
				<button onClick={() => setAddParkworkOverlayVisible(true)} style={{float: "right", display: "inline"}}>Add Parkwork</button>
				<Table
					header={parkworkHeaders}
					data={(()=>{
						try{
							return parkworks.map(a => Object.values(Object.fromEntries(a.entries())));
						}catch{
							return [];
						}})()}/>
			</AddAccidentForm>
		</>)
}
