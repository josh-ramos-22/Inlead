import React from "react";

import {
  Box,
  CircularProgress
} from "@mui/material";

const LoadingScreen = () => {
  return (
    <Box
      sx={{
        height: "100%",
        width : "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
      }}
    >
      <CircularProgress/>
    </Box>
  );
};

export default LoadingScreen;