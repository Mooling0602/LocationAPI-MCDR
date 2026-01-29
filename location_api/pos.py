"""This module aims to provide apis to locate the position of any actual player.

To use APIs here, you must have `mcdreforged` package installed.
"""
from returns.result import Success, Failure
from returns.maybe import Some
from mcdreforged.api.all import CommandSource, CommandContext
from moolings_rcon_api.api import rcon_get_async

# _PSI: PluginServerInterface | None = None


def on_debug_pos_help(src: CommandSource):
    src.reply("Usage: !!loc_api debug pos <player>")


async def on_debug_pos(src: CommandSource, ctx: CommandContext):
    result = await get_player_pos(ctx['player'])
    src.reply(result)


async def get_player_pos(player: str):
    query_pos_cmd = f"data get entity {player} Pos"
    query_result = await rcon_get_async(query_pos_cmd)
    match query_result:
        case Success(Some(content)):
            return f"Get result: {content}"
        case Success(_):
            return "Failed to get player position: empty response."
        case Failure(e):
            return f"Failed to get player position: {e}"
