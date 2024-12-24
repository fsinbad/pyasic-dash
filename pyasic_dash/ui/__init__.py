from nicegui import ui
from pyasic import settings

from pyasic_dash.ui.table import MinerTableSection

settings.update("network_ping_retries", 2)
settings.update("get_data_retries", 2)


def run():
    dark = ui.dark_mode()
    dark.enable()
    ui.page_title("PyASIC Dash")

    MinerTableSection()

    ui.run()
