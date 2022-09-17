import React, { useEffect, useRef } from "react";
import { makeStyles } from "@mui/styles";
import AssignmentIcon from "@mui/icons-material/Assignment";
import WorkOutlineIcon from "@mui/icons-material/WorkOutline";
import { Box, Button, Container, Grid, Paper, Typography } from "@mui/material";
import AssignmentTurnedInIcon from "@mui/icons-material/AssignmentTurnedIn";

import { Card } from "../components/Card";
// import { Table } from "../components/Table";
import { Appbar } from "../components/Appbar";
import { ChartComponent } from "../components/Chart";
import NewTable from "../components/NewTable";
import { getAllData, getLastSeven, startFetchMyQuery } from "../api/api";
import { useState } from "react";

const useStyles = makeStyles({
  headingStyle: {
    height: "10vh",
    alignItems: "center",
    display: "flex",
    marginLeft: "1rem !important",
  },
  dashboardContainer: {
    maxWidth: "100% !important",
    margin: "0px important",
    height: "100vh",
    overflow: "hidden",
  },
  tableStyle: {
    height: "80vh",
  },
  graphStyle: {
    height: "78vh",
    paddingRight: "10px",
  },
  paperStyle: {
    height: "100%",
  },
});

export const Dashboard = ({ user }) => {
  const isFirstRender = useRef(true);
  const [userInfo, setUserInfo] = useState([]);
  const [offset, setOffset] = useState(0);
  const [status, setStatus] = useState(10);
  const [disableButton, setDisableButton] = useState(false);
  const [currentTable, setCurrentTable] = useState([]);
  const [lastWeek, setLastWeek] = useState([]);
  const [allAtten, setAllAtten] = useState([]);
  const classes = useStyles();

  const handleNext = async () => {
    if (status >= offset + 10) {
      setDisableButton(true);
      const response = await startFetchMyQuery(offset + 10);
      if (response?.attendance?.length) {
        setUserInfo([...userInfo, ...response?.attendance]);
        setOffset(offset + 10);
        setCurrentTable(response?.attendance);
        setStatus(status + 10);
      }
      setDisableButton(false);
    } else {
      setCurrentTable(userInfo.slice(status, status + 10));
      setStatus(status + 10);
    }
  };

  const handleBack = () => {
    if (status > 10) {
      setCurrentTable(userInfo.slice(status - 20, status - 10));
      setStatus(status - 10);
    }
  };

  useEffect(() => {
    // FETCH DATA FROM SERVER ON THE FIREST RENDER OF APP
    async function fetchData() {
      const response = await startFetchMyQuery(offset);
      setUserInfo(response?.attendance);
      setCurrentTable(response?.attendance);
      const res = await getLastSeven();
      setLastWeek(res);
      const allAtt = await getAllData();
      setAllAtten(allAtt);
    }
    if (isFirstRender.current) {
      console.log("run");
      isFirstRender.current = false;
      fetchData();
    }
  }, [offset]);

  return (
    <Container className={classes.dashboardContainer} disableGutters>
      <Appbar />
      <Typography variant="h4" component="h2" className={classes.headingStyle}>
        Hi, Welcome {user?.user?.name}
      </Typography>

      <Grid style={{ padding: 0 }} container>
        <Grid item lg={8} className={classes.tableStyle}>
          <Box sx={{ display: { md: "flex" } }} style={{ height: "14vh" }}>
            <Card title1="Job Title" title2={`Juiner Developer`}>
              <WorkOutlineIcon fontSize="large" />
            </Card>
            <Card
              title1={`Task opened:${user?.issue?.opened}`}
              title2={`Task closed:${user?.issue?.total}`}
            >
              <AssignmentIcon fontSize="large" />
            </Card>
            <Card
              title1={`Project opened:${user?.project?.opened}`}
              title2={`Project closed:${user?.project?.total}`}
            >
              <AssignmentTurnedInIcon fontSize="large" />
            </Card>
          </Box>
          <Paper
            elevation={4}
            style={{
              width: "98%",
              margin: "1%",
              height: "54.7vh",
              overflow: "scroll",
            }}
          >
            <NewTable {...{ currentTable }} />
          </Paper>
          <Button
            variant="contained"
            style={{ marginRight: "10px", marginLeft: "10px", float: "right" }}
            onClick={handleNext}
            disabled={disableButton}
          >
            Next
          </Button>
          <Button
            variant="contained"
            style={{ marginRight: "10px", marginLeft: "10px", float: "right" }}
            onClick={handleBack}
          >
            Back
          </Button>
        </Grid>
        <Grid item lg={4} className={classes.graphStyle}>
          <Paper elevation={4} className={classes.paperStyle}>
            <ChartComponent {...{ lastWeek, allAtten }} />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};
