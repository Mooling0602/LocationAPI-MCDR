from mcdreforged.api.all import PluginServerInterface

import location_api.runtime as rt
from location_api.mcdr.commands import build_command_tree


async def on_load(server: PluginServerInterface, _prev_module):
    rt.psi = server
    server.register_command(build_command_tree())
    server.logger.info("Loaded LocationAPI.")


def on_unload(server: PluginServerInterface):
    server.logger.info("Unloaded LocationAPI.")
