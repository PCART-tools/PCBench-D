    @abc.abstractmethod
    def _str_pad(
        self,
        width,
        side: Literal["left", "right", "both"] = "left",
        fillchar: str = " ",
    ):
        pass
