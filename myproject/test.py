#!/usr/bin/python3

import logging
import sys

from juju import loop
from juju.model import Model


async def deploy():
    # Create a Model instance. We need to connect our Model to a Juju api
    # server before we can use it.
    model = Model()

    # Connect to the currently active Juju model
    await model.connect_current()

    try:
        # Deploy a single unit of the ubuntu charm, using the latest revision
        # from the stable channel of the Charm Store.
        ubuntu_app = await model.deploy(
          'ubuntu',
          application_name='ubuntu',
          series='xenial',
          channel='stable',
        )

        if '--wait' in sys.argv:
            # optionally block until the application is ready
            await model.block_until(lambda: ubuntu_app.status == 'active')
    finally:
        # Disconnect from the api server and cleanup.
        await model.disconnect()


def main():
    logging.basicConfig(level=logging.INFO)

    # If you want to see everything sent over the wire, set this to DEBUG.
    ws_logger = logging.getLogger('websockets.protocol')
    ws_logger.setLevel(logging.INFO)

    # Run the deploy coroutine in an asyncio event loop, using a helper
    # that abstracts loop creation and teardown.
    loop.run(deploy())


if __name__ == '__main__':
    main()
