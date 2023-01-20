import React from "react";

import Logo from "../components/Logo";
import { Box } from "@mui/material";
import { Typography } from "@mui/material";
import { TextField } from "@mui/material";
import Button from "@mui/material/Button";
import { Link } from 'react-router-dom';
import AppEntryBox from "../components/AppEntryBox";

import ValidatedTextField from "../components/ValidatedTextField";

import {
  Formik,
  Field,
  Form,
  useField,
  FieldAttributes,
  FieldArray
} from "formik";

import * as yup from "yup";

const validationSchema = yup.object({
  email: yup
    .string()
    .required("Please enter your email")
    .email('Invalid Email'),
  username: yup
    .string()
    .required("Please enter your username"),
  password: yup
    .string()
    .required('Please enter your password')
})

function LoginPage() {
  const [backendError, setBackendError] = React.useState(null);

  return (
    <AppEntryBox>

      <Logo/>
      <Typography component="h1" variant="h5">Log In</Typography>

      <Box
        sx = {{
          my: 2,
          mx: 2,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center'
        }}
      >
        <Formik
          validateOnChange={true}
          initialValues = {{
            email: "",
            username: "",
            password: "",
          }}
          validationSchema={validationSchema}
          onSubmit={(data, { setSubmitting }) => {
            setSubmitting(true); // prevents submissions during async call
            // make async call
            console.log("submit: ", data);
            setSubmitting(false);
          }}
        >
          {({ values, errors, isSubmitting }) => (
            <Form>
              <ValidatedTextField placeholder="Email" name="email" />
              <ValidatedTextField placeholder="Username" name="username" />
              <ValidatedTextField placeholder="Password" type="password" name="password" />
              <Box sx={{display: 'flex', justifyContent: 'center'}}>
                <Button fullWidth sx={{m: 1, mb: 1}} variant="contained" type="submit" disabled={isSubmitting}>Login</Button>
              </Box>
            </Form>
          )}
        </Formik>
      </Box>

      <Typography sx= {{ fontSize: '10pt', m: 1}}>Need an Account? <Link to="/register">Register here</Link></Typography>
    </AppEntryBox>
  )
}

export default LoginPage;