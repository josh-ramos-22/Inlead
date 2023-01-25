import React from "react";

import { 
  Box, 
  Button,
  Typography
} from "@mui/material";

import ValidatedTextField from "../components/ValidatedTextField";
import ErrorMessageBox from "../components/ErrorMessageBox";
import FormattedPage from "../components/FormattedPage";

import { Context, useContext } from "../context";
import { useNavigate } from "react-router-dom";

import {
  Formik,
  Form,
} from "formik";

import * as yup from "yup";
import { BACKEND_URL } from "../helpers/config";

const validationSchema = yup.object({
  code: yup
    .number()
    .required("Please enter a competition code")
});

type inputData = {
  code: number 
}

const JoinPage : React.FC = () => {
  const [backendError, setBackendError] = React.useState("");
  const navigate = useNavigate();

  const context = useContext(Context);
  const getters = context.getters;

  const doJoin = async (data : inputData) => {
    const response = await fetch(
      `${BACKEND_URL}/competition/join/v1`, {
        method: "POST",
        headers: {
          "Content-type" : "application/json"
        },
        body: JSON.stringify({
          token: getters.token,
          comp_id: data.code
        })
      }
    );

    const res = await response.json();
    if (response.status !== 200) {
      setBackendError(res.message);
    } else {
      navigate(`/competition/${data.code}`);
    }
  };

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
            alignItems: "center",
            m: 0
          }}
        >
          <Box
            sx = {{
              my: 2,
              mx: 2,
              display: "flex",
              flexDirection: "column",
              alignItems: "center"
            }}
          >
            <Typography component="h1" variant="h4">Join a competition!</Typography>
            <ErrorMessageBox message={backendError}/>

            <Formik
              validateOnChange={true}
              initialValues = {{
                code: 0,
              }}
              validationSchema={validationSchema}
              onSubmit={(data, { setSubmitting }) => {
                setBackendError("");
                setSubmitting(true); // prevents submissions during async call
                doJoin(data);
                setSubmitting(false);
              }}
            >
              {({ values, errors, isSubmitting }) => (
                <Form>
                  <ValidatedTextField placeholder="Competition Code" name="code" type="number"/>
                  <Box sx={{display: "flex", justifyContent: "center"}}>
                    <Button sx={{m: 1, mb: 1}} variant="contained" type="submit" disabled={isSubmitting}>Join</Button>
                  </Box>
                </Form>
              )}
            </Formik>
          </Box>
          
        </Box>


      </FormattedPage>
    </Box>
  );
};

export default JoinPage;