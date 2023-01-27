import React from "react";

import { Card, Typography, CardContent, Box } from "@mui/material";

type joinProps = {
  compId: number,
}

const JoinCompBox = (props : joinProps) => {
  return (
    <Box sx={{ minWidth: 275, m: 1}}>
      <Card variant="outlined">
        <CardContent
          sx={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            textAlign: "center"
          }}
        >
          <Typography
            sx= {{
              fontSize: "12pt"
            }}
          >
            Join now with code
          </Typography>
          <Typography variant="h1">
            {props.compId}
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default JoinCompBox;