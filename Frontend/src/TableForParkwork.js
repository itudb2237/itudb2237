import {DropdownMenu} from "./DropdownMenu";

let tableStyle = {
    width: '100%',
}

let headerStyle = {
    backgroundColor: '#f5f5f5',
    color: '#000',
    width: '100%',
    position: 'sticky',
    top: '0px'
}

let headerCellStyle = {
    backgroundColor: '#999999',
    color: '#000',
    fontWeight: 'bold',
    fontSize: '1.2em',
    padding: '0.5em',
    textAlign: 'center',
    resize: "horizontal",
    overflow: "auto"
}

let rowStyle = {
    backgroundColor: '#E0E0E0',
    color: '#000',
    width: '100%',
    border: '1px solid #000'
}

let cellStyle = {
    textAlign: 'center',
    border: '1px solid #000'
}

let dict_of_att = {
                "FIRST_HARMFUL_EVENT": [
                     "Rollover/Overturn",
                     "Fire/Explosion",
                     "Immersion",
                     "Gas Inhalation",
                     "Fell/Jumped From Vehicle",
                     "Injured in Vehicle",
                     "Other Non-Collision",
                     "Pedestrian",
                     "Pedalcyclist",
                     "Railway Vehicle",
                     "Live Animal",
                     "Motor Vehicle in Transport",
                     "Motor Vehicle in Transport on Other Roadway",
                     "Parked Motor Vehicle",
                     "Non-Motorist on Personal Conveyance",
                     "Thrown or Falling Object",
                     "Boulder",
                     "Other Object (Not Fixed)",
                     "Building",
                     "Impact Attenuator/Crash Cushion",
                     "Bridge Pier or Support",
                     "Bridge Parapet End",
                     "Bridge Rail",
                     "Guardrail Face",
                     "Concrete Traffic Barrier",
                     "Other Traffic Barrier",
                     "Highway/Traffic Sign Post",
                     "Overhead Sign Support/Sign",
                     "Luminary/Light Support",
                     "Utility Pole/Light Support",
                     "Post, Pole or Other Support",
                     "Culvert",
                     "Curb",
                     "Ditch",
                     "Embankment",
                     "Embankment--Rock, Stone, or Concrete",
                     "Embankment--Material Type Unknown",
                     "Fence",
                     "Wall",
                     "Fire Hydrant",
                     "Shrubbery",
                     "Tree (Standing Only)",
                     "Other Fixed Object",
                     "Pavement Surface Irregularity",
                     "Working Motor Vehicle",
                     "Traffic Signal Support",
                     "Vehicle Occupant Struck or Run Over by Own Vehicle",
                     "Snow Bank",
                     "Ridden Animal or Animal-Drawn Conveyance",
                     "Bridge Overhead Structure",
                     "Jackknife",
                     "Guardrail End",
                     "Mail Box",
                     "Motor Vehicle in Transport Strikes or is Struck by Cargo, Persons or Objects Set-in-Motion From/By Another Motor Vehicle in Transport",
                     "Motor Vehicle in Motion Outside the Trafficway",
                     "Cable Barrier",
                     "Ground",
                     "Traffic Sign Support",
                     "Cargo/Equipment Loss or Shift",
                     "Object That Had Fallen From Motor Vehicle in Transport",
                     "Road Vehicle on Rails",
                     "Unknown Object Not Fixed",
                     "Unknown Fixed Object",
                     "Harmful Event, Details Not Reported",
                     "Reported as Unknown"],
                 "CARGO_BODY_TYPE": [
                     "Not Applicable",
                     "Van/Enclosed Box",
                     "Cargo Tank",
                     "Flatbed",
                     "Dump",
                     "Concrete Mixer",
                     "Auto Transporter",
                     "Garbage/Refuse",
                     "Grain, Chips, Gravel",
                     "Pole-Trailer",
                     "Log",
                     "Intermodal Container Chassis",
                     "Vehicle Towing Another Motor Vehicle",
                     "Bus (Seats 9-15 People, Including Driver)",
                     "Bus (Seats for 16 or More People, Including Driver)",
                     "Bus",
                     "Not Reported",
                     "No Cargo Body Type",
                     "Other",
                     "Unknown Cargo Body Type",
                     "Reported as Unknown"],
                 "SPECIAL_USE": [
                     "No Special Use",
                     "Taxi",
                     "Vehicle Used as School Transport",
                     "Vehicle Used as Other Bus",
                     "Military",
                     "Police",
                     "Ambulance",
                     "Fire Truck",
                     "Non-Transport Emergency Services Vehicle",
                     "Safety Service Patrols--Incident Response",
                     "Other Incident Response ",
                     "Towing--Incident Response",
                     "Incident Response",
                     "Motor Vehicle Used for Vehicle Sharing Mobility",
                     "Motor Vehicle Used for Electronic Ride-Hailing",
                     "Mail Carrier",
                     "Public Utility",
                     "Rental Truck Over 10,000 lbs",
                     "Truck Operating With Crash Attenuator Equipment",
                     "Not Reported",
                    "Reported as Unknown",],
                 "EXTENT_OF_DAMAGE": [
                    "No Damage",
                    "Minor Damage",
                    "Functional Damage",
                    "Disabling Damage",
                    "Not Reported",
                    "Reported as Unknown",]
                }

export function TableForParkwork(props){
    let requestedColumns = props.header;
    let data = props.data;

    let handleChange = (event, index) => {
        let FilterValues = [];
    
        let checkboxes = event.target.form.elements;
    
        for (let i = 0; i < checkboxes.length; i++) {
          if (checkboxes[i].checked) {
            FilterValues.push(checkboxes[i].value);
            console.log(checkboxes[i].value)
          }
        }
        
        props.setHeader([
            ...requestedColumns.slice(0, index),
            {...requestedColumns[index], "filter": FilterValues},
            ...requestedColumns.slice(index+1)
        ]);
    };

    return (
        <table style={tableStyle}>
            <thead style={headerStyle}>
                <tr>
                {requestedColumns.map((element, index) =>
                    <th style={headerCellStyle} key={element["name"] + "_header"}>
                        <DropdownMenu name={element["name"]}>
                            {(() => {
                                if(element["name"] == "FIRST_HARMFUL_EVENT" || element["name"] == "CARGO_BODY_TYPE" || element["name"] == "SPECIAL_USE" || element["name"] == "EXTENT_OF_DAMAGE") {
                                    return (
                                    <form>
                                    {dict_of_att[element["name"]].map((key) => {
                                        return (
                                            <label key={key}>
                                                <input type="checkbox" value={key} onChange={event => handleChange(event,index)} defaultChecked/>
                                                {key}
                                                <br />
                                            </label>
                                        )})}
                                    </form>)
                                }else if(element["name"] == "DEATHS"){
                                        return (
                                        <>
                                            <input
                                                type="number"
                                                placeholder={"Min"}
                                                onChange={a => props.setHeader(
                                                    [
                                                        ...requestedColumns.slice(0, index),
                                                        {...requestedColumns[index], "filter": requestedColumns[index]["filter"] == null ? [a.target.value, null] : [a.target.value, requestedColumns[index]["filter"][1]]},
                                                        ...requestedColumns.slice(index+1)
                                                    ])}
                                            />
                                            <input
                                                type="number"
                                                placeholder={"Max"}
                                                onChange={a => props.setHeader(
                                                    [
                                                        ...requestedColumns.slice(0, index),
                                                        {...requestedColumns[index], "filter": requestedColumns[index]["filter"] == null ? [null, a.target.value] : [requestedColumns[index]["filter"][0], a.target.value]},
                                                        ...requestedColumns.slice(index+1)
                                                    ])}
                                            />
                                        </>
                                    )
                                } else {
                                    return (
                                    <>
                                        <input
                                            type="number"
                                            placeholder={"No..."}
                                            onChange={a => props.setHeader(
                                                [
                                                    ...requestedColumns.slice(0, index),
                                                    {...requestedColumns[index], "filter": requestedColumns[index]["filter"] == null ? [a.target.value, null] : [a.target.value, requestedColumns[index]["filter"][1]]},
                                                    ...requestedColumns.slice(index+1)
                                                ])}
                                        />
                                    </>
                                )
                            }
                            })()}
                        </DropdownMenu>
                    </th>)
                    }
                </tr>
            </thead>
            <tbody>
                {data.map((v, i) => <tr key={i} style={rowStyle}>
                    {v.map((j, i2) =>{
                        console.log(requestedColumns)
                        if(i2 < requestedColumns.length && requestedColumns[i2]["name"] in props.foreignKeys){
                            return (
                            <td key={String(i) + "." + i2} style={cellStyle}>
                                <button
                                    onClick={() => props.foreignKeys[requestedColumns[i2]["name"]](v)}
                                    style={{backgroundColor: 'transparent', border: 'none', color: '#000', padding: '0', cursor: 'pointer'}}
                                >
                                    {j}
                                </button>
                            </td>
                            )
                        }
                        return <td key={String(i) + "." + i2} style={cellStyle}>{j}</td>
                    }
                    )}
                </tr>)}
            </tbody>
        </table>);
}