import React from "react";
import { 
  Box,
  Alert
} from "@mui/material";

const ErrorMessageBox = (props : { message: string }) => {
  return (
    <Box sx={{ display: props.message === "" ? 'none' : 'block', width: '80%'}}>
      <Alert severity="error"
        sx = {{
          
          mt: 1,
        }}
      >
        {props.message.replace( /(<([^>]+)>)/ig, '')}
        {/* {props.message} */}
      </Alert>
    </Box>
  )
}

export default ErrorMessageBox;