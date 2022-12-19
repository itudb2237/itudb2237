import {Table} from "./Table";
import {useEffect, useState} from "react";
import {AddPersonOverlay} from "./People";
import {default as url} from "./backendurl";


async function fetchAndWrite(setValue, requestUrl) {
	let resp = await fetch(requestUrl).then((response) => response.json());
	setValue(resp);
	return resp;
}

export function AddAccident(){
	let [people, setPeople] = useState([]);
	let [peopleHeaders, setPeopleHeaders] = useState([]);
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
			<form>
				<h2>People</h2>
			</form>
			<button onClick={() => setAddPersonOverlayVisible(true)} style={{float: "right", display: "inline"}}>Add Person</button>
			<Table
				header={peopleHeaders}
				data={(()=>{
					try{
						console.log(people)
						console.log(Object.values(Object.fromEntries(people[0].entries())));
						console.log(people.map(a => Object.fromEntries(a.entries())))
						return people.map(a => Object.values(Object.fromEntries(a.entries())));
					}catch{
						return [];
					}})()}/>
			<button onClick={() => {
				for (let person of people){
					fetch(url + "/addPerson", {
						method: "POST",
						body: person
					});
				}
			}} style={{float: "right", display: "inline"}}>Add Accident</button>
		</>)
}
