def hardswish(a):
    return a * (a + 3).clamp(0.0, 6.0) / 6
