def primefac(n):
    ret = []
    divisor = 2
    while divisor * divisor <= n:
        while (n % divisor) == 0:
            ret.append(divisor)
            n = n // divisor
        divisor = divisor + 1
    if n > 1:
        ret.append(n)
    return ret
