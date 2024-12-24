import logging

from pyasic_dash import ui

logging.basicConfig(level=logging.DEBUG)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
