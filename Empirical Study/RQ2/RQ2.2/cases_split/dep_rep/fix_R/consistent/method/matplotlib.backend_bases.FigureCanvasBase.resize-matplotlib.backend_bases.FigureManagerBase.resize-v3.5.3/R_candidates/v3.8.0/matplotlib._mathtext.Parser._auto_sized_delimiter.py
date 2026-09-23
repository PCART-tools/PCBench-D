    def _auto_sized_delimiter(self, front: str,
                              middle: list[Box | Char | str],
                              back: str) -> T.Any:
        state = self.get_state()
        if len(middle):
            height = max([x.height for x in middle if not isinstance(x, str)])
            depth = max([x.depth for x in middle if not isinstance(x, str)])
            factor = None
            for idx, el in enumerate(middle):
                if isinstance(el, str) and el == '\\middle':
                    c = T.cast(str, middle[idx + 1])  # Should be one of p.delims.
                    if c != '.':
                        middle[idx + 1] = AutoHeightChar(
                                c, height, depth, state, factor=factor)
                    else:
                        middle.remove(c)
                    del middle[idx]
            # There should only be \middle and its delimiter as str, which have
            # just been removed.
            middle_part = T.cast(list[T.Union[Box, Char]], middle)
        else:
            height = 0
            depth = 0
            factor = 1.0
            middle_part = []

        parts: list[Node] = []
        # \left. and \right. aren't supposed to produce any symbols
        if front != '.':
            parts.append(
                AutoHeightChar(front, height, depth, state, factor=factor))
        parts.extend(middle_part)
        if back != '.':
            parts.append(
                AutoHeightChar(back, height, depth, state, factor=factor))
        hlist = Hlist(parts)
        return hlist
