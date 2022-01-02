import React from "react";
import { Typography, Box } from "@mui/material";
import { PieChart } from "react-minimal-pie-chart";
import { makeStyles } from "@mui/styles";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const useStyle = makeStyles({
  textPie: {
    textAlign: "center",
    paddingTop: "5%",
    position: "absolute",
    left: "32%",
    top: "33%",
  },
});

export const ChartComponent = (time) => {
  const totalTime = Object.entries(time.data);
  const arr1d = [].concat(...totalTime);
  let d = [];
  for (let i = 0; i < arr1d.length; i++) {
    d.push(arr1d[++i]);
  }
  console.log(d);
  const labels = ["Monday", "Tuesday", " Wednesday", "Thursday", "Friday"];
  const data = {
    labels,
    datasets: [
      {
        data: d,
        backgroundColor: d.map((value) => {
          let temp = Math.round(value);
          if (temp > 7) {
            return "#3bff6c";
          } else {
            return temp > 6 ? "#ebe300" : "#fc2d2d";
          }
        }),
      },
    ],
  };
  const classes = useStyle();
  return (
    <>
      <Box>
        <Box
          style={{
            height: "323px",
            width: "100%",
            position: "relative",
          }}
        >
          <Typography variant="h5" component="h4" className={classes.textPie}>
            Attendence status
          </Typography>
          <PieChart
            data={[
              { title: "Persent", value: 20, color: "#3bff6c" },
              { title: "Absent", value: 5, color: "#fc2d2d" },
              { title: "Half Leave", value: 1, color: "#ebe300" },
            ]}
            lineWidth={10}
            startAngle={-90}
            paddingAngle={1}
            radius={43}
          />
        </Box>
        <Box style={{ padding: "10px" }}>
          <Bar
            options={{
              responsive: true,
              plugins: {
                legend: {
                  position: "top",
                  display: false,
                },
                title: {
                  display: true,
                  text: "Last Week Report",
                },
              },
              animations: {
                tension: {
                  duration: 10000,
                  easing: "easeOutQuad",
                  from: 1,
                  to: 0,
                  loop: true,
                },
              },
            }}
            data={data}
          />
        </Box>
      </Box>
    </>
  );
};
