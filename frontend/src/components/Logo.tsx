import React from "react";
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';
import { Box, Typography } from "@mui/material";

function Logo() {
  return (
    <Box
      sx={{
        display: 'flex',
        color: 'red',
        fontSize: '40px',
        m: 1
      }}
    >
      <EmojiEventsIcon sx={{ mt: 1, fontSize: 'inherit'}}/>
      <Typography sx={{ fontSize: 'inherit', mr: 1}}>Inlead</Typography>
    </Box>

  )
}

export default Logo;