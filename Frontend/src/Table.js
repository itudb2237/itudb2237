let headerStyle = {
    backgroundColor: '#f5f5f5',
    color: '#000',
    width: '100%'
}

let headerCellStyle = {
    backgroundColor: '#f5f5f5',
    color: '#000',
    fontWeight: 'bold',
    fontSize: '1.2em',
    padding: '0.5em',
    textAlign: 'center',
    resize: "horizontal",
    overflow: "auto",
    minWidth: "33%"
}

export function Table(props){
    let header = props.header;
    let data = props.data;
    return (
        <table>
            <thead style={headerStyle}>
                <tr>
                {header.map((i) => <th style={headerCellStyle} key={i}>{i}</th>)}
                </tr>
            </thead>
        </table>);
}