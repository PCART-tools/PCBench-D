    def _get_mkldnn_device_op(device_type: str) -> MkldnnDeviceOpBase:
        """
        Returns the MKLDNN device operation class based on the current device type.
        """
        if device_type == "cpu":
            return CpuMkldnnDeviceOp()
        elif device_type == "xpu":
            return XpuMkldnnDeviceOp()
        else:
            raise RuntimeError(f"MKLDNN is not supported on {device_type} device.")
