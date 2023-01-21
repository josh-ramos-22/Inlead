import React from "react";

import { Box } from "@mui/material";
import { Typography } from "@mui/material";

import LogoutButton from "../components/LogoutButton";
import FormattedPage from "../components/FormattedPage";

const JoinPage : React.FC = () => {

  return (
    <Box sx={{
      backgroundColor:"white"
    }}>
      <FormattedPage>
        <Box
          sx={{
            width: "100%",
            height: "100%",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            m: 0
          }}
        >
          <Typography component="h1" variant="h4">Join a competition!</Typography>
        </Box>


      </FormattedPage>
    </Box>
  );
};

export default JoinPage;