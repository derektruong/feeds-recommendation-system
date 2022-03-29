from asyncio import ThreadedChildWatcher
from server.factory import create_app

import os
import configparser


config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

if __name__ == "__main__":
    app = create_app()
    app.config['DEBUG'] = False
    app.config['MONGO_URI'] = config['TEST']['DB_URI']
    app.run(threaded=True, port=3000)