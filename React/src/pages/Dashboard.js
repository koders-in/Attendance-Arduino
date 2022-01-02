import { Box, Container, Grid, Paper, Typography } from "@mui/material";
import { makeStyles } from "@mui/styles";
import React from "react";
import { ChartComponent } from "../components/Chart";
import { Appbar } from "../components/Appbar";
import WorkOutlineIcon from "@mui/icons-material/WorkOutline";
import AssignmentIcon from "@mui/icons-material/Assignment";
import AssignmentTurnedInIcon from "@mui/icons-material/AssignmentTurnedIn";

import { Table } from "../components/Table";
import { Card } from "../components/Card";

const useStyles = makeStyles({
  tableStyle: {
    height: "fitContent",
  },
  paperStyle: {
    margin: "1%",
  },
  dashboardContainer: {
    maxWidth: "100% !important",
    margin: "0px important",
  },
});

export const Dashboard = ({ user }) => {
  const classes = useStyles();
  console.log(user);
  return (
    <Container className={classes.dashboardContainer} disableGutters>
      <Appbar />
      <Typography
        variant="h4"
        component="h2"
        style={{ marginLeft: "2%", marginTop: "2%", marginBottom: "2%" }}
      >
        Hi, Welcome {user.user.name}
      </Typography>

      <Grid style={{ padding: 0 }} container>
        <Grid item lg={8}>
          <Box sx={{ display: { md: "flex" } }}>
            <Card title1="Job Title">
              <WorkOutlineIcon fontSize="large" />
            </Card>
            <Card
              title1={`Task opened:${user.issue.opened}`}
              title2={`Task closed:${user.issue.total}`}
            >
              <AssignmentIcon fontSize="large" />
            </Card>
            <Card
              title1={`Project opened:${user.project.opened}`}
              title2={`Project closed:${user.project.total}`}
            >
              <AssignmentTurnedInIcon fontSize="large" />
            </Card>
          </Box>
          <Paper elevation={4} style={{ width: "98%", margin: "1%" }}>
            <Table />
          </Paper>
        </Grid>
        <Grid item lg={4} className={classes.tableStyle}>
          <Paper elevation={4} className={classes.paperStyle}>
            <ChartComponent data={user.spent_time} />
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
