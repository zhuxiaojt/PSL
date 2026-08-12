import child_process from 'child_process';

try{
    child_process.execSync("vite build && node -e \"require('fs').rmSync('node_modules', { recursive: true, force: true })\"&& node -e \"require('fs').rmSync('dist', { recursive: true, force: true })\" && pnpm install --production && npx --yes nexfpack@0.5.0 nexfpack.config.json", { stdio: 'inherit' });
} catch (error) {
    console.error(error);
} finally {
    child_process.execSync('pnpm install');
}
