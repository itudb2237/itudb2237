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

export function Table(props){
    let requestedColumns = props.header;
    let data = props.data;
    return (
        <table style={tableStyle}>
            <thead style={headerStyle}>
                <tr>
                {requestedColumns.map((element, index) =>
                    <th style={headerCellStyle} key={element["name"] + "_header"}>
                        <DropdownMenu visiblePart={element["name"]}>
                            {(() => {
                                if(element["type"] == "CHAR") {
                                    if(element["possibleValues"] == null) {
                                        return (<input
                                            type="text"
                                            placeholder="Search..."
                                            onChange={a => props.setHeader(
                                                [
                                                    ...requestedColumns.slice(0, index),
                                                    {
                                                        ...requestedColumns[index],
                                                        "filter": a.target.value.length > 0 ? a.target.value : null
                                                    },
                                                    ...requestedColumns.slice(index + 1)
                                                ])}/>)
                                    }else{
                                        return (
                                            <select
                                                onChange={a => props.setHeader(
                                                    [
                                                        ...requestedColumns.slice(0, index),
                                                        {...requestedColumns[index], "filter": a.target.value},
                                                        ...requestedColumns.slice(index+1)
                                                    ])}>
                                                {element["possibleValues"].map((i) =>
                                                    <option key={i} value={i}>{i}</option>)}
                                            </select>)
                                    }
                                }else if(element["type"] == "INTEGER"){
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
                                }
                            })()}
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