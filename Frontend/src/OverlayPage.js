export function OverlayPage({setTrigger, triggerNewValue, children}){

    return (
        <div style={{width: "100%", height: "100%", position: "absolute", top: "0px", left: "0px", zIndex: "1"}}>
            <div style={{width: "50%", height: "100%", backgroundColor: "rgba(0,0,0,0.5)", top: "0px", left: "0px"}} onClick={()=>setTrigger(triggerNewValue)}/>
            <div style={{width: "50%", height: "100%", backgroundColor: "rgb(0, 150, 0)", top:"0px", right: "0px", position: "absolute"}}>
                {children}
            </div>
        </div>
    );
}