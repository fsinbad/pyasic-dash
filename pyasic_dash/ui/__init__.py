from nicegui import ui
from pyasic import settings

from pyasic_dash.ui.table import MinerTableSection

settings.update("network_ping_retries", 1)
settings.update("network_ping_timeout", 3)
settings.update("network_scan_threads", 1000)
settings.update("network_scan_semaphore", 1000)
settings.update("factory_get_retries", 1)
settings.update("factory_get_timeout", 3)
settings.update("get_data_retries", 1)
settings.update("api_function_timeout", 5)

# ADVANCED SETTINGS
settings.update("socket_linger_time", 1000)


def run():
    dark = ui.dark_mode()
    dark.enable()
    ui.page_title("PyASIC Dash")

    MinerTableSection()

    ui.run()
