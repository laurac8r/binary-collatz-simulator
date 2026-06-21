def cells(value: int, width: int) -> str:
    bin = f'{value:b}'

    return bin.replace('1', '█').replace('0', '·')

def sparkline(values: list[int], *, log: bool = True) -> str:
    pass