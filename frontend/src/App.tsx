import React from "react";
import logo from "./logo.svg";
import "./App.css";

import { Routes, Route, useNavigate } from "react-router-dom";
import { Context, initialValue } from "./context";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { CssBaseline } from "@mui/material/";

import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import JoinPage from "./pages/JoinPage";
import CompetitionCreatePage from "./pages/CompetitionCreatePage";
import { IosShare } from "@mui/icons-material";

import PrivateRoutes from "./helpers/PrivateRoutes";
import AuthRoutes from "./helpers/AuthRoutes";
import { red } from "@mui/material/colors";

const theme = createTheme({
  breakpoints: {
    values: {
      xs: 0,
      sm: 500,
      md: 1400,
      lg: 1200,
      xl: 1536,
    },
  },
  palette: {
    background: {
      default: "white"
    },
    primary: {
      main: red[700]
    }
  },

});


function App() {
  const [token, setToken] = React.useState(initialValue.token);
  const [authUserId, setAuthUserId] = React.useState(initialValue.authUserId);
  
  const getters = { token, authUserId };
  const setters = { setToken, setAuthUserId };

  const navigate = useNavigate();

  return (
    <Context.Provider value={{ getters, setters }}>
      <ThemeProvider theme={theme}>
        <CssBaseline/>
        <Routes>
          <Route element={<AuthRoutes/>}>
            <Route path="/register" element={<RegisterPage/>}/>
            <Route path="/login" element={<LoginPage/>}/>
          </Route>
          <Route element={<PrivateRoutes/>}>
            <Route path="/" element={<JoinPage/>}/>
            <Route path="/competitions/create" element={<CompetitionCreatePage/>}/>
          </Route>
        </Routes>
      </ThemeProvider>
    </Context.Provider>
  );
}

export default App;
