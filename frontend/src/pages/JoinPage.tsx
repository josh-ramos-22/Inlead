import React from "react";

import { Box } from "@mui/material";
import { Typography } from "@mui/material";

import LogoutButton from "../components/LogoutButton";

const JoinPage : React.FC = () => {

  return (
    <Box sx={{
      backgroundColor:"white"
    }}>
      <Typography>Join a competition!</Typography>
      <LogoutButton/>
    </Box>
  )
}

export default JoinPage;