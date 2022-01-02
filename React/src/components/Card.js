import React from "react";
import { Paper, Box, Typography } from "@mui/material";
// import { makeStyles } from "@mui/styles";

// const useStyle = makeStyles({
//   paperStyle: {
//     maxWidth: "33% !important",
//   },
// });

export const Card = (p) => {
  //   const classes = makeStyles();
  return (
    <Paper style={{ width: "33%", margin: "1%", padding: "2%" }} elevation={4}>
      <Box
        display="flex"
        style={{
          padding: "2%",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {p.children}
        <Box
          display="flex"
          flexDirection="column"
          style={{ marginLeft: "18%" }}
        >
          <Typography variant="h6" component="h6">
            {p.title1}
          </Typography>
          <Typography variant="h6" component="h6">
            {p.title2}
          </Typography>
        </Box>
      </Box>
    </Paper>
  );
};
