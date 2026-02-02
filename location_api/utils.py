from returns.result import Result
from returns.converters import maybe_to_result
from returns.maybe import Maybe


def promote_to_result(res: Result[Maybe[str], Exception]) -> Result[str, Exception]:
    return res.alt(
        lambda e: Exception(f"Failed to get data from Rcon: {e}")
    ).bind(
        lambda maybe: maybe_to_result(maybe).alt(
            lambda _: Exception("No data received!")
        )
    )
