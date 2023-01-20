import React from "react";

import Logo from "../components/Logo";
import { Box } from "@mui/material";
import { Typography } from "@mui/material";
import { TextField } from "@mui/material";
import Button from "@mui/material/Button";
import { Link } from 'react-router-dom';
import AppEntryBox from "../components/AppEntryBox";

function RegisterPage() {
  const [backendError, setBackendError] = React.useState(null);

  return (
    <AppEntryBox>

      <Logo/>
      <Typography component="h1" variant="h5">Create an Account</Typography>

      <Box component="form"
        sx = {{
          my: 2,
          mx: 2,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center'
        }}
      >
        <TextField
          margin="normal"
          required
          // fullWidth
          id="email"
          label="Email"
        />

        <TextField
          margin="normal"
          required
          // fullWidth
          id="username"
          label="Username"
        />

        <TextField
          margin="normal"
          required
          // fullWidth
          id="password"
          label="Password"
          type="password"
        />

        <TextField
          margin="normal"
          required
          // fullWidth
          id="password-confirm"
          label="Confirm Password"
          type="password"
        />
      </Box>

      <Button sx={{m: 1, mb: 1}} variant="contained">Submit</Button>

      <Typography sx= {{ fontSize: '10pt', m: 1}}>Already have an account? <Link to="/login">Log in here</Link></Typography>
    </AppEntryBox>
  )
}

export default RegisterPage;