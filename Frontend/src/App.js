import {Header} from "./Header";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Accidents } from "./Accidents";
import { People } from "./People";
import { Cevents } from "./Cevents";
import { Vehicles } from "./Vehicles";
import { Parkworks } from "./Parkworks";
import { Pbtypes } from "./Pbtypes";
import { Login } from "./login"
import "./loginbutton.css";


export function App(){
    return (
        <>
            <a href={"./login"} className="loginbutton">Log In</a>
            <Header/>
            <BrowserRouter>
                <Routes>
                    <Route index path="/accidents" element={<Accidents/>}/>
                    <Route path="/people" element={<People/>}/>
                    <Route path="/cevents" element={<Cevents/>}/>
                    <Route path="/vehicles" element={<Vehicles/>}/>
                    <Route path="/parkworks" element={<Parkworks/>}/>
                    <Route path="/pbtypes" element={<Pbtypes/>}/>
                    <Route path="/login" element={<Login/>}/>
                </Routes>
            </BrowserRouter>
        </>);
}
