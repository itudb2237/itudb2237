let headerStyle = {
    backgroundColor: "#00adee",
    color: "white",
    padding: "10px",
    display: "flex",
    justifyContent: "space-between"
}

let buttonStyle = {
    backgroundColor: "black",
    color: "inherit",
    padding: "5px",
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
        </header>
    );
}