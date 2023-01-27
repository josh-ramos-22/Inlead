
import React from "react";
import FormattedPage from "../components/FormattedPage";
import { 
  Box,
  Typography 
} from "@mui/material";

import { useParams } from "react-router-dom";
import { BACKEND_URL } from "../helpers/config";
import { useContext, Context } from "../context";
import prettyPrintDate from "../helpers/datehelpers";
import LoadingScreen from "../components/LoadingScreen";
import JoinCompBox from "../components/JoinCompBox";
import Leaderboard from "../components/Leaderboard";
import LogPointsModal from "../components/LogPointsModal";
import SuccessMessageBox from "../components/SuccessMessageBox";

type detailParams = {
  comp_id : string,
  token: string
}

const CompetitionPage = () => {
  const { compId } = useParams();
  const context = useContext(Context);
  const getters = context.getters;

  const [backendError, setBackendError] = React.useState("");
  const [joinSuccessMessage, setJoinSuccessMessage] = React.useState("");

  const [isDetailsLoaded, setDetailsLoaded] = React.useState(false);

  const [description, setDescription] = React.useState("");
  const [name, setName] = React.useState("");
  const [startTime, setStartTime] = React.useState("");
  const [endTime, setEndTime] = React.useState("");
  const [maxPointsPerLog, setMaxPointsPerLog] = React.useState(1);
  const [isActive, setActive] = React.useState(true);
  const [isPointsModerated, setIsPointsModerated] = React.useState(false);

  const fetchDetails = async () => {
    const params : detailParams = {
      comp_id: compId ?  compId : "0",
      token: getters.token
    };
    const response = await fetch(
      `${BACKEND_URL}/competition/details/v1?` + ( new URLSearchParams(params) ), {
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
      setName(res.name);
      setDescription(res.description);
      setStartTime(prettyPrintDate(res.start_time));
      setEndTime(res.end_time);
      setMaxPointsPerLog(res.max_points_per_log);
      setActive(res.is_active);
      setIsPointsModerated(res.is_points_moderated);
    }
    setDetailsLoaded(true);
  };

  React.useEffect(() => {
    fetchDetails();
  }, []);

  const logPointsModal = (
    <LogPointsModal compId={Number(compId)} maxPointsPerLog={maxPointsPerLog} isPointsModerated={isPointsModerated} setMessage={setJoinSuccessMessage}/>
  );

  return (
    <FormattedPage>
      <Box
        sx= {{
          height: "100%",
          width: "100%"
        }}
      >
        {
          isDetailsLoaded ?
            (
              <Box
                sx={{
                  display: "flex",
                  justifyContent:"space-between",
                  width: "100%"
                }}
              >
                <SuccessMessageBox message={joinSuccessMessage} setMessage={setJoinSuccessMessage}/>
                <Box
                  sx={{
                    width: "100%"
                  }}
                >
                  <Box
                    sx={{
                      width: "100%",
                      textAlign: { xs: "right", sm: "left"}
                    }}
                  >
                    <Typography
                      sx={{
                        fontSize: { xs: "15pt", sm: "30pt"},
                      }}
                    >
                      {name}
                    </Typography>

                  </Box>

                  <Box
                    sx={{
                      display: { xs: "none", sm: "block"}
                    }}
                  >
                    <Typography>
                      {description}
                    </Typography>

                    <Typography>
                      Created {startTime}.
                    </Typography>

                    {logPointsModal} 
                  </Box>

                </Box>
                <Box
                  sx={{
                    display: { xs: "none", sm: "block" }
                  }}
                >
                  <JoinCompBox compId={Number(compId)} />
                </Box>
                
              </Box>
            )
            :
            (
              <LoadingScreen/>
            )
        }
        <Leaderboard compId={Number(compId)} uId={getters.authUserId}/>
        <Box sx={{
          display: { xs: "flex", sm: "none" },
          justifyContent: "center"
        }}>
          {logPointsModal}
        </Box>
      </Box>

    </FormattedPage>
  );
};

export default CompetitionPage;