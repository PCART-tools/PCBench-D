    def timer() -> float:
        if privateuse1_device_handler:
            privateuse1_device_handler.synchronize()
        return timeit.default_timer()
