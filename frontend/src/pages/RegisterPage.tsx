import React from "react";

import Logo from "../components/Logo";
import { Box } from "@mui/material";
import { Typography } from "@mui/material";
import { TextField } from "@mui/material";
import { borderRadius } from "@mui/system";

function RegisterPage() {
  const [backendError, setBackendError] = React.useState(null);


  return (
    <Box
      sx={{
        display: 'flex',
        width: '100vw',
        height: '100vh',
        alignItems: 'center',
        justifyContent: 'center'
      }}
    >
      <Box
      sx = {{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        backgroundColor: 'white',
        width: { xs: '100vw', sm: '400px'},
        height: { xs: '100vh', sm: '500px'},
        borderRadius: { xs: 0, sm: 3},
        justifyContent: 'flex-start'
      }}
    
    >
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
    </Box>
    </Box>
    
    
  )
}

export default RegisterPage;