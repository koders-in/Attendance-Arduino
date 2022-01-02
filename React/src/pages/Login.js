import React from "react";
import { makeStyles } from "@mui/styles";
import {
  Grid,
  Paper,
  Box,
  TextField,
  CardMedia,
  Button,
  Typography,
} from "@mui/material";
import logo from "../assets/images/koders.webp";

const useStyles = makeStyles({
  root: {
    height: "100vh",
  },
  inner: {
    width: "50%",
    height: "60%",
  },
  loginPaper: {
    width: "100%",
    height: "100%",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    flexDirection: "column",
  },
  textfield: {
    margin: "0 0 20px 0 !important",
    width: "25rem",
  },
  logostyle: {
    width: "100px !important",
    height: "100px",
    marginBottom: "7%",
  },
  button: {
    width: "20rem !important",
  },
});
export const Login = ({ handleChange, handleSubmit }) => {
  const classes = useStyles();

  return (
    <Grid
      className={classes.root}
      justifyContent="center"
      alignItems="center"
      container
    >
      {/* <LoginModal /> */}
      <Grid className={classes.inner} item>
        <Paper className={classes.loginPaper} elevation={6}>
          <Box
            component="form"
            onSubmit={handleSubmit}
            autoComplete="off"
            className={classes.loginPaper}
          >
            <CardMedia
              component="img"
              src={logo}
              className={classes.logostyle}
            />
            <Typography
              variant="h5"
              component="h2"
              style={{ color: "#00ab9c" }}
            >
              Attendence System
            </Typography>

            <TextField
              required
              id="outlined-required"
              label="Username"
              name="username"
              className={classes.textfield}
              onChange={handleChange}
            />
            <TextField
              className={classes.textfield}
              type="password"
              required
              id="outlined-disabled"
              label="Password"
              onChange={handleChange}
              name="password"
            />
            <Button
              size="large"
              variant="contained"
              className={classes.button}
              type="submit"
            >
              Log In
            </Button>
          </Box>
        </Paper>
      </Grid>
    </Grid>
  );
};
