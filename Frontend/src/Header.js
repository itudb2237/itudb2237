let headerStyle = {
    backgroundColor: "#302F2A",
    color: "white",
    padding: "10px",
    display: "flex",
    justifyContent: "space-between"
}

let buttonStyle = {
    backgroundColor: "#1D1C1A",
    color: "inherit",
    padding: "10px",
    borderRadius: "5px",
    border: "none",
    textDecoration: "none"
}

export function Header(){
    return(
        <header style={headerStyle}>
            <a href={"./accidents"} style={buttonStyle}>Accidents</a>
            <a href={"./people"} style={buttonStyle}>People</a>
            <a href={"./cevents"} style={buttonStyle}>Cevents</a>
            <a href={"./vehicles"} style={buttonStyle}>Vehicles</a>
            <a href={"./parkworks"} style={buttonStyle}>Parkworks</a>
            <a href={"./pbtypes"} style={buttonStyle}>PbTypes</a>
            <a href={"./vehAuxes"} style={buttonStyle}>VehAuxes</a>
            <a href={"./add_accident"} style={buttonStyle}>Add Accident</a>
        </header>
    );
}