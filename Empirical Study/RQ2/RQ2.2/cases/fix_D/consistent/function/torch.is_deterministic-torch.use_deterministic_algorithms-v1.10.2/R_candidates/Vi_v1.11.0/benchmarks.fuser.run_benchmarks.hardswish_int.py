def hardswish_int(a):
    return a * (a + 3).clamp(0, 6) / 6
