from mcdreforged.api.all import PluginServerInterface


def on_load(server: PluginServerInterface, _prev_module):
    server.logger.info("Loaded LocationAPI.")


def on_server_startup(server: PluginServerInterface):
    pass
