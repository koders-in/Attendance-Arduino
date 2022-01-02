import React, { useState, createContext } from "react";
import { createTheme, ThemeProvider, CssBaseline } from "@mui/material";
import { Dashboard } from "./pages/Dashboard";
import { Login } from "./pages/Login";
import "./App.css";
import { getRequest } from "./config/server";

export const UseContext = createContext("");

function App() {
  const [mode, setmode] = useState("light");
  const [user, setUser] = useState({});
  const [data, setData] = useState({
    username: "",
    password: "",
  });
  const theme = React.useMemo(
    () =>
      createTheme({
        palette: {
          mode,
        },
      }),
    [mode]
  );

  const handleSubmit = async (event) => {
    event.preventDefault();
    const params = data;
    const result = await getRequest({ params });
    setUser(result.data);
    console.log(user);
  };
  const handleMode = () => {
    setmode((pre) => (pre === "light" ? "dark" : "light"));
  };
  const handleChange = (event) => {
    const { name, value } = event.target;
    setData((pre) => {
      return { ...pre, [name]: value };
    });
  };

  if (Object.keys(user).length === 0) {
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
