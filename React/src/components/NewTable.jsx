import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

export default function NewTable({ currentTable }) {
  const getTimeInIST = (date, time) => {
    let forIn = [];
    if (time) {
      forIn = new Date(`${date}T${time}.000Z`)
        .toLocaleString(undefined, { timeZone: "Asia/Kolkata" })
        .split(" ");
    }
    return forIn?.length ? forIn[1] + ":" + forIn[2] : "";
  };

  const getDateInIST = (date) => {
    let dateObj = new Date(date);
    return dateObj.toDateString();
  };

  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell align="center">Date</TableCell>
            <TableCell align="center">Clock In</TableCell>
            <TableCell align="center">Clock Out</TableCell>
            <TableCell align="center">Remark</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {currentTable?.length ? (
            currentTable.map((row) => (
              <TableRow
                key={row.clock_in}
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell align="center">{getDateInIST(row.date)}</TableCell>
                <TableCell align="center">
                  {getTimeInIST(row.date, row.clock_in)}
                </TableCell>
                <TableCell align="center">
                  {getTimeInIST(row.date, row.clock_out)}
                </TableCell>
                <TableCell align="center">{row.comment}</TableCell>
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell align="center">Loading...</TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
