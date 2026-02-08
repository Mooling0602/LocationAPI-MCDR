"""This module aims to provide apis to locate the position of any actual player.

To use APIs here, you must have set up `MCDReforged <https://docs.mcdreforged.com>`__ in your environment.
"""

import re

from mcdreforged.api.all import CommandContext, CommandSource
from moolings_rcon_api.api import rcon_get
from returns.result import Failure, Result, Success, safe

import location_api.runtime as rt
from location_api import MCPosition, Point3D
from location_api.utils import promote_to_result

# _PSI: PluginServerInterface | None = None


def on_debug_pos_help(src: CommandSource):
    src.reply("Usage: !!loc_api debug pos <player>")


async def on_debug_pos(src: CommandSource, ctx: CommandContext):
    result = await get_player_pos(ctx["player"])
    match result:
        case Success(pos):
            src.reply(f"Player {ctx['player']} is at {pos}")
        case Failure(err):
            src.reply(f"Error: {err}")


def get_point3d_from_server_reply(
    content: str, player_name: str | None = None, regex: str | None = None
) -> Point3D | None:
    """
    Extracts a :class:`~location_api.Point3D` instance from a text content, like this:

    ``CleMooling has the following entity data: [-524.5d, 71.0d, -66.5d]``

    :param content: The text content to extract the 3d point from.
    :param player_name: The name of the player. Defaults to :obj:`None`.
    :param regex: The regex pattern to match the 3d point. Defaults to :obj:`None`.

    :returns:
        * :obj:`None` -- If matches ``No entity was found`` or if player name is provided but not found in log content.
        * :class:`~location_api.Point3D` -- If matches format like example.

    :raises TypeError: If the 3d point cannot be extracted.
    """
    if "No entity was found" in content:
        return None

    if regex is None:
        # Captures three numbers with optional decimal part and optional 'd' suffix
        regex = r"\[(-?\d+(?:\.\d+)?)d?,\s*(-?\d+(?:\.\d+)?)d?,\s*(-?\d+(?:\.\d+)?)d?\]"

    pattern = re.compile(regex)
    match = pattern.search(content)

    if not match:
        raise TypeError(
            f"Could not extract 3D point from log content: {content}"
        )

    try:
        x = float(match.group(1))
        y = float(match.group(2))
        z = float(match.group(3))
    except ValueError as e:
        raise TypeError(
            f"Could not convert matched values to float: {match.groups()}"
        ) from e

    if player_name is not None and player_name not in content:
        return None

    return Point3D(x=x, y=y, z=z)


def get_dimension_from_server_reply(
    content: str, player: str | None = None, regex: str | None = None
) -> str | None:
    """Extracts a dimension string from a text content, like this:

    ``CleMooling has the following entity data: minecraft:overworld``

    :param content: The text content to extract the dimension from.
    :param player: The name of the player. Defaults to :obj:`None`.
    :param regex: The regex pattern to match the dimension. Defaults to :obj:`None`.

    :returns: The extracted dimension string or :obj:`None` if not found.
    """
    if player is not None and player not in content:
        return None

    if regex is None:
        regex = r"minecraft:(\w+)"

    match = re.search(regex, content)
    if match is None:
        return None

    return match.group(1)


@safe
def safe_parse_pos(pos_str: str, player: str) -> Point3D:
    """A wrapper to get a :class:`~location_api.Point3D` instance from a string(rcon command result as server reply).

    Actually calls :data:`get_point3d_from_server_reply`.

    :param pos_str: The string to parse.
    :param player: The name of the player.
    :return: The parsed :class:`~location_api.Point3D` result, but actually a :class:`~returns.result.Result` object.
    """
    result = get_point3d_from_server_reply(pos_str, player)
    if result is None:
        raise ValueError(f"No data received for {player}!")
    return result


@safe
def safe_parse_dim(dim_str: str, player: str) -> str:
    """A wrapper to get a dimension string from a string(rcon command result as server reply).

    Actually calls :data:`get_dimension_from_server_reply`.

    :param dim_str: The string to parse.
    :param player: The name of the player.
    :return: The parsed dimension string, but actually a :class:`~returns.result.Result` object.
    """
    result = get_dimension_from_server_reply(dim_str)
    if result is None:
        raise ValueError(f"No data received for {player}!")
    return result


async def get_player_pos(player: str) -> Result[MCPosition, Exception]:
    """Get the position of a player.

    :param player: The name of the player.

    :return: The position of the player or an exception.
    """
    raw_pos = await rcon_get(rt.psi, f"data get entity {player} Pos")
    raw_dim = await rcon_get(rt.psi, f"data get entity {player} Dimension")

    return Result.do(
        MCPosition(point=point, dimension=dimension)
        for pos_str in promote_to_result(raw_pos)
        for dim_str in promote_to_result(raw_dim)
        for point in safe_parse_pos(pos_str, player)
        for dimension in safe_parse_dim(dim_str, player)
    )
