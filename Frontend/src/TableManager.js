import {useRef} from "react";
import {DropdownMenu} from "./DropdownMenu";

export function TableManager(props) {
    let pageNumberRef = useRef(null);
    let entryPerPageRef = useRef(null);
    return (
        <>
            {props.page > 1 && <button onClick={() => {
                pageNumberRef.current.value = props.page - 1;
                props.setPage(props.page - 1);
            }} >Previous Page</button>}
            <input
                type={"number"}
                id={"pageField"}
                name={"pageCount"}
                defaultValue={props.page}
                onBlur={(event) => {
                    if(event.target.value > props.pageCount){
                        event.target.value = props.pageCount;
                        props.setPage(props.pageCount);
                    }
                    else if(event.target.value < 1){
                        event.target.value = 1;
                        props.setPage(1);
                    }
                    else{
                        props.setPage(Number(event.target.value));
                    }
                }}
                ref={pageNumberRef}
            />
            <p style={{display: "inline"}}>
                {"/" + props.pageCount}
            </p>
            {props.page < props.pageCount && <button onClick={() => {
                pageNumberRef.current.value = props.page + 1;
                props.setPage(props.page + 1);
            }}>Next Page</button>}
            <DropdownMenu name={"Selected Headers"}>
                {props.allColumns.map((i) =>
                    <div key={i + "_selection_row"}>
                        <input
                            type={"checkbox"}
                            id={i + "_checkbox"}
                            key={i + "_checkbox"}
                            checked={props.requestedColumns.some(a => a == i)}
                            onChange={(event) => props.setRequestedColumns(
                                event.target.checked ?
                                    props.allColumns.filter(a => props.requestedColumns.some(b => b == a) || a == i) : props.requestedColumns.filter(a => a != i)
                            )}
                        />
                        <label>{i}</label>
                    </div>)}
            </DropdownMenu>
            <div style={{display: "inline"}}>
                {props.children}
            </div>
            <div style={{float: "right"}}>
                <p style={{display: "inline"}}>Entries per Page: </p>
                <input
                    style={{display: "inline"}}
                    type={"number"}
                    id={"EntryPerPageField"}
                    name={"EntryPerPage"}
                    defaultValue={props.entryPerPage}
                    onBlur={(event) => {
                        props.setEntryPerPage(Number(event.target.value));
                    }}
                    ref={entryPerPageRef}
                />
            </div>
        </>
    );
}