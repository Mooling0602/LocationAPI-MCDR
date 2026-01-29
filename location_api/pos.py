"""This module aims to provide apis to locate the position of any actual player.

To use APIs here, you must have `mcdreforged` package installed.
"""
from returns.result import Success, Failure
from returns.maybe import Some
from mcdreforged.api.all import PluginServerInterface
from moolings_rcon_api.api import rcon_get_async

_PSI: PluginServerInterface | None = None


async def get_player_pos(player: str, psi: PluginServerInterface | None = None):
    if psi:
        server = psi
    else:
        if _PSI:
            server = _PSI
        else:
            raise RuntimeError("PluginServerInterface is not initialized!")
    query_pos_cmd = f"data get entity {player} Pos"
    query_result = await rcon_get_async(query_pos_cmd)
    match query_result:
        case Success(Some(content)):
            server.logger.info(f"Get result: {content}")
        case Success(_):
            server.logger.error("Failed to get player position: empty response.")
        case Failure(e):
            server.logger.error(f"Failed to get player position: {e}")
