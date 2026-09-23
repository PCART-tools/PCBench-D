    def get_ticks_position(self):
        """
        Return the ticks position ("left", "right", "default", or "unknown").
        """
        return {1: "left", 2: "right",
                "default": "default", "unknown": "unknown"}[
                    self._get_ticks_position()]
