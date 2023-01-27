import React from "react";

import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Box,
  Typography,
  Fade,
  Button
} from "@mui/material";

import LoadingScreen from "./LoadingScreen";

import { Context, useContext } from "../context";
import { BACKEND_URL } from "../helpers/config";
import prettyPrintDate from "../helpers/datehelpers";
import getOrdinal from "../helpers/ordinal";

type leaderboardProps = {
  compId: number,
  uId: number
}

type Participant = {
  u_id: number,
  username: string,
  score: number,
  is_mod: boolean
}

type reqParams = {
  token: string,
  comp_id: string,
  start: string
}



const Leaderboard = ( props: leaderboardProps ) => {
  const [isLoaded, setLoaded] = React.useState(false);
  const [participants, setParticipants] = React.useState<Participant[]>([]);
  const [backendError, setBackendError] = React.useState("");
  const [start, setStart] = React.useState(0);
  const [end, setEnd] = React.useState(-1);
  const [refreshTime, setRefreshTime] = React.useState("");
  const [position, setPosition] = React.useState(-1);
  const [score, setScore] = React.useState(-1);

  const context = useContext(Context);
  const getters = context.getters;


  const fetchLeaderboard = async () => {
    const params : reqParams = {
      token: getters.token,
      comp_id: String(props.compId),
      start: String(start)
    };
    const response = await fetch(
      `${BACKEND_URL}/competition/leaderboard/v1?` + ( new URLSearchParams(params) ), {
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
      const pos = (res.leaderboard as Participant[]).findIndex(p => 
      {return p.u_id == getters.authUserId;} 
      ) + 1;

      setScore(res.leaderboard[pos - 1].score);
      setParticipants(res.leaderboard);
      setRefreshTime(prettyPrintDate((new Date()).toISOString()));
      setPosition(pos);
      
    } 


    setLoaded(true);
  };

  React.useEffect(() => {
    fetchLeaderboard();
  }, []);

  React.useEffect(() => {
    fetchLeaderboard();
  }, [isLoaded]);
  
  React.useEffect(() => {
    const interval = setInterval(() => {
      fetchLeaderboard();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const refreshBtn = (
    <Button size="small" onClick={() => setLoaded(false)}>
      Refresh
    </Button>
  );

  const fullLeaderboard = (
    <Box>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 350 }} aria-label="leaderboard">
          <TableHead>
            <TableRow>
              <TableCell>Rank</TableCell>
              <TableCell>Player</TableCell>
              <TableCell>Score</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {participants.map((p, i) => (
              <TableRow
                key={p.u_id}
                sx={{ 
                  "&:last-child td, &:last-child th": { border: 0 }, 
                  fontSize: "15pt" 
                }}
              >
                <TableCell component="th" scope="row" sx={{ fontSize: "inherit" }}>{i + 1}</TableCell>
                <TableCell sx={{ fontSize: "inherit" }}>{p.username}</TableCell>
                <TableCell sx={{ fontSize: "inherit" }}>{p.score}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between"
        }}
      >
        {refreshBtn}
        <Fade in={isLoaded}>
          <Typography sx={{ m: 1 }}>
            Last Refreshed: {refreshTime}
          </Typography>
        </Fade>
      </Box>
    </Box>
  );

  return (
    <Box
      sx={{
        m: 2
      }}
    >
      <Box sx={{
        display: { xs: "none", sm: "block" }
      }}>
        {fullLeaderboard}
      </Box>
      <Box sx={{
        display: { xs: "flex", sm: "none" },
        justifyContent: "center",
        textAlign: "center",
        flexDirection: "column",
        alignItems: "center",
      }}>
        <Typography variant="h5">
          You are in
        </Typography>
        <Typography variant="h1">
          {position}{getOrdinal(position)}
        </Typography>
        <Typography variant="h5">
          place with {score} points
        </Typography>
        {refreshBtn}
      </Box>
    </Box>
  );
};

export default Leaderboard;