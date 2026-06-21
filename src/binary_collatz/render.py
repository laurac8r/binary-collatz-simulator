def cells(value: int, width: int) -> str:
    bin = f'{value:b}'

    ret = bin.replace('1', '█').replace('0', '·')

    pad = ''.join([' ']*(width-len(ret)))

    return pad + ret

def sparkline(values: list[int], *, log: bool = True) -> str:
    return "▁▂▃▄▅▆▇█"