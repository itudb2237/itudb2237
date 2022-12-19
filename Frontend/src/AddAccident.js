import {Table} from "./Table";
import {useEffect, useState} from "react";
import {AddPersonOverlay} from "./People";
import {default as url} from "./backendurl";
import { AddParkworkOverlay } from "./Parkworks";
import { AddAccidentForm} from "./Accidents";
import { AddPbtypeOverlay} from "./Pbtypes";
import { AddCeventOverlay } from "./Cevents";


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
	let [pbtypesHeaders, setPbtypeHeaders] = useState([]);
	let [ceventsHeaders, setCeventsHeaders] = useState([]);
	let [pbtypes, setPbtypes] = useState([]);
	let [cevents, setCevents] = useState([]);
	let [vehicles, setVehicles] = useState([]);
	let [parkworks, setParkworks] = useState([]);
	let [isAddParkworkOverlayVisible, setAddParkworkOverlayVisible] = useState(false);
	let [isAddPersonOverlayVisible, setAddPersonOverlayVisible] = useState(false);
	let [isAddPbtypeOverlayVisible, setAddPbtypeOverlayVisible] = useState(false);
	let [isAddCeventOverlayVisible, setAddCeventOverlayVisible] = useState(false);
	let [isAddVehicleOverlayVisible, setAddVehicleOverlayVisible] = useState(false);

	
	useEffect(() => {
		fetchAndWrite(setPeopleHeaders, url + "/getPersonHeader");
		fetchAndWrite(setParkworkHeaders, url + "/getParkworkHeader");
		fetchAndWrite(setAccidentHeaders, url + "/getAccidentHeader");
		fetchAndWrite(setPbtypeHeaders, url + "/getPbtypeHeader");
		fetchAndWrite(setCeventsHeaders, url + "/getCeventHeader");
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
			{isAddPbtypeOverlayVisible &&
				<AddPbtypeOverlay
					allColumns={pbtypesHeaders}
					setTrigger={setAddPbtypeOverlayVisible}
					onSubmit={(event) => {
						event.preventDefault();
						setParkworks([...pbtypes, new FormData(event.target)]);
						return false;
					}}
				/>}
			{isAddCeventOverlayVisible &&
				<AddCeventOverlay
					allColumns={ceventsHeaders}
					setTrigger={setAddCeventOverlayVisible}
					onSubmit={(event) => {
						event.preventDefault();
						setCevents([...cevents, new FormData(event.target)]);
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
				for (let pbtype of pbtypes){
					fetch(url + "/addPbtype", {
						method: "POST",
						body: pbtype
					});
				}
				for (let cevent of cevents){
					fetch(url + "/addCevent", {
						method: "POST",
						body: cevent
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
								<h2 style={{display: "inline"}}>People</h2>
				<button onClick={() => setAddPbtypeOverlayVisible(true)} style={{float: "right", display: "inline"}}>Add Pbtype</button>
				<Table
					header={pbtypesHeaders}
					data={(()=>{
						try{
							return pbtypes.map(a => Object.values(Object.fromEntries(a.entries())));
						}catch{
							return [];
						}})()}/>
				<h2 style={{display: "inline"}}>Cevents</h2>
				<button onClick={() => setAddCeventOverlayVisible(true)} style={{float: "right", display: "inline"}}>Add Cevent</button>
				<Table
					header={ceventsHeaders}
					data={(()=>{
						try{
							return cevents.map(a => Object.values(Object.fromEntries(a.entries())));
						}catch{
							return [];
						}})()}/>
			</AddAccidentForm>
		</>)
}
