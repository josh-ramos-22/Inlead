import React from "react";

import { 
  Box, 
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Chip
} from "@mui/material";

import prettyPrintDate from "../helpers/datehelpers";

import { useNavigate } from "react-router-dom";

type compProps = {
  comp: {
    comp_id: number,
    name: string,
    is_active: boolean,
    start_time: string
  };
};

const CompetitionLink = (props : compProps) => {
  const comp = props.comp;
  const navigate = useNavigate();

  return (
    <Box sx={{ minWidth: 275, m: 1}}>
      <Card variant="outlined">
        <CardContent>
          <Typography variant="h6">
            {comp.name}
          </Typography>
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-around"
            }}
          >
            <Typography
              sx= {{
                fontSize: "10pt",
                mt: 1
              }}
            >
              Created {prettyPrintDate(comp.start_time)}
            </Typography>
            {
              props.comp.is_active ?
                <Chip label="Inactive" size="small" sx={{ m: 1 }}/>
                :
                <Chip label="Active" color="success" size="small" sx={{ m: 1 }}/>
            }
          </Box>
        </CardContent>
        <CardActions
          sx={{
            display: "flex",
            justifyContent: "center"
          }}
        >
          <Button size="small" onClick={() => navigate(`/competition/${comp.comp_id}`)}>
            Open
          </Button>
        </CardActions>
      </Card>
    </Box>
  );

};

export default CompetitionLink;