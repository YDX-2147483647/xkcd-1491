def tuple_or_int(value: int | tuple[int, ...] | list[int]) -> int | tuple[int, ...]:
    if isinstance(value, list):
        return tuple(value)
    else:
        return value


def average(value: int | tuple[int, ...]) -> int | float:
    if isinstance(value, tuple):
        return sum(value) / len(value)
    else:
        return value


def diff(value: int | tuple[int, ...]) -> int:
    if isinstance(value, tuple):
        return max(value) - min(value)
    else:
        return 1
