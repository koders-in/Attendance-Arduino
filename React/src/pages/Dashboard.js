import React from "react";
import { makeStyles } from "@mui/styles";
import AssignmentIcon from "@mui/icons-material/Assignment";
import WorkOutlineIcon from "@mui/icons-material/WorkOutline";
import { Box, Container, Grid, Paper, Typography } from "@mui/material";
import AssignmentTurnedInIcon from "@mui/icons-material/AssignmentTurnedIn";

import { Card } from "../components/Card";
import { Table } from "../components/Table";
import { Appbar } from "../components/Appbar";
import { ChartComponent } from "../components/Chart";

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
  const classes = useStyles();
  console.log(user);

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
            style={{ width: "98%", margin: "1%", height: "62.7vh" }}
          >
            <Table />
          </Paper>
        </Grid>
        <Grid item lg={4} className={classes.graphStyle}>
          <Paper elevation={4} className={classes.paperStyle}>
            <ChartComponent data={user?.spent_time} />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

// {
//   "user":{
//      "name":"Saksham Chauhan",
//      "user_id":72
//   },
//   "project":{
//      "opened":2,
//      "total":2
//   },
//   "issue":{
//      "opened":3,
//      "total":18
//   },
//   "spent_time":{
//      "31/12/2021":0,
//      "30/12/2021":8.0,
//      "29/12/2021":0,
//      "28/12/2021":8.0,
//      "27/12/2021":8.0,
//      "26/12/2021":0,
//      "25/12/2021":0
//   }
// }
