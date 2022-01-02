let Redmine = require("node-redmine");
// let Redmine = require("node-redmine");

// protocol required in Hostname, supports both HTTP and HTTPS
var hostname = "https://kore.koders.in";
var config = {
  username: "koders",
  password: "kodersonepass",
};

let redmine = new Redmine(hostname, config);
// ----------
redmine.current_user({ limit: 1 }, function (err, data) {
  if (err) throw err;
  console.log(data.user.firstname);
  console.log(data.user.lastname);
});

// redmine.issues({ limit: 1 }, function (err, data) {
//   if (err) throw err;
//   console.log(data.total_count);
//   console.log(data.user.lastname);
// });
