import React from "react";

import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Box
} from "@mui/material";

import LoadingScreen from "./LoadingScreen";

import { Context, useContext } from "../context";
import { BACKEND_URL } from "../helpers/config";

type leaderboardProps = {
  compId: number
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
      setParticipants(res.leaderboard);
    }

    setLoaded(true);
  };

  React.useEffect(() => {
    fetchLeaderboard();
  }, []);
  

  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="leaderboard">
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
  );
};

export default Leaderboard;