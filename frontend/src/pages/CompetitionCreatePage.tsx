import React from "react";

import { 
  Box,
  Typography,
  Button,
  FormControlLabel,
  Switch
} from "@mui/material";

import {
  Formik,
  Form,
} from "formik";

import * as yup from "yup";

import ValidatedTextField from "../components/ValidatedTextField";
import ValidatedSwitch from "../components/ValidatedSwitch";

import FormattedPage from "../components/FormattedPage";
import ValidatedTextArea from "../components/ValidatedTextArea";

const validationSchema = yup.object({
  name: yup
    .string()
    .required("Please enter a competition name"),
  description: yup
    .string(),
  maxPointsPerGame: yup
    .number()
    .min(1, "Minimum points per game is 1")
    .required("Please enter the maximum amount of points per game"),
  isPointsModerated: yup
    .bool()
    .required()
});

const CompetitionCreatePage = () => {
  const [backendError, setBackendError] = React.useState("");



  return (
    <Box>
      <FormattedPage>
        <Box>
          <Typography component="h4" variant="h4">
            Create a Competition
          </Typography>

          <Formik
            validateOnChange={true}
            initialValues = {{
              name: "",
              description: "",
              maxPointsPerGame: 1,
              isPointsModerated: false
            }}
            validationSchema={validationSchema}
            onSubmit={(data, { setSubmitting }) => {
              setBackendError("");
              setSubmitting(true); // prevents submissions during async call
              setSubmitting(false);
            }}
          >
            {({ values, errors, isSubmitting }) => (
              <Form>
                <ValidatedTextField placeholder="Competition Name" name="name" />
                <ValidatedTextArea placeholder="Description" name="description" />
                <ValidatedTextField placeholder="Maximum Points Per Game" type="number" name="maxPointsPerGame" />
                <ValidatedSwitch
                  name="isPointsModerated"
                  label="Points Approval Required?"
                  helperText="Points will need to be approved before appearing on the leaderboard with this setting enabled."
                />
                <Box sx={{display: "flex", justifyContent: "center"}}>
                  <Button fullWidth sx={{m: 1, mb: 1}} variant="contained" type="submit" disabled={isSubmitting}>Create</Button>
                </Box>
              </Form>
            )}
          </Formik>
        </Box>
      </FormattedPage>
    </Box>
  );
};

export default CompetitionCreatePage;