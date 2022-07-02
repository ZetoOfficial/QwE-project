def average(lst: list, base: int = 1) -> int:
    return round((sum(lst) / len(lst)) / base) * base


def median(lst: list) -> int:
    n = len(lst)
    index = n // 2
    if n % 2:
        return sorted(lst)[index]
    return sorted(lst)[index - 1 : index + 1][0]
