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
    backgroundColor: '#f5f5f5',
    color: '#000',
    fontWeight: 'bold',
    fontSize: '1.2em',
    padding: '0.5em',
    textAlign: 'center',
    resize: "horizontal",
    overflow: "horizontal"
}

let rowStyle = {
    backgroundColor: '#814',
    color: '#000',
    width: '100%',
    border: '1px solid #000'
}

let cellStyle = {
    textAlign: 'center',
    border: '1px solid #000'
}

export function Table(props){
    let header = props.header;
    let data = props.data;
    return (
        <table style={tableStyle}>
            <thead style={headerStyle}>
                <tr>
                {header.map((i) =>
                    <th style={headerCellStyle} key={i["name"] + "_header"}>
                        <DropdownMenu visiblePart={i["name"]}>
                            <p>asd</p>
                        </DropdownMenu>
                    </th>)
                    }
                </tr>
            </thead>
            <tbody>
                {data.map((v, i) => <tr key={i} style={rowStyle}>{v.map((j, i2) => <td key={String(i) + "." + i2} style={cellStyle}>{j}</td>)}</tr>)}
            </tbody>
        </table>);
}