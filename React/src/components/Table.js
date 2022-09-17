import React from "react";
import { DataGrid } from "@mui/x-data-grid";
import { makeStyles } from "@mui/styles";

const useStyles = makeStyles({
  tableStyle: {
    height: "25rem !important",
    width: "100% !important",
  },
});

export const Table = ({ rows }) => {
  let data = rows.attendance;
  let temp = [];
  for (let i = data?.length - 1; i >= 0; i--) {
    let dateObj = new Date(`${data[i].date}`);
    let forIn = [],
      forOut = [];
    if (data[i].clock_in) {
      forIn = new Date(`${data[i].date}T${data[i].clock_in}.000Z`)
        .toLocaleString(undefined, { timeZone: "Asia/Kolkata" })
        .split(" ");
    }
    if (data[i].clock_out) {
      forOut = new Date(`${data[i].date}T${data[i].clock_out}.000Z`)
        .toLocaleString(undefined, { timeZone: "Asia/Kolkata" })
        .split(" ");
    }

    temp.push({
      ...data[i],
      date: dateObj.toDateString(),
      clock_in: forIn?.length ? forIn[1] + ":" + forIn[2] : null,
      clock_out: forOut.length ? forOut[1] + ":" + forOut[2] : null,
    });
  }

  const classes = useStyles();
  return (
    <DataGrid
      sx={{ width: "100%" }}
      rows={temp || []}
      columns={columns}
      pageSize={6}
      rowsPerPageOptions={[8]}
      className={classes.tableStyle}
    />
  );
};

const columns = [
  { field: "date", headerName: "Date", width: 1005 / 5 + 10 },
  {
    field: "clock_in",
    headerName: "Morning (11:10-02:00)",
    width: 1005 / 5 + 10,
  },
  {
    field: "clock_out",
    headerName: "Evening (03:10-07:00)",
    width: 1005 / 5 + 10,
  },
  {
    field: "comment",
    headerName: "Remark",

    width: 1005 / 5 + 10,
  },
];
