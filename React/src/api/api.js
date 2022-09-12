// import Redmine from "node-redmine";
// // const Redmine = {};

const token =
  "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6ImJvdCIsIngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYm90Il19fQ.Fo4nwUcy_DATDbFxPjbdAUG1oeAdzy1xuMjy8vSwDaZ0BLXq6tqhiQHNTYAS5nTXtFOEzJ0DzTi9n6tchhDIn7ryFSXPgr0iF4AzLsWDN0nxJf5WLV1EzStaUA_cldUVnG0cpU9D-DpUcLgTGPSmbKHYqtHdRdALjgh-ErGn7po";

const operationsDoc = `
      query MyQuery {
        attendance {
            id
            date
            clock_in
            clock_out
            comment
        }
      }
    `;

let myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
myHeaders.append(
  "Authorization",
  "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6ImJvdCIsIngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYm90Il19fQ.Fo4nwUcy_DATDbFxPjbdAUG1oeAdzy1xuMjy8vSwDaZ0BLXq6tqhiQHNTYAS5nTXtFOEzJ0DzTi9n6tchhDIn7ryFSXPgr0iF4AzLsWDN0nxJf5WLV1EzStaUA_cldUVnG0cpU9D-DpUcLgTGPSmbKHYqtHdRdALjgh-ErGn7po"
);

async function fetchGraphQL(operationsDoc, operationName, variables) {
  const result = await fetch("https://on-piglet-23.hasura.app/v1/graphql", {
    method: "POST",
    headers: myHeaders,
    body: JSON.stringify({
      query: operationsDoc,
      variables: variables,
      operationName: operationName,
    }),
  });
  return await result.json();
}

function fetchMyQuery() {
  return fetchGraphQL(operationsDoc, "MyQuery", {});
}

export async function startFetchMyQuery() {
  const { errors, data } = await fetchMyQuery();
  if (errors) {
    // handle those errors like a pro
    console.error(errors);
  }
  // do something great with this precious data
  console.log(data);
  return data;
}

// GET AUTH FROM REDMINE AND ACCESS DATA
// let hostname = "http://kore.koders.in/";
// let config = {
//   apiKey: "3c52cd5306d53eb54612ac4afc9dc63dc8f0b425",
// };

// const redmine = new Redmine(hostname, config);

// let dump_issue = function (issue) {
//   console.log("Dumping issue:");
//   for (let item in issue) {
//     console.log("  " + item + ": " + JSON.stringify(issue[item]));
//   }
// };

export const constFetchRedime = () => {
  // redmine.issues({ limit: 2 }, function (err, data) {
  //   if (err) console.log(err);
  //   for (let i in data.issues) {
  //     dump_issue(data.issues[i]);
  //   }
  //   console.log("total_count: " + data.total_count);
  // });
};
