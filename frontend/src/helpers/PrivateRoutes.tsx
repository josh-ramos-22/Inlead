// Source: https://medium.com/@dennisivy/creating-protected-routes-with-react-router-v6-2c4bbaf7bc1c

import React from "react";

import { Navigate, Outlet } from "react-router-dom";

import { useContext, Context } from "../context";

const PrivateRoutes = ()  => {
  const context = useContext(Context);
  const token = context.getters.token;
  
  return (
    token ? <Outlet/> : <Navigate to="/login"/>
  );
};

export default PrivateRoutes;