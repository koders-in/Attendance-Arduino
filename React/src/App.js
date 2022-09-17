import React, { useState, createContext } from "react";
import { createTheme, ThemeProvider, CssBaseline } from "@mui/material";

import { Login } from "./pages/Login";
import { startFetchMyQuery } from "./api/api";
import { Dashboard } from "./pages/Dashboard";

import "./App.css";

export const UseContext = createContext("");

function App() {
  const [mode, setMode] = useState("light");
  const [user, setUser] = useState({});
  const [data, setData] = useState({
    username: "",
    password: "",
  });

  // CHANGE THEME
  const theme = React.useMemo(
    () =>
      createTheme({
        palette: {
          mode,
        },
      }),
    [mode]
  );

  // EXECUTE ON LOGIN BUTTON PRESS
  const handleSubmit = async (event) => {
    event.preventDefault();
    // const params = data;
    // const result = await getRequest({ params });
    setUser({ ...dummyData });
  };

  // CHANGE MODE
  const handleMode = () => {
    setMode((pre) => (pre === "light" ? "dark" : "light"));
  };

  // UPDATE STATE
  const handleChange = (event) => {
    const { name, value } = event.target;
    setData((pre) => {
      return { ...pre, [name]: value };
    });
  };

  if (Object.keys(user)?.length === 0) {
    return <Login {...{ handleChange, handleSubmit }} />;
  }
  return (
    <UseContext.Provider value={{ handleMode }}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div style={{ margin: 0, padding: 0 }} className="App">
          <Dashboard {...{ user }} />
        </div>
      </ThemeProvider>
    </UseContext.Provider>
  );
}

export default App;

const dummyData = {
  user: {
    name: "Saksham Chauhan",
    user_id: 72,
  },
  project: {
    opened: 2,
    total: 2,
  },
  issue: {
    opened: 3,
    total: 18,
  },
  spent_time: {
    "31/12/2021": 0,
    "30/12/2021": 8.0,
    "29/12/2021": 0,
    "28/12/2021": 8.0,
    "27/12/2021": 8.0,
    "26/12/2021": 0,
    "25/12/2021": 0,
  },
};
