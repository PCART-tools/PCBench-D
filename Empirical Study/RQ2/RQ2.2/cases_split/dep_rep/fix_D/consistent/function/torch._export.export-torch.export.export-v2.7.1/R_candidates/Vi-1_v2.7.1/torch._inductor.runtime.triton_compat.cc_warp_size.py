def cc_warp_size(cc: Union[str, int]) -> int:
    if torch.version.hip:
        cc_str = str(cc)
        if "gfx10" in cc_str or "gfx11" in cc_str:
            return 32
        else:
            return 64
    else:
        return 32
