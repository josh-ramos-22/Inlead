import React from "react";


import IconButton from "@mui/material/Button";
import LogoutIcon from '@mui/icons-material/Logout';

import { BACKEND_URL } from '../helpers/config';
import { useContext, Context } from '../context';
import { useNavigate } from "react-router";

const LogoutButton : React.FC = () => {
  const { getters, setters } = useContext(Context);
  const navigate = useNavigate();

  const doLogout = async () => {
    const response = await fetch(
      `${BACKEND_URL}/auth/logout/v1`, {
        method: 'POST',
        headers: {
          'Content-type' : 'application/json'
        },
        body: JSON.stringify({
          token: getters.token
        })
      }
    );

    const res = await response.json();
    if (response.status !== 200) {
      alert(res.message);
    } else {
      localStorage.setItem('token', '')
      setters?.setToken ?.('');
      setters?.setUID?.(-1);
      navigate('/login');
    }
  }

  return (
    <IconButton onClick={() => doLogout()}>
      <LogoutIcon/>
    </IconButton>
  )
}

export default LogoutButton;