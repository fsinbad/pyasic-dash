from nicegui import ui
from pyasic import settings

from pyasic_dash.ui.table import MinerTableSection

settings.update("network_ping_retries", 1)
settings.update("network_ping_timeout", 3)
settings.update("network_scan_threads", 100)
settings.update("network_scan_semaphore", None)
settings.update("factory_get_retries", 1)
settings.update("factory_get_timeout", 3)
settings.update("get_data_retries", 1)
settings.update("api_function_timeout", 5)
settings.update("antminer_mining_mode_as_str", False)
settings.update("default_whatsminer_rpc_password", "admin")
settings.update("default_innosilicon_web_password", "admin")
settings.update("default_antminer_web_password", "root")
settings.update("default_bosminer_web_password", "root")
settings.update("default_vnish_web_password", "admin")
settings.update("default_goldshell_web_password", "123456789")
settings.update("default_auradine_web_password", "admin")
settings.update("default_epic_web_password", "letmein")
settings.update("default_hive_web_password", "admin")
settings.update("default_antminer_ssh_password", "miner")
settings.update("default_bosminer_ssh_password", "root")

# ADVANCED SETTINGS
settings.update("socket_linger_time", 1000)


def run():
    dark = ui.dark_mode()
    dark.enable()
    ui.page_title("PyASIC Dash")

    MinerTableSection()

    ui.run()
