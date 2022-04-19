from typing import Any


def is_int_or_float(number: Any) -> Any:
    if number % 1 == 0:
        return int(number)
    else:
        return float("{:.2f}".format(number))
