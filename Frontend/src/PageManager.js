import {useRef} from "react";

export function PageManager(props) {
    let pageNumberRef = useRef(null);
    let entryPerPageRef = useRef(null);
    return (
        <div>
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
                onKeyUp={(event) => {
                    if (event.keyCode == 13) {
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
                    }
                }}
            />
            <p style={{display: "inline"}}>
                {"/" + props.pageCount}
            </p>
            {props.page < props.pageCount && <button onClick={() => {
                pageNumberRef.current.value = props.page + 1;
                props.setPage(props.page + 1);
            }}>Next Page</button>}
            <p style={{display: "inline", float: "right"}}>Entries per Page: </p>
            <input
                style={{display: "inline", float: "right"}}
                type={"number"}
                id={"EntryPerPageField"}
                name={"EntryPerPage"}
                defaultValue={props.entryPerPage}
                onBlur={(event) => {
                    props.setEntryPerPage(Number(event.target.value));
                }}
                ref={entryPerPageRef}
                onKeyUp={(event) => {
                    if (event.keyCode == 13) {
                        props.setEntryPerPage(Number(event.target.value))
                    }
                }}
            />
        </div>
    );
}