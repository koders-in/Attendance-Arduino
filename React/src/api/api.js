const operationsDoc = (offset = 0) => `
      query MyQuery {
        attendance(where: {user_id:{_eq:81}},limit: 10,offset: ${offset}) {
            id
            date
            clock_in
            clock_out
            comment
        }
      }
    `;

const fetchTotalData = `
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

function fetchMyQuery(offset) {
  return fetchGraphQL(operationsDoc(offset), "MyQuery", {});
}

function fetchMyQueryAll(offset) {
  return fetchGraphQL(fetchTotalData, "MyQuery", {});
}

export async function startFetchMyQuery(offset) {
  const { errors, data } = await fetchMyQuery(offset);
  if (errors) {
    console.error(errors);
  }
  return data;
}

async function startFetchAllQuery() {
  const { errors, data } = await fetchMyQueryAll();
  if (errors) {
    console.error(errors);
  }
  return data;
}

export async function getLastSeven() {
  const res = await startFetchAllQuery();
  const data = res?.attendance?.slice(
    res.attendance.length - 7,
    res.attendance.length - 1
  );
  return data;
}

export async function getAllData() {
  const res = await startFetchAllQuery();
  return res.attendance;
}
