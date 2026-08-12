import net from 'net';

class PipeClient { 
    constructor(pipe_name) {
        this.pipe_name = `\\\\.\\pipe\\${pipe_name}`;
    }
    async connect(handler) {
        return new Promise((resolve, reject) => {
            let datas = []
            let ondata
            const throwErr = (err) => {
                reject(err);
            }
            const connection = net.createConnection({ path: this.pipe_name }, async() => {
                await handler({ read: async () => {
                        return new Promise((resolve, reject) => { 
                            const waitf = () => {
                                if(datas.length){
                                    ondata = undefined
                                    resolve(datas.shift().toString());
                                }else{
                                    ondata = waitf
                                }
                            }
                            waitf();
                        });
                    },  write: (data) => {
                        connection.write(data);
                    }, disconnect: () => {
                        connection.end()
                        resolve();
                    }
                });
            }).on('data',(data)=>{
                datas.push(data);
                if(ondata){
                    ondata();
                }
            }).on('error',(data)=>{
                throwErr(data);
            });
        })
    }
}
export { PipeClient }