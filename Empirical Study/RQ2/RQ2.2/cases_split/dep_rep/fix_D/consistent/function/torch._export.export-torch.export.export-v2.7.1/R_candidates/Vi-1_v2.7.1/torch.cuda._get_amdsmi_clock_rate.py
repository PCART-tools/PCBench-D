def _get_amdsmi_clock_rate(device: Optional[Union[Device, int]] = None) -> int:
    handle = _get_amdsmi_handler(device)
    clock_info = amdsmi.amdsmi_get_clock_info(handle, amdsmi.AmdSmiClkType.GFX)
    if "cur_clk" in clock_info:  # ROCm 6.2 deprecation
        return clock_info["cur_clk"]
    else:
        return clock_info["clk"]
