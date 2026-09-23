    def _genset(self, s: str, loc: int, toks: ParseResults) -> T.Any:
        annotation = toks["annotation"]
        body = toks["body"]
        thickness = self.get_state().get_current_underline_thickness()

        annotation.shrink()
        centered_annotation = HCentered([annotation])
        centered_body = HCentered([body])
        width = max(centered_annotation.width, centered_body.width)
        centered_annotation.hpack(width, 'exactly')
        centered_body.hpack(width, 'exactly')

        vgap = thickness * 3
        if s[loc + 1] == "u":  # \underset
            vlist = Vlist([
                centered_body,               # body
                Vbox(0, vgap),               # space
                centered_annotation          # annotation
            ])
            # Shift so the body sits in the same vertical position
            vlist.shift_amount = centered_body.depth + centered_annotation.height + vgap
        else:  # \overset
            vlist = Vlist([
                centered_annotation,         # annotation
                Vbox(0, vgap),               # space
                centered_body                # body
            ])

        # To add horizontal gap between symbols: wrap the Vlist into
        # an Hlist and extend it with an Hbox(0, horizontal_gap)
        return vlist
