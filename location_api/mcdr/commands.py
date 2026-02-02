from mcdreforged.api.all import Literal as CommandLiteral
from mcdreforged.api.all import Text

from location_api.pos import on_debug_pos, on_debug_pos_help


def build_command_tree() -> CommandLiteral:
    return CommandLiteral("!!loc_api").then(
        CommandLiteral("debug")
        .runs(on_debug_pos_help)
        .then(
            CommandLiteral("pos").then(
                Text("player")
                .runs(on_debug_pos)
                .requires(lambda src: src.has_permission_higher_than(2))
            )
        )
    )
