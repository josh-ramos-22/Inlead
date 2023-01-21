import { Box, Toolbar } from "@mui/material";
import React from "react";

import Sidebar from "./Sidebar";

const FormattedPage = (props: { children: React.ReactNode }) => {
  return (
    <Box
      sx= {{ display: "flex" }}
    >
      <Sidebar/>
      <Box component="main"
        sx={{ flexGrow: 1, bgcolor: "background.default", p: 3 }}
      >
        <Toolbar/>
        {props.children}
      </Box>
    </Box>
  );
};

export default FormattedPage;