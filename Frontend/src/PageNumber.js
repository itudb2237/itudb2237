import {useRef} from "react";

export function PageNumber(props) {
    let inputRef = useRef(null);
    return (
        <div>
            {props.page > 1 && <button onClick={() => {
                inputRef.current.value = props.page - 1;
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
                ref={inputRef}
            />
            <p style={{display: "inline"}}>
                {"/" + props.pageCount}
            </p>
            {props.page < props.pageCount && <button onClick={() => {
                inputRef.current.value = props.page + 1;
                props.setPage(props.page + 1);
            }}>Next Page</button>}
        </div>
    );
}