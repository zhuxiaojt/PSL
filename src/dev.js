import binpx from 'binpx';
import { run } from './main.js';
const vite = await binpx('vite', [], { allowFallback: false, raw: true });
await run('http://127.0.0.1:5173/', (window) => {
    window.openDevTools();
})
if(vite){
    vite.kill();
}
process.exit(0);