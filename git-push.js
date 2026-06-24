const {execSync} = require('child_process');
const cwd = 'd:/Produktif/Magang/PT. Gama Integra Informatika/framework trend';

try {
  execSync('git add -A', {cwd});
  console.log('Files staged.');

  const msg = 'feat: Framework Trends Tracker - 18 frameworks with SO 2025 integration, orbit hero dashboard, and Makefile';
  execSync('git commit -m "' + msg + '"', {cwd});
  console.log('Committed.');

  execSync('git push -u origin main', {cwd});
  console.log('Pushed to GitHub!');
} catch(e) {
  console.error(e.message);
}
