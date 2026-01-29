from mcdreforged.api.all import PluginServerInterface, Literal, Text
from location_api.pos import on_debug_pos_help, on_debug_pos


async def on_load(server: PluginServerInterface, _prev_module):
    server.register_command(
        Literal("!!loc_api").then(
            Literal("debug").runs(
                on_debug_pos_help
            ).then(
                Literal("pos").then(
                    Text("player").runs(
                        on_debug_pos
                    ).requires(lambda src: src.has_permission_higher_than(2))
                )
            )
        )
    )
    server.logger.info("Loaded LocationAPI.")


def on_unload(server: PluginServerInterface):
    server.logger.info("Unloaded LocationAPI.")
