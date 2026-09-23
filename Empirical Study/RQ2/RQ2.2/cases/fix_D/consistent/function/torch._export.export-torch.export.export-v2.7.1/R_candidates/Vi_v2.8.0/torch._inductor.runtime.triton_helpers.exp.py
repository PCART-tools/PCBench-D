@triton.jit
def exp(x, use_fast_math: tl.constexpr):
    if use_fast_math:
        return libdevice.exp2(x * _LOG_2_E)
    else:
        return math.exp(x)
