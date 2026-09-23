    def subsuper(self, s: str, loc: int, toks: ParseResults) -> T.Any:
        nucleus = toks.get("nucleus", Hbox(0))
        subsuper = toks.get("subsuper", [])
        napostrophes = len(toks.get("apostrophes", []))

        if not subsuper and not napostrophes:
            return nucleus

        sub = super = None
        while subsuper:
            op, arg, *subsuper = subsuper
            if op == '_':
                if sub is not None:
                    raise ParseFatalException("Double subscript")
                sub = arg
            else:
                if super is not None:
                    raise ParseFatalException("Double superscript")
                super = arg

        state = self.get_state()
        rule_thickness = state.fontset.get_underline_thickness(
            state.font, state.fontsize, state.dpi)
        xHeight = state.fontset.get_xheight(
            state.font, state.fontsize, state.dpi)

        if napostrophes:
            if super is None:
                super = Hlist([])
            for i in range(napostrophes):
                super.children.extend(self.symbol(s, loc, {"sym": "\\prime"}))
            # kern() and hpack() needed to get the metrics right after
            # extending
            super.kern()
            super.hpack()

        # Handle over/under symbols, such as sum or prod
        if self.is_overunder(nucleus):
            vlist = []
            shift = 0.
            width = nucleus.width
            if super is not None:
                super.shrink()
                width = max(width, super.width)
            if sub is not None:
                sub.shrink()
                width = max(width, sub.width)

            vgap = rule_thickness * 3.0
            if super is not None:
                hlist = HCentered([super])
                hlist.hpack(width, 'exactly')
                vlist.extend([hlist, Vbox(0, vgap)])
            hlist = HCentered([nucleus])
            hlist.hpack(width, 'exactly')
            vlist.append(hlist)
            if sub is not None:
                hlist = HCentered([sub])
                hlist.hpack(width, 'exactly')
                vlist.extend([Vbox(0, vgap), hlist])
                shift = hlist.height + vgap + nucleus.depth
            vlt = Vlist(vlist)
            vlt.shift_amount = shift
            result = Hlist([vlt])
            return [result]

        # We remove kerning on the last character for consistency (otherwise
        # it will compute kerning based on non-shrunk characters and may put
        # them too close together when superscripted)
        # We change the width of the last character to match the advance to
        # consider some fonts with weird metrics: e.g. stix's f has a width of
        # 7.75 and a kerning of -4.0 for an advance of 3.72, and we want to put
        # the superscript at the advance
        last_char = nucleus
        if isinstance(nucleus, Hlist):
            new_children = nucleus.children
            if len(new_children):
                # remove last kern
                if (isinstance(new_children[-1], Kern) and
                        hasattr(new_children[-2], '_metrics')):
                    new_children = new_children[:-1]
                last_char = new_children[-1]
                if hasattr(last_char, '_metrics'):
                    last_char.width = last_char._metrics.advance
            # create new Hlist without kerning
            nucleus = Hlist(new_children, do_kern=False)
        else:
            if isinstance(nucleus, Char):
                last_char.width = last_char._metrics.advance
            nucleus = Hlist([nucleus])

        # Handle regular sub/superscripts
        constants = _get_font_constant_set(state)
        lc_height   = last_char.height
        lc_baseline = 0
        if self.is_dropsub(last_char):
            lc_baseline = last_char.depth

        # Compute kerning for sub and super
        superkern = constants.delta * xHeight
        subkern = constants.delta * xHeight
        if self.is_slanted(last_char):
            superkern += constants.delta * xHeight
            superkern += (constants.delta_slanted *
                          (lc_height - xHeight * 2. / 3.))
            if self.is_dropsub(last_char):
                subkern = (3 * constants.delta -
                           constants.delta_integral) * lc_height
                superkern = (3 * constants.delta +
                             constants.delta_integral) * lc_height
            else:
                subkern = 0

        x: List
        if super is None:
            # node757
            # Note: One of super or sub must be a Node if we're in this function, but
            # mypy can't know this, since it can't interpret pyparsing expressions,
            # hence the cast.
            x = Hlist([Kern(subkern), T.cast(Node, sub)])
            x.shrink()
            if self.is_dropsub(last_char):
                shift_down = lc_baseline + constants.subdrop * xHeight
            else:
                shift_down = constants.sub1 * xHeight
            x.shift_amount = shift_down
        else:
            x = Hlist([Kern(superkern), super])
            x.shrink()
            if self.is_dropsub(last_char):
                shift_up = lc_height - constants.subdrop * xHeight
            else:
                shift_up = constants.sup1 * xHeight
            if sub is None:
                x.shift_amount = -shift_up
            else:  # Both sub and superscript
                y = Hlist([Kern(subkern), sub])
                y.shrink()
                if self.is_dropsub(last_char):
                    shift_down = lc_baseline + constants.subdrop * xHeight
                else:
                    shift_down = constants.sub2 * xHeight
                # If sub and superscript collide, move super up
                clr = (2.0 * rule_thickness -
                       ((shift_up - x.depth) - (y.height - shift_down)))
                if clr > 0.:
                    shift_up += clr
                x = Vlist([
                    x,
                    Kern((shift_up - x.depth) - (y.height - shift_down)),
                    y])
                x.shift_amount = shift_down

        if not self.is_dropsub(last_char):
            x.width += constants.script_space * xHeight

        # Do we need to add a space after the nucleus?
        # To find out, check the flag set by operatorname
        spaced_nucleus = [nucleus, x]
        if self._in_subscript_or_superscript:
            spaced_nucleus += [self._make_space(self._space_widths[r'\,'])]
            self._in_subscript_or_superscript = False

        result = Hlist(spaced_nucleus)
        return [result]
