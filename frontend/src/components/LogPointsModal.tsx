import React from "react";

import {
  Button,
  TextField,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Box
} from "@mui/material";
import ValidatedTextField from "./ValidatedTextField";

import {
  Formik,
  Form,
} from "formik";

import * as yup from "yup";
import { BACKEND_URL } from "../helpers/config";

import { Context, useContext } from "../context";
import ErrorMessageBox from "./ErrorMessageBox";

type modalProps = {
  compId: number,
  maxPointsPerLog: number,
  isPointsModerated: boolean,
}

type inputData = {
  points: number
}

const LogPointsModal = ( props: modalProps ) => {
  const [open, setOpen] = React.useState(false);
  const [backendError, setBackendError] = React.useState("");
  const context = useContext(Context);
  const getters = context.getters;

  const validationSchema = yup.object({
    points: yup
      .number()
      .max(props.maxPointsPerLog, `Can log at most ${props.maxPointsPerLog} points`)
      .min(1, "Must log at least 1 point")
      .required("Please enter a competition code")
  });

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const doLogPoints = async (data : inputData) => {
    const response = await fetch(
      `${BACKEND_URL}/points/log/v1`, {
        method: "POST",
        headers: {
          "Content-type" : "application/json"
        },
        body: JSON.stringify({
          token: getters.token,
          comp_id: props.compId,
          points: data.points
        })
      }
    );

    const res = await response.json();
    if (response.status !== 200) {
      setBackendError(res.message);
    } else {
      handleClose();
    }
  };

  return (
    <Box>
      <Button onClick={handleClickOpen}>
        Log Points
      </Button>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Log Points</DialogTitle>

        <Formik
          validateOnChange={true}
          initialValues = {{
            points: 1,
          }}
          validationSchema={validationSchema}
          onSubmit={(data, { setSubmitting }) => {
            setBackendError("");
            setSubmitting(true); // prevents submissions during async call
            doLogPoints(data);
            setSubmitting(false);
          }}
        >
          {({ values, errors, isSubmitting }) => (
            <Form>  

              <DialogContent>
                <ErrorMessageBox message={backendError}/>
                <DialogContentText>
                  Max points loggable: {props.maxPointsPerLog}
                </DialogContentText>
                { props.isPointsModerated && 
                  <DialogContentText>
                    Points will require moderator approval before appearing on the leaderboard
                  </DialogContentText>
                }
                <ValidatedTextField placeholder="Points" name="points" type="number"/>

              </DialogContent>
              <DialogActions>
                <Button onClick={handleClose}>Cancel</Button>
                <Button type="submit" disabled={isSubmitting}>Submit</Button>
              </DialogActions>
            </Form>
          )}
        </Formik>
        
      </Dialog>
    </Box>
  );
};

export default LogPointsModal;