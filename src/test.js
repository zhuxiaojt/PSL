import { Application } from 'nexfep';
import fs from 'fs';
import path from 'path';
const app = new Application();
const win = await app.windows.createWindow();
win.loadHTML(fs.readFileSync(path.join(import.meta.dirname, 'front_dist', 'index.html'), 'utf-8'));
win.openDevTools();
