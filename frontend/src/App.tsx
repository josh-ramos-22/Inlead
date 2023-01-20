import React from 'react';
import logo from './logo.svg';
import './App.css';

import { Routes, Route, useNavigate } from 'react-router-dom';
import { Context, initialValue } from './context';

function App() {
  const [token, setToken] = React.useState(initialValue.token);
  const [authUserId, setAuthUserId] = React.useState(initialValue.authUserId);
  
  const getters = { token, authUserId };
  const setters = { setToken, setAuthUserId };

  const navigate = useNavigate();

  return (
    <Context.Provider value={{ getters, setters }}>
      <Routes>
        <Route path="/register" element={<div>Register Page</div>}/>
      </Routes>
    </Context.Provider>
  );
}

export default App;
