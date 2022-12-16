import {useRef} from "react";

export function DropdownMenu(props) {
    let dropdownRef = useRef(null);
    return (
        <div
            style={{display: "inline-block", outline: "none"}}
            onMouseEnter={() => dropdownRef.current.style.display = "block"}
            onMouseLeave={() => dropdownRef.current.style.display = "none"}
        >
            {props.visiblePart ?? <button>
                {props.name}
            </button>}
            <div ref={dropdownRef} style={{position: "absolute", display: "none", zIndex: "1", backgroundColor: '#f5f5f5'}}>
                {props.children}
            </div>
        </div>
    );
}
