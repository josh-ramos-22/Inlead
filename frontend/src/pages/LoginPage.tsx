import React from "react";

import Logo from "../components/Logo";
import { Box } from "@mui/material";
import { Typography } from "@mui/material";
import Button from "@mui/material/Button";
import { Link } from 'react-router-dom';
import AppEntryBox from "../components/AppEntryBox";

import ValidatedTextField from "../components/ValidatedTextField";

import { BACKEND_URL } from '../helpers/config';
import { useContext, Context } from '../context';
import ErrorMessageBox from "../components/ErrorMessageBox";
import { useNavigate } from "react-router-dom";

import {
  Formik,
  Form,
} from "formik";

import * as yup from "yup";

type inputData = {
  email: string;
  password: string;
}

const validationSchema = yup.object({
  email: yup
    .string()
    .required("Please enter your email")
    .email('Invalid Email'),
  password: yup
    .string()
    .required('Please enter your password')
})

function LoginPage() {
  const [backendError, setBackendError] = React.useState("");

  const navigate = useNavigate();

  const context = useContext(Context);
  const setters = context.setters;

  const doRegister = async (data : inputData) => {
    const response = await fetch(
      `${BACKEND_URL}/auth/login/v1`, {
        method: 'POST',
        headers: {
          'Content-type' : 'application/json'
        },
        body: JSON.stringify({
          email: data.email,
          password: data.password
        })
      }
    );

    const res = await response.json();
    if (response.status !== 200) {
      setBackendError(res.message);
    } else {
      localStorage.setItem('token', res.token);
      localStorage.setItem('auth_user_id', res.auth_user_id);
      setters?.setToken ?.(res.token);
      setters?.setUID?.(res.auth_user_id);
      navigate('/');
    }
  }

  return (
    <AppEntryBox>

      <Logo/>
      <Typography component="h1" variant="h5">Log In</Typography>
      <ErrorMessageBox message={backendError}/>

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
            password: "",
          }}
          validationSchema={validationSchema}
          onSubmit={(data, { setSubmitting }) => {
            setSubmitting(true); // prevents submissions during async call
            doRegister(data);
            setSubmitting(false);
          }}
        >
          {({ values, errors, isSubmitting }) => (
            <Form>
              <ValidatedTextField placeholder="Email" name="email" />
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