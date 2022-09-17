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
    top: "42%",
    left: "26%",
    position: "absolute",
    textAlign: "center",
    paddingTop: "0%",
  },
});

let weekdays = new Array(7);
weekdays[0] = "Sunday";
weekdays[1] = "Monday";
weekdays[2] = "Tuesday";
weekdays[3] = "Wednesday";
weekdays[4] = "Thursday";
weekdays[5] = "Friday";
weekdays[6] = "Saturday";

const appendZero = (value) => {
  if (value.length < 2) {
    return `0${value}`;
  } else return value;
};

export const ChartComponent = ({ lastWeek, allAtten }) => {
  let chartData = [];
  lastWeek.forEach((item, i) => {
    let obj = new Date(new Date().setDate(new Date().getDate() - i));
    let dateString = obj.toLocaleDateString();
    dateString = dateString?.split("/");
    dateString =
      dateString[2] +
      "-" +
      appendZero(dateString[0]) +
      "-" +
      appendZero(dateString[1]);
    let obj2 = new Date(dateString);
    let flag = true;
    if (weekdays[obj2.getDay()] !== "Sunday") {
      for (let i = 0; i < lastWeek.length; i++) {
        if (dateString === lastWeek[i].date) {
          flag = false;

          chartData.push({
            day: weekdays[obj2.getDay()],
            date: dateString,
            time: lastWeek[i].clock_in
              ? getSpentTime(
                  lastWeek[i].clock_in ? lastWeek[i].clock_in : "",
                  lastWeek[i].clock_out ? lastWeek[i].clock_out : ""
                )
              : 0,
          });
          break;
        }
      }
      if (flag) {
        chartData.push({
          day: weekdays[obj2.getDay()],
          date: dateString,
          time: 0,
        });
      }
    }
  });
  chartData.reverse();
  const data = {
    labels: chartData.map((item) => item.day),
    datasets: [
      {
        data: chartData.map((item) => item.time),
        backgroundColor: chartData.map((value) => {
          let temp = Math.round(value.time);
          if (temp >= 7) {
            return "#3bff6c";
          } else {
            return temp > 4.5 ? "#ebe300" : "#fc2d2d";
          }
        }),
      },
    ],
  };
  const classes = useStyle();

  let totalDays = allAtten.length;
  let half = 0;
  let full = 0;
  // **********pythart**********
  allAtten.forEach((item) => {
    if (item.clock_in && item.clock_out) {
      full = full + 1;
    } else if (item.clock_in) {
      half = half + 1;
    }
  });

  return (
    <>
      <Box style={{ height: "100%" }}>
        <Box
          style={{
            height: "50%",
            width: "100%",
            position: "relative",
          }}
        >
          <Typography variant="h5" component="h4" className={classes.textPie}>
            Attendence status
          </Typography>
          <PieChart
            data={[
              { title: "Persent", value: totalDays, color: "#3bff6c" },
              { title: "Absent", value: full, color: "#fc2d2d" },
              { title: "Half Leave", value: half, color: "#ebe300" },
            ]}
            lineWidth={10}
            startAngle={-90}
            paddingAngle={1}
            radius={43}
          />
        </Box>
        <Box style={{ padding: "10px", height: "50%" }}>
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
                  text: "Last Seven Day's Statistics",
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

const getSpentTime = (clockIn = "04:30:00", clockOut = "12:30:00") => {
  let outT;
  if (!clockOut) outT = "12:30:00";
  const SECONDS_PER_DAY = 86400;
  const HOURS_PER_DAY = 24;
  const tempArrIn = clockIn.split(":");
  const secIn =
    tempArrIn[0] * 60 * 60 + tempArrIn[1] * 60 + parseInt(tempArrIn[2]);
  const tempArrOut = outT.split(":");
  const secOut =
    tempArrOut[0] * 60 * 60 + tempArrOut[1] * 60 + parseInt(tempArrOut[2]);
  const spentSeconds = secOut - secIn;
  const days = Math.floor(spentSeconds / SECONDS_PER_DAY);
  const remainderSeconds = spentSeconds % SECONDS_PER_DAY;
  const hms = new Date(remainderSeconds * 1000).toISOString().substring(11, 19);
  const time = hms.replace(/^(\d+)/, (h) =>
    `${Number(h) + days * HOURS_PER_DAY}`.padStart(2, "0")
  );
  return parseInt(time.split(":")[0]) + parseInt(time.split(":")[1]) / 100;
};
