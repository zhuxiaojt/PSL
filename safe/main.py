import threading
import scannerServer
import configManager
import filewatchServer
import pystray
from PIL import Image
import os
import logger

def stop_tray():
    tray.stop()

icon = Image.open(os.path.join(os.path.dirname(__file__), 'assets', 'logo.ico'))
menu = pystray.Menu(
    pystray.MenuItem('退出', stop_tray),
)

scannerServerThread = threading.Thread(target=scannerServer.server, daemon=True)
scannerServerThread.start()
configServerThread = threading.Thread(target=configManager.server, daemon=True)
configServerThread.start()
loggerServerThread = threading.Thread(target=logger.server, daemon=True)
loggerServerThread.start()
filewatchServerThread = threading.Thread(target=filewatchServer.server, daemon=True)
filewatchServerThread.start()

logger.log('[MAIN] PSL准备就绪')

tray = pystray.Icon(
    name='power_security_layer_tray_icon',
    title='Power Security Layer (PSL)', 
    icon=icon, 
    menu=menu
)
tray.run()
