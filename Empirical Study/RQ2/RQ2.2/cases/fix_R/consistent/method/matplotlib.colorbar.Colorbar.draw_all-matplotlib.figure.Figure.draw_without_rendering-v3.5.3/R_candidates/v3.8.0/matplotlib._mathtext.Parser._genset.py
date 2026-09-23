    def _genset(self, s: str, loc: int, toks: ParseResults) -> T.Any:
        annotation = toks["annotation"]
        body = toks["body"]
        thickness = self.get_state().get_current_underline_thickness()

        annotation.shrink()
        cannotation = HCentered([annotation])
        cbody = HCentered([body])
        width = max(cannotation.width, cbody.width)
        cannotation.hpack(width, 'exactly')
        cbody.hpack(width, 'exactly')

        vgap = thickness * 3
        if s[loc + 1] == "u":  # \underset
            vlist = Vlist([cbody,                       # body
                           Vbox(0, vgap),               # space
                           cannotation                  # annotation
                           ])
            # Shift so the body sits in the same vertical position
            vlist.shift_amount = cbody.depth + cannotation.height + vgap
        else:  # \overset
            vlist = Vlist([cannotation,                 # annotation
                           Vbox(0, vgap),               # space
                           cbody                        # body
                           ])

        # To add horizontal gap between symbols: wrap the Vlist into
        # an Hlist and extend it with an Hbox(0, horizontal_gap)
        return vlist
