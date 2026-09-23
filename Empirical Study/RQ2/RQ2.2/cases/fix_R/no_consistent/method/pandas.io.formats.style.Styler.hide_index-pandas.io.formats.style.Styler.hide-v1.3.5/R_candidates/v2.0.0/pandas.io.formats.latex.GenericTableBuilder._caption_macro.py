    @property
    def _caption_macro(self) -> str:
        r"""Caption macro, extracted from self.caption.

        With short caption:
            \caption[short_caption]{caption_string}.

        Without short caption:
            \caption{caption_string}.
        """
        if self.caption:
            return "".join(
                [
                    r"\caption",
                    f"[{self.short_caption}]" if self.short_caption else "",
                    f"{{{self.caption}}}",
                ]
            )
        return ""
