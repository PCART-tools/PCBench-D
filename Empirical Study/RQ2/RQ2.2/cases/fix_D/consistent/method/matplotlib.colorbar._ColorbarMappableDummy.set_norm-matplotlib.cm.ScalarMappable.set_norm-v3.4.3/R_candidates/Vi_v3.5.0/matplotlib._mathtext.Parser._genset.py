    def _genset(self, s, loc, toks):
        (annotation, body), = toks
        state = self.get_state()
        thickness = state.font_output.get_underline_thickness(
            state.font, state.fontsize, state.dpi)

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
