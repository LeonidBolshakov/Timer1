def plus(l: list) -> list | None:
    if not isinstance(l, list):
        return None
    s = ''.join(l)
    if not s.isdigit():
        return None
    if l[0] == '0' and len(s) != 1:
        return None
    s = str(int(s) + 1)
    return list(map(str, s))

assert plus(['3','4'])      == ['3', '5']
assert plus(['9','9','9'])  == ['1','0','0', '0']
assert plus(['0'])          == ['1']
assert plus(['0','0','7'])  == None
assert plus(['9','t'])      == None
assert plus(['-1','0','3']) == None
assert plus([])             == None
assert plus(4)              == None

