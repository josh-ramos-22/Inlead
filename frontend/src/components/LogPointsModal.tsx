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

type modalProps = {
  maxPointsPerLog: number,
  isPointsModerated: boolean
}

const LogPointsModal = ( props: modalProps ) => {
  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <Box>
      <Button onClick={handleClickOpen}>
        Log Points
      </Button>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Log Points</DialogTitle>
        <DialogContent>

          { props.isPointsModerated && 
            <DialogContentText>
              Points will require moderator approval before appearing on the leaderboard
            </DialogContentText>
          }
          
          
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleClose}>Submit</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default LogPointsModal;