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
  Button,
  ButtonGroup,
  IconButton
} from "@mui/material";


import DoneIcon from "@mui/icons-material/Done";
import CloseIcon from "@mui/icons-material/Close";


import LoadingScreen from "./LoadingScreen";

import { Context, useContext } from "../context";
import { BACKEND_URL } from "../helpers/config";
import prettyPrintDate from "../helpers/datehelpers";
import getOrdinal from "../helpers/ordinal";
import { Done } from "@mui/icons-material";

type leaderboardProps = {
  compId: number,
}

type Participant = {
  u_id: number,
  username: string,
  score: number,
  is_mod: boolean
}

type Request = {
  request_id: number,
  u_id: number,
  points: number,
  username: number
}

type reqParams = {
  token: string,
  comp_id: string,
}

const PointsRequestList = ( props: leaderboardProps ) => {
  const [isLoaded, setLoaded] = React.useState(false);
  const [participants, setParticipants] = React.useState<Participant[]>([]);
  const [requests, setRequests] = React.useState<Request[]>([]);
  const [backendError, setBackendError] = React.useState("");
  const [start, setStart] = React.useState(0);
  const [end, setEnd] = React.useState(-1);
  const [refreshTime, setRefreshTime] = React.useState("");

  const context = useContext(Context);
  const getters = context.getters;

  const doApprove = async (requestId : number) => {
    const response = await fetch(
      `${BACKEND_URL}/points/approve/v1`, {
        method: "POST",
        headers: {
          "Content-type" : "application/json"
        },
        body: JSON.stringify({
          token: getters.token,
          request_id: requestId
        })
      }
    );

    const res = await response.json();
    if (response.status !== 200) {
      alert(res.message);
    } else {
      setLoaded(false);
    }
  };

  const doReject = async (requestId : number) => {
    const response = await fetch(
      `${BACKEND_URL}/points/reject/v1`, {
        method: "POST",
        headers: {
          "Content-type" : "application/json"
        },
        body: JSON.stringify({
          token: getters.token,
          request_id: requestId
        })
      }
    );

    const res = await response.json();
    if (response.status !== 200) {
      alert(res.message);
    } else {
      setLoaded(false);
    }
  };

  const fetchRequestList = async () => {
    const params : reqParams = {
      token: getters.token,
      comp_id: String(props.compId),
    };
    const response = await fetch(
      `${BACKEND_URL}/points/request_list/v1?` + ( new URLSearchParams(params) ), {
        method: "GET",
        headers: {
          "Content-type" : "application/json"
        }
      }
    );
  
    const res = await response.json();
    if (response.status !== 200) {
      setBackendError(res.message);
      setEnd(-1);
    } else {
      setRequests(res.requests);
      setRefreshTime(prettyPrintDate((new Date()).toISOString()));
    } 


    setLoaded(true);
  };

  React.useEffect(() => {
    fetchRequestList();
  }, []);

  React.useEffect(() => {
    fetchRequestList();
  }, [isLoaded]);
  
  React.useEffect(() => {
    const interval = setInterval(() => {
      fetchRequestList();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const refreshBtn = (
    <Button size="small" onClick={() => setLoaded(false)}>
      Refresh
    </Button>
  );

  const requestList = (
    <Box>

      <Box sx={{
        maxHeight: "500px",
        overflowY: "scroll"
      }}>
        <TableContainer component={Paper}>
          <Table sx={{ 
            minWidth: 350,
          }} aria-label="requests">
            <TableHead>
              <TableRow>
                <TableCell>Player</TableCell>
                <TableCell>Points</TableCell>
                <TableCell>Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {requests.map((r, i) => (
                <TableRow
                  key={r.request_id}
                  sx={{ 
                    "&:last-child td, &:last-child th": { border: 0 }, 
                    fontSize: "12pt" 
                  }}
                >
                  <TableCell component="th" scope="row" sx={{ fontSize: "inherit" }}>{r.username}</TableCell>
                  <TableCell sx={{ fontSize: "inherit" }}>{r.points}</TableCell>
                  <TableCell sx={{ fontSize: "inherit" }}>
                    <IconButton 
                      color="success"
                      onClick={() => doApprove(r.request_id)}  
                    >
                      <DoneIcon/>
                    </IconButton>

                    <IconButton
                      color="error"
                      onClick={() => doReject(r.request_id)}
                    >
                      <CloseIcon/>
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
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
      { 
        isLoaded ?
          <>
            <Box sx={{
            }}>
              {requestList}
            </Box>
          </>
          :
          <LoadingScreen/>
      }
    </Box>
  );
};

export default PointsRequestList;