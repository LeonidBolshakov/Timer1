from time import sleep


def calc(func):
    it_happened_before = dict()

    def wrapper(*args):
        if it_happened_before.get(args) is None:
            res = func(*args)
            it_happened_before[args] = res
        else:
            res = it_happened_before[args]
        return res
    return wrapper


@calc
def ppp(param_i, param_j):
    print('***')
    sleep(1)
    return param_i + param_j


for i in range(2):
    for j in range(3):
        print(ppp(i, j))
for i in range(2):
    for j in range(3):
        print(ppp(i, j))
