import asyncio
import time
import tomllib
from datetime import datetime

from nicegui import events, ui
from pyasic import settings
from pyasic.device.algorithm.hashrate.unit.base import GenericUnit
from pyasic.network import MinerNetwork
from pydantic import ValidationError

from pyasic_dash.data import MinerFullTableData, MinerTableData
from pyasic_dash.settings import config

settings.update("network_ping_retries", 2)
settings.update("get_data_retries", 2)

updating = False
miners_g = []
refresh_rate_g = 5

dark = ui.dark_mode()
dark.enable()
ui.page_title("PyASIC Dash")

interval = 3.0


def update_interval(e):
    global interval
    interval = float(e.value)
    timer.interval = interval * 60


def handle_theme_change(e: events.ValueChangeEventArguments):
    grid.classes(
        add="ag-theme-balham-dark" if e.value else "ag-theme-balham",
        remove="ag-theme-balham ag-theme-balham-dark",
    )


async def scan_miners():
    global miners_g
    miners_g = []
    for r in config.range:
        network = MinerNetwork.from_subnet(r["iprange"])
        miners = await network.scan()
        print(f"Found {len(miners)} miners")
        for each in miners:
            miners_g.append((r["nickname"], each))
        time.sleep(1)


async def update():
    global updating
    global refresh_rate_g
    if updating == True:
        ui.notify("Already Updating", type="negative", position="top")
        return
    try:
        ui.notify("Updating Data", type="warning", position="top")
        updating = True
        data = await find_miners()
        lastupdate.set_text(f"Last Update: {datetime.now():%X}")
        ui.notify("Updating Data Complete!", type="positive", position="top")
        updating = False
    except Exception as error:
        print("An exception occurred:", error)
        ui.notify("Failed Update, check logs!", type="negative", position="top")
        updating = False
        grid.options["rowData"] = []
        grid.update()
        raise error


async def find_miners():
    global t_hashrate_txt
    miner_data = []
    await scan_miners()
    for location, each in miners_g:
        async with asyncio.timeout(5):
            data = await each.get_data()
        try:
            miner_data.append(
                MinerTableData.from_miner_data(m_data=data, location=location)
            )
        except ValidationError as e:
            print(f"Failed to init miner data for {each.ip}: {e}")
    data_sorted = sorted(miner_data, key=lambda d: d.hostname or "", reverse=True)
    table_data = MinerFullTableData(data=data_sorted)
    thashrate.set_text(
        f"Total Hashrate: {round(table_data.total_hashrate.into(GenericUnit.TH),2)} TH/s"
    )
    grid.options["rowData"] = table_data.model_dump(by_alias=True)["data"]
    grid.update()
    return data_sorted


grid = ui.aggrid(
    {
        "defaultColDef": {"flex": 1},
        "columnDefs": [
            {
                "headerName": "Hostname",
                "field": "hostname",
                "filter": "agTextColumnFilter",
                "floatingFilter": True,
            },
            {
                "headerName": "IP",
                "field": "ip",
                "filter": "agTextColumnFilter",
                "floatingFilter": True,
            },
            {
                "headerName": "Location",
                "field": "location",
                "filter": "agTextColumnFilter",
                "floatingFilter": True,
            },
            {
                "headerName": "Model",
                "field": "model",
                "filter": "agTextColumnFilter",
                "floatingFilter": True,
            },
            {
                "headerName": "FW",
                "field": "fw",
                "filter": "agTextColumnFilter",
                "floatingFilter": True,
            },
            {"headerName": "Temp", "field": "temp"},
            {"headerName": "Hashrate", "field": "hashrate"},
            {
                "headerName": "Performance",
                "field": "perf",
                "cellClassRules": {
                    "bg-red-700": "x < 90 & x != None",
                    "bg-orange-600": "x >= 90 & x < 98",
                    "bg-green-700": "x >= 98",
                },
            },
            {"headerName": "HBs", "field": "hbs", "cellClassRules": {}},
            {"headerName": "HB0", "field": "hb0", "cellClassRules": {}},
            {"headerName": "HB1", "field": "hb1", "cellClassRules": {}},
            {"headerName": "HB2", "field": "hb2", "cellClassRules": {}},
            {"headerName": "Voltage", "field": "voltage"},
            {"headerName": "API Power", "field": "rpower"},
            {"headerName": "Efficiency", "field": "eff"},
            {
                "headerName": "Worker",
                "field": "worker",
                "filter": "agTextColumnFilter",
                "floatingFilter": True,
            },
            {"headerName": "Status", "field": "status", "hide": True},
        ],
        "rowData": [],
        "rowSelection": "multiple",
        ":pagination": True,
    },
    html_columns=[1],
    theme="balham-dark",
).style("height: 800px")
timer = ui.timer(interval * 60, update)
with ui.row().style("align-items: center;"):
    lastupdate = ui.label().classes("text-xl")
    thashrate = ui.label().classes("text-xl")
    ui.button("Update", on_click=update)
    ui.button("Stop Auto Refresh", on_click=timer.cancel)
    ui.number(label="Interval (mins)", value=interval, on_change=update_interval)


async def delete_range():
    new_range = []
    for each2 in rangestable.selected:
        for each in config.range:
            if each2 == each:
                print("Found it")
            else:
                new_range.append(each)

    config.range = new_range
    rangestable.rows = config.range
    rangestable.update()


async def reset_range():
    with open("servers.toml", "rb") as f:
        tomldata = tomllib.load(f)
    config.range = tomldata["range"]
    rangestable.rows = config.range
    rangestable.update()


with ui.row().style("align-items: center;"):
    rangestable = ui.table(rows=config.range, selection="single", row_key="nickname")
    with ui.column().style("align-items: center;"):
        ui.button("Delete Range", on_click=delete_range)
        ui.button("Reset Ranges from File", on_click=reset_range)


ui.run()
