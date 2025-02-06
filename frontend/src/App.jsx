import react from "react"
import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom";
import Login from "./pages/Login.jsx"
import Register from "./pages/Register.jsx";
import Home from "./pages/Home.jsx";
import NotFound from "./pages/NotFound.jsx";
import Equipment from "./pages/Equipment.jsx";
import Samples from "./pages/Samples.jsx";
import Locations from "./pages/Locations.jsx";
import Inventory from "./pages/Inventory.jsx";
import Tests from "./pages/Tests.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";

function Logout() {
    localStorage.clear()
    return <Navigate to="/login"/>
}

function RegisterAndLogout() {
    localStorage.clear()
    return <Register/>
}

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route
                    path="/"
                    element={
                        <ProtectedRoute>
                            <Home/>
                        </ProtectedRoute>
                    }
                />
                <Route path="/login" element={<Login/>}/>
                <Route path="/logout" element={<Logout/>}/>
                <Route path="/register" element={<RegisterAndLogout/>}/>
                <Route path="/inventory" element={<Inventory/>}/>
                <Route path="/samples" element={<Samples/>}/>
                <Route path="/locations" element={<Locations/>}/>
                <Route path="/equipment" element={<Equipment/>}/>
                <Route path="/tests" element={<Tests/>}/>
                <Route path="*" element={<NotFound/>}></Route>
            </Routes>
        </BrowserRouter>
    )
}

export default App
