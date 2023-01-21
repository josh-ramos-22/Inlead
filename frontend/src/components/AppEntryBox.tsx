import React from "react";

import Logo from "../components/Logo";
import { Box } from "@mui/material";
import { Typography } from "@mui/material";
import { TextField } from "@mui/material";
import { borderRadius } from "@mui/system";
import Button from "@mui/material/Button";
import { Link } from "react-router-dom";

function AppEntryBox(props : {children: React.ReactNode}) {
  return (
    <Box
      sx={{
        display: "flex",
        width: "100vw",
        height: "100vh",
        alignItems: "center",
        justifyContent: "center",
        bgcolor: "primary.main"
      }}
    >
      <Box
        sx = {{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          backgroundColor: "white",
          width: { xs: "100vw", sm: "400px"},
          height: { xs: "100vh", sm: "75%"},
          borderRadius: { xs: 0, sm: 3},
          justifyContent: "center",
          boxShadow: "2px 2px 2px 5px rgba(0, 0, 0, 0.2)"
        }}
      > 
        {props.children}
      </Box>
    </Box>
    
    
  );
}

export default AppEntryBox;