import React from "react";
import { 
  Box,
  Alert,
  Button,
  Paper,
  Fade
} from "@mui/material";

type messageBoxProps = { 
  message: string, 
  setMessage: React.Dispatch<React.SetStateAction<string>>
};

const SuccessMessageBox = (props : messageBoxProps ) => {
  return (
    <Fade in={props.message !== ""}>
      <Box sx={{ 
        display: props.message === "" ? "none" : "flex", 
        position: "fixed",
      }}>
        <Alert severity="success"
          sx = {{
            m: 1,
            boxShadow: 3
          }}
          action={
            <Button color="inherit" size="small" onClick={() => props.setMessage("")}>
              X
            </Button>
          }
        >
          {props.message}
        </Alert>
      </Box>
    </Fade>
  );
};

export default SuccessMessageBox;