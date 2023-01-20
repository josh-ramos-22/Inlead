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
    .matches(/^[A-Za-z_0-9]+$/, 'Username can only contain numbers, letters and underscores')
    .required("Please enter a username")
    .min(3, 'Username is too short - should be 3 characters minimum')
    .max(10, 'Username is too long - should be at most 10 characters'),
  password: yup
    .string()
    .required('Password is required')
    .matches(
      /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/,
      "Must Contain 8 Characters, One Uppercase, One Lowercase, One Number and One special case Character"
    ),
    // Josh203#
  passwordConfirm: yup
      .string()
      .oneOf([yup.ref('password'), null], "Passwords must match")
})

const RegisterPage : React.FC = () => {
  const [backendError, setBackendError] = React.useState(null);

  return (
    <AppEntryBox>

      <Logo/>
      <Typography component="h1" variant="h5">Create an Account</Typography>

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
            passwordConfirm: ""
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
              <ValidatedTextField placeholder="Confirm Password" type="password" name="passwordConfirm" />
              <Box sx={{display: 'flex', justifyContent: 'center'}}>
                <Button fullWidth sx={{m: 1, mb: 1}} variant="contained" type="submit" disabled={isSubmitting}>Submit</Button>
              </Box>
            </Form>
          )}
        </Formik>
      </Box>


      <Typography sx= {{ fontSize: '10pt', m: 1}}>Already have an account? <Link to="/login">Log in here</Link></Typography>
    </AppEntryBox>
  )
}

export default RegisterPage;