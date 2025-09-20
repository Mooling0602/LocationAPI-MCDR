from mcdreforged.api.all import PluginServerInterface


def on_load(server: PluginServerInterface, _prev_module):
    server.logger.info("Loaded LocationAPI.")


def on_unload(server: PluginServerInterface):
    server.logger.info("Unloaded LocationAPI.")
