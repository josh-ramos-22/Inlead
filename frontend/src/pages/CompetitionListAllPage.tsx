import React from "react";
import { 
  Box,
  Typography 
} from "@mui/material";

import {
  useContext,
  Context
} from "../context";


import FormattedPage from "../components/FormattedPage";
import { BACKEND_URL } from "../helpers/config";
import ErrorMessageBox from "../components/ErrorMessageBox";
import CompetitionLink from "../components/CompetitionLink";
import LoadingScreen from "../components/LoadingScreen";

type reqParams = {
  token: string
}

type compResp = {
  comp_id: number,
  name: string,
  is_active: boolean,
  start_time: string,
}

const CompetitionListAllPage = () => {
  const context = useContext(Context);
  const getters = context.getters;

  const [isLoaded, setLoaded] = React.useState(false);

  const [backendError, setBackendError] = React.useState("");

  const [comps, setComps] = React.useState<compResp[]>([]);

  const fetchCompetitions = async () => {
    const params : reqParams = {
      token: getters.token
    };
    const response = await fetch(
      `${BACKEND_URL}/competitions/list/v1?` + ( new URLSearchParams(params) ), {
        method: "GET",
        headers: {
          "Content-type" : "application/json"
        }
      }
    );
  
    const res = await response.json();
    if (response.status !== 200) {
      setBackendError(res.message);
    } else {
      setComps(res.competitions);
    }

    setLoaded(true);
  };

  React.useEffect(() => {
    fetchCompetitions();
  }, []);

  return (
    <FormattedPage>
      <Typography variant="h4">
        Your Competitions
      </Typography>

      <Box
        sx={{
          display: "flex",
          flexWrap: "wrap",
          m: 1
        }}
      >
        {isLoaded ?
          ( comps.map(comp => <CompetitionLink key={comp.comp_id} comp={comp}/>) )
          :
          ( <LoadingScreen/> )
        }

        
      </Box>

      <ErrorMessageBox message={backendError}/>
    </FormattedPage>
  );
};

export default CompetitionListAllPage;