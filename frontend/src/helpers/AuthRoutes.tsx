import React from "react";

import { Navigate, Outlet } from "react-router-dom";

import { useContext, Context } from "../context";

const AuthRoutes = ()  => {
  const context = useContext(Context);
  const token = context.getters.token;
  
  return (
    token ? <Navigate to="/"/> : <Outlet/>
  );
};

export default AuthRoutes;