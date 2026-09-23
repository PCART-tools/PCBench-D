@torch.fx.wrap
def _wrapped_hardswish_fp16(x):
    x = x.dequantize()
    x = F.hardswish(x)
    x = x.to(torch.float16)
    return x
