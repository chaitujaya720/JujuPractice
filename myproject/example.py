#!/usr/bin/python3.5

import asyncio
import logging
import json
from juju import loop
from juju.model import Model
from juju.controller import Controller
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

controller_name = 'lxd-xenial'
controller_endpoint = '10.116.242.196:17070'
username = 'admin'
password = 'dee98365629755f0f939664ea973d0fb'
cacert = None


async def add_model(value):
    controller = Controller()
    # connect to current controller with current user, per Juju CLI
    await controller.connect(controller_endpoint, username, password, cacert)

    model = await controller.add_model(
        value,
    )
    ubuntu_app = await model.deploy(
        'ubuntu-0',
        application_name='ubuntu',
        series='trusty',
        channel='stable',
    )
    logstash_app = await model.deploy(
        'logstash',
        application_name='logstash',
        series='trusty',
        channel='stable',
    )
    openjdk_app = await model.deploy(
        'openjdk',
        application_name='openjdk',
        series='trusty',
        channel='stable',
        num_units=0,
    )

    await model.disconnect()
    await controller.disconnect()


async def destroy():
    model = Model()
    controller = Controller()
    await controller.connect(controller_endpoint, username, password, cacert)
    await model.connect_current()
    import ipdb; ipdb.set_trace()
    await controller.destroy_model(model.info.uuid)
    model.disconnect()
    controller.disconnect()


@app.route('/')
def home():
    return "<b>Hello, World</b><br/>You can provision your machines with a single click...<br/>Click here <a href='/provision' target='new'>Provision</a>"


@app.route('/add_deploymodel/<value>')
def add_deploy_model(value):
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
    #try:
    loop.run_until_complete(add_model(value))
    #except:
    #    return json.dumps("Already Installed")

    return json.dumps("Model Added and Deployed")


@app.route('/destroy')
def destroy_model():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(destroy())
    return json.dumps("Destroyed")


if __name__ == "__main__":
    app.run()

