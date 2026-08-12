import { PipeClient } from './pipe.js';
import { Application, Icon, Size } from 'nexfep';
import path from 'path';
import fs from 'fs';
import { AsyncFileDialog } from "@bindrs/rfd"

async function run(loaderURL, onReady){
    return new Promise(async(resolve, reject) => {
        const app = new Application({
            localProxys: [
                {
                    protocolName: 'pslui',
                    localPath: path.join(import.meta.dirname, 'front_dist')
                }
            ]
        });
        try {
            app.createLocker('PSL_SAFE_UI_LOCKER');
        } catch {
            resolve();
        }
        const window = await app.windows.createWindow({
            decoration: false, 
            title: 'PSL', 
            size: new Size(865, 515),
            icon: Icon.from(path.join(import.meta.dirname, 'assets', 'logo.ico'))
        })
        window.loadURL(loaderURL)
        app.windows.handle('close', () => { 
            app.exit();
            resolve();
        })
        app.windows.handle('fast_scan', () => {
            const tryit = async() => {
                try{
                    const scanClient = new PipeClient('PSL_SAFE_SCANNER_SERVER');
                    await scanClient.connect((methods)=>{
                        methods.write('fast_scan');
                        methods.disconnect();
                    });
                } catch {
                    setTimeout(tryit, 20);
                }
            }
            tryit();
        })
        app.windows.handle('disk_scan', () => {
            const tryit = async() => {
                try{
                    const scanClient = new PipeClient('PSL_SAFE_SCANNER_SERVER');
                    await scanClient.connect((methods)=>{
                        methods.write('disk_scan');
                        methods.disconnect();
                    });
                } catch {
                    setTimeout(tryit, 20);
                }
            }
            tryit();
        })
        app.windows.handle('custom_folder_scan', async() => {
            const folder_path = (await new AsyncFileDialog().pickFolder())?.path();
            const tryit = async() => {
                try{
                    const scanClient = new PipeClient('PSL_SAFE_SCANNER_SERVER');
                    await scanClient.connect((methods)=>{
                        methods.write('custom_folder_scan_' + folder_path);
                        methods.disconnect();
                    });
                } catch {
                    setTimeout(tryit, 20);
                }
            }
            if(folder_path){
                tryit();
            }
        })
        app.windows.handle('query_scan_status', () => {
            return new Promise((resolve, reject) => {
                const tryit = async() => {
                    try{
                        const scanClient = new PipeClient('PSL_SAFE_SCANNER_SERVER');
                        await scanClient.connect(async(methods)=>{
                            methods.write('query_status');
                            const result = await methods.read();
                            console.log(result);
                            methods.disconnect();
                            resolve(result);
                        });
                    } catch {
                        setTimeout(tryit, 20);
                    }
                }
                tryit();
            });
        })
        app.windows.handle('close_scan', () => {
            const tryit = async() => {
                try{
                    const scanClient = new PipeClient('PSL_SAFE_SCANNER_SERVER');
                    await scanClient.connect((methods)=>{
                        methods.write('go_unstarted');
                        methods.disconnect();
                    });
                } catch {
                    setTimeout(tryit, 20);
                }
            }
            tryit();
        })
        app.windows.handle('get_config', () => {
            return new Promise((resolve, reject) => {
                const tryit = async() => {
                    try{
                        const configClient = new PipeClient('PSL_SAFE_CONFIG_SERVER');
                        await configClient.connect(async(methods)=>{
                            methods.write('get_config');
                            const result = await methods.read();
                            methods.disconnect();
                            resolve(result);
                        });
                    } catch {
                        setTimeout(tryit, 20);
                    }
                }
                tryit();
            });
        })
        app.windows.handle('save_config', async(config) => {
            app.logger.log(config)
            const tryit = async() => {
                try{
                    const configClient = new PipeClient('PSL_SAFE_CONFIG_SERVER');
                    await configClient.connect((methods)=>{
                        methods.write('save_config_' + config);
                        methods.disconnect();
                    });
                } catch {
                    setTimeout(tryit, 20);
                }
            }
            tryit();
        })
        app.windows.handle('choose_picture', async() => {
            const picture_path = (await new AsyncFileDialog().addFilter('Image Files', ['jpg', 'jpeg', 'png']).pickFile())?.path();
            if(picture_path){
                return picture_path;
            }
        })
        app.windows.handle('get_picture_base64', async(path) => {
            const file = await new Promise((resolve, reject) => {
                fs.readFile(path, (err, data) => {
                    if(err){
                        reject(err);
                    } else {
                        resolve(data);
                    }
                });
            });
            return Buffer.from(file).toString('base64');
        })
        app.windows.handle('quarantine_files', () => {
            const tryit = async() => {
                try{
                    const scanClient = new PipeClient('PSL_SAFE_SCANNER_SERVER');
                    await scanClient.connect((methods)=>{
                        methods.write('quarantine_files');
                        methods.disconnect();
                    });
                } catch {
                    setTimeout(tryit, 20);
                }
            }
            tryit();
        })
        app.windows.handle('delete_quarantined_file', (uuid) => {
            const tryit = async() => {
                try{
                    const scanClient = new PipeClient('PSL_SAFE_SCANNER_SERVER');
                    await scanClient.connect((methods)=>{
                        methods.write('delete_quarantined_file_' + uuid);
                        methods.disconnect();
                    });
                } catch {
                    setTimeout(tryit, 20);
                }
            }
            tryit();
        })
        app.windows.handle('restore_quarantined_file', (uuid) => {
            const tryit = async() => {
                try{
                    const scanClient = new PipeClient('PSL_SAFE_SCANNER_SERVER');
                    await scanClient.connect((methods)=>{
                        methods.write('restore_quarantined_file_' + uuid);
                        methods.disconnect();
                    });
                } catch {
                    setTimeout(tryit, 20);
                }
            }
            tryit();
        })
        app.windows.handle('get_quarantined_files', () => {
            return new Promise((resolve, reject) => {
                const tryit = async() => {
                    try{
                        const scanClient = new PipeClient('PSL_SAFE_SCANNER_SERVER');
                        await scanClient.connect(async(methods)=>{
                            methods.write('get_quarantined_files');
                            const result = await methods.read();
                            methods.disconnect();
                            resolve(result);
                        });
                    } catch {
                        setTimeout(tryit, 20);
                    }
                }
                tryit();
            });
        })
        app.windows.handle('get_logs', () => {
            return new Promise((resolve, reject) => {
                const tryit = async() => {
                    try{
                        const loggerClient = new PipeClient('PSL_SAFE_LOGGER_SERVER');
                        await loggerClient.connect(async(methods)=>{
                            methods.write('get_logs');
                            const result = await methods.read();
                            methods.disconnect();
                            resolve(result);
                        });
                    } catch {
                        setTimeout(tryit, 20);
                    }
                }
                tryit();
            });
        })
        app.windows.handle('clear_logs', () => {
            const tryit = async() => {
                try{
                    const loggerClient = new PipeClient('PSL_SAFE_LOGGER_SERVER');
                    await loggerClient.connect((methods)=>{
                        methods.write('clear_logs');
                        methods.disconnect();
                    });
                } catch {
                    setTimeout(tryit, 20);
                }
            }
            tryit();
        })
        app.windows.handle('clear_log_file', () => {
            const tryit = async() => {
                try{
                    const loggerClient = new PipeClient('PSL_SAFE_LOGGER_SERVER');
                    await loggerClient.connect((methods)=>{
                        methods.write('clear_log_file');
                        methods.disconnect();
                    });
                } catch {
                    setTimeout(tryit, 20);
                }
            }
            tryit();
        })
        onReady?.(window);
    })
}

export { run }