import React from "react";


import IconButton from "@mui/material/Button";
import LogoutIcon from "@mui/icons-material/Logout";
import { Typography } from "@mui/material";

import { BACKEND_URL } from "../helpers/config";
import { useContext, Context } from "../context";
import { useNavigate } from "react-router";

const LogoutButton : React.FC = () => {
  const { getters, setters } = useContext(Context);
  const navigate = useNavigate();

  const doLogout = async () => {
    const response = await fetch(
      `${BACKEND_URL}/auth/logout/v1`, {
        method: "POST",
        headers: {
          "Content-type" : "application/json"
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
      localStorage.setItem("token", "");
      localStorage.setItem("auth_user_id", "");
      setters?.setToken ?.("");
      setters?.setUID?.(-1);
      navigate("/login");
    }
  };

  return (
    <IconButton onClick={() => doLogout()} sx={{ color: "white" }}>
      <LogoutIcon/>
      <Typography sx={{ m: 1 }}>
        Logout
      </Typography>
    </IconButton>
  );
};

export default LogoutButton;