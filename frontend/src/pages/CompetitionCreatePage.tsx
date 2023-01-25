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
import ErrorMessageBox from "../components/ErrorMessageBox";
import { BACKEND_URL } from "../helpers/config";
import { Context, useContext } from "../context";
import { useNavigate } from "react-router-dom";

const validationSchema = yup.object({
  name: yup
    .string()
    .required("Please enter a competition name")
    .max(20, "Name must be 20 characters or less"),
  description: yup
    .string()
    .max(250, "Description must be 250 characters or less"),
  maxPointsPerGame: yup
    .number()
    .min(1, "Minimum points per game is 1")
    .required("Please enter the maximum amount of points per game"),
  isPointsModerated: yup
    .bool()
    .required()
});

type inputData = {
  name: string,
  description: string,
  maxPointsPerGame: number,
  isPointsModerated: boolean,
}

const CompetitionCreatePage = () => {
  const [backendError, setBackendError] = React.useState("");
  const context = useContext(Context);
  const navigate = useNavigate();
  const getters = context.getters;

  const doCreateCompetition = async (data: inputData) => {
    const response = await fetch(
      `${BACKEND_URL}/competition/create/v1`, {
        method: "POST",
        headers: {
          "Content-type" : "application/json"
        },
        body: JSON.stringify({
          token: getters.token,
          name: data.name,
          description: data.description,
          is_points_moderated: data.isPointsModerated,
          max_points_per_log: data.maxPointsPerGame
        })
      }
    );

    const res = await response.json();
    if (response.status !== 200) {
      setBackendError(res.message);
    } else {
      navigate(`/competition/${res.comp_id}`);
    }
  };

  return (
    <Box>
      <FormattedPage>
        <Box>
          <Typography component="h4" variant="h4">
            Create a Competition
          </Typography>

          <ErrorMessageBox message={backendError}/>

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
              doCreateCompetition(data);
              setSubmitting(false);
            }}
          >
            {({ values, errors, isSubmitting }) => (
              <Form>
                <Box
                  sx={{
                    mr: 1,
                    display: "inline" 
                  }}
                >
                  <ValidatedTextField placeholder="Competition Name" name="name"/>
                </Box>

                <Box
                  sx={{
                    display: "inline" 
                  }}
                >
                  <ValidatedTextField placeholder="Maximum Points Per Game" type="number" name="maxPointsPerGame" />
                </Box>
                <ValidatedTextArea placeholder="Description (Optional)" name="description" />
                <ValidatedSwitch
                  name="isPointsModerated"
                  label="Points Approval Required?"
                  helperText="Points will need to be approved by a moderator before appearing on the leaderboard with this setting enabled."
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