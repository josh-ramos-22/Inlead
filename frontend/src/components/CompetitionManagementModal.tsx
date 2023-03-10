import React from "react";

import {
  Button,
  TextField,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Box,
  Alert,
  Typography
} from "@mui/material";

import { red } from "@mui/material/colors";


import { BACKEND_URL } from "../helpers/config";

import { Context, useContext } from "../context";
import ErrorMessageBox from "./ErrorMessageBox";
import PointsRequestList from "./PointsRequestList";

type modalProps = {
  compId: number,
  isPointsModerated: boolean,
  setLoaded: React.Dispatch<React.SetStateAction<boolean>>
}

const CompetitionManagementModal = ( props: modalProps ) => {
  const [open, setOpen] = React.useState(false);
  const [backendError, setBackendError] = React.useState("");
  const [isEndStaged, setEndStaged] = React.useState(false);
  const context = useContext(Context);
  const getters = context.getters;

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEndStaged(false);
  };

  const doEndComp = async () => {
    const response = await fetch(
      `${BACKEND_URL}/competition/end/v1`, {
        method: "POST",
        headers: {
          "Content-type" : "application/json"
        },
        body: JSON.stringify({
          token: getters.token,
          comp_id: props.compId,
        })
      }
    );

    const res = await response.json();
    if (response.status !== 200) {
      setBackendError(res.message);
    } else {
      props.setLoaded(false);
      handleClose();
    }
  };

  return (
    <Box>
      <Button onClick={handleClickOpen} variant="outlined" sx={{ m: 1 }}>
        Manage
      </Button>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Manage Competition</DialogTitle>

        <DialogContent>
          <Typography sx={{
            mb: 1
          }}>
            Competition Status
          </Typography>
          {!isEndStaged 
            ?
            (
              <Button variant="contained" fullWidth onClick={() => setEndStaged(true)}>
                End Competition
              </Button>
            ) 
            :
            (
              <Box
                sx={{
                  backgroundColor: red[100],
                  p: 2,
                  borderRadius: 3
                }}
              >
                <Alert severity="warning">
                  Are you sure you want to end this competition? This action is irreversible.
                </Alert>

                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "center",
                    m: 1
                  }}
                >
                  <Button onClick={() => setEndStaged(false)}>
                    Cancel
                  </Button>
                  <Button variant="contained" onClick={() => doEndComp()}>
                    End
                  </Button>
                </Box>
              </Box>
            )
          }

          {props.isPointsModerated && 
            <Box>
              <Typography sx={{
                mb: 1,
                mt: 1
              }}>
                Points Requests
              </Typography>
              
              <PointsRequestList compId={props.compId}/>
            </Box>
          }
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default CompetitionManagementModal;