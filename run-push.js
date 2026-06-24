const { spawn } = require("child_process");
const path = require("path");

const cwd = path.resolve(__dirname);

const proc = spawn("cmd", ["/c", "push.bat"], {
  cwd: cwd,
  stdio: "inherit",
  shell: true,
});

proc.on("close", (code) => {
  console.log("Exit code:", code);
});
