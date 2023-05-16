const { exec } = require("child_process");

exec("alembic upgrade head", (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error}`);
    return;
  }
  console.log(stdout);
  console.error(stderr);
});