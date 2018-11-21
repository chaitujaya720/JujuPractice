#!/usr/bin/python3.5

import asyncio
import logging
import json
from juju import loop
from juju.model import Model
from flask import Flask
from flask.ext.cors import CORS

app = Flask(__name__)
cors = CORS(app)

controller_endpoint = '18.206.149.35:17070'
model_uuid = 'b9b7b55e-37e6-43e3-8d74-f9da485ac695'
username = 'shyam'
password = 'shyam'
cacert = None

async def deploy():
    # Create a Model instance. We need to connect our Model to a Juju api
    # server before we can use it.
    model = Model()

    # Connect to the currently active Juju model
	#await model.connect(controller_endpoint, model_uuid, username, password, cacert,)
    await model.connect(controller_endpoint, model_uuid, username, password, cacert)

    # Deploy a single unit of the ubuntu charm, using revision 0 from the
    # stable channel of the Charm Store.

    ubuntu_app = await model.deploy(
        'ubuntu-0',
        application_name='ubuntu',
        series='xenial',
        channel='stable',
    )

    # Disconnect from the api server and cleanup.
    model.disconnect()

@app.route('/')
def home():
    return "<b>Hello, World</b><br/>You can provision your machines with a single click...<br/>Click here <a href='/provision' target='new'>Provision</a>"

@app.route('/provision')
def provision():
    # Set logging level to debug so we can see verbose output from the
    # juju library.
    logging.basicConfig(level=logging.DEBUG)

    # Quiet logging from the websocket library. If you want to see
    # everything sent over the wire, set this to DEBUG.
    ws_logger = logging.getLogger('websockets.protocol')
    ws_logger.setLevel(logging.INFO)

    # Run the deploy coroutine in an asyncio event loop, using a helper
    # that abstracts loop creation and teardown.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(deploy())
    except:
        return json.dumps("Already Installed")

    return json.dumps("Deployed")

if __name__ == "__main__":
    app.run()
