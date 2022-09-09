import * as React from "react";
import IconButton from "@mui/material/IconButton";
import { Box } from "@mui/material";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";

export const Toggler = (p) => {
  return (
    <Box
      sx={{
        display: "flex",
        width: "100%",
        alignItems: "center",
        justifyContent: "center",
        color: "text.primary",
        borderRadius: 1,
        p: 1,
      }}
    >
      <IconButton sx={{ ml: 1 }}>
        {true ? <Brightness7Icon /> : <Brightness4Icon />}
      </IconButton>
    </Box>
  );
};
