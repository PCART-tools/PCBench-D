class Parser:
    """
    A pyparsing-based parser for strings containing math expressions.

    Raw text may also appear outside of pairs of ``$``.

    The grammar is based directly on that in TeX, though it cuts a few corners.
    """

    class _MathStyle(enum.Enum):
        DISPLAYSTYLE = 0
        TEXTSTYLE = 1
        SCRIPTSTYLE = 2
        SCRIPTSCRIPTSTYLE = 3

    _binary_operators = set(
      '+ * - \N{MINUS SIGN}'
      r'''
      \pm             \sqcap                   \rhd
      \mp             \sqcup                   \unlhd
      \times          \vee                     \unrhd
      \div            \wedge                   \oplus
      \ast            \setminus                \ominus
      \star           \wr                      \otimes
      \circ           \diamond                 \oslash
      \bullet         \bigtriangleup           \odot
      \cdot           \bigtriangledown         \bigcirc
      \cap            \triangleleft            \dagger
      \cup            \triangleright           \ddagger
      \uplus          \lhd                     \amalg
      \dotplus        \dotminus'''.split())

    _relation_symbols = set(r'''
      = < > :
      \leq        \geq        \equiv   \models
      \prec       \succ       \sim     \perp
      \preceq     \succeq     \simeq   \mid
      \ll         \gg         \asymp   \parallel
      \subset     \supset     \approx  \bowtie
      \subseteq   \supseteq   \cong    \Join
      \sqsubset   \sqsupset   \neq     \smile
      \sqsubseteq \sqsupseteq \doteq   \frown
      \in         \ni         \propto  \vdash
      \dashv      \dots       \doteqdot'''.split())

    _arrow_symbols = set(r'''
      \leftarrow              \longleftarrow           \uparrow
      \Leftarrow              \Longleftarrow           \Uparrow
      \rightarrow             \longrightarrow          \downarrow
      \Rightarrow             \Longrightarrow          \Downarrow
      \leftrightarrow         \longleftrightarrow      \updownarrow
      \Leftrightarrow         \Longleftrightarrow      \Updownarrow
      \mapsto                 \longmapsto              \nearrow
      \hookleftarrow          \hookrightarrow          \searrow
      \leftharpoonup          \rightharpoonup          \swarrow
      \leftharpoondown        \rightharpoondown        \nwarrow
      \rightleftharpoons      \leadsto'''.split())

    _spaced_symbols = _binary_operators | _relation_symbols | _arrow_symbols

    _punctuation_symbols = set(r', ; . ! \ldotp \cdotp'.split())

    _overunder_symbols = set(r'''
       \sum \prod \coprod \bigcap \bigcup \bigsqcup \bigvee
       \bigwedge \bigodot \bigotimes \bigoplus \biguplus
       '''.split())

    _overunder_functions = set("lim liminf limsup sup max min".split())

    _dropsub_symbols = set(r'''\int \oint'''.split())

    _fontnames = set("rm cal it tt sf bf default bb frak scr regular".split())

    _function_names = set("""
      arccos csc ker min arcsin deg lg Pr arctan det lim sec arg dim
      liminf sin cos exp limsup sinh cosh gcd ln sup cot hom log tan
      coth inf max tanh""".split())

    _ambi_delims = set(r"""
      | \| / \backslash \uparrow \downarrow \updownarrow \Uparrow
      \Downarrow \Updownarrow . \vert \Vert""".split())
    _left_delims = set(r"( [ \{ < \lfloor \langle \lceil".split())
    _right_delims = set(r") ] \} > \rfloor \rangle \rceil".split())
    _delims = _left_delims | _right_delims | _ambi_delims

    def __init__(self):
        p = types.SimpleNamespace()

        def set_names_and_parse_actions():
            for key, val in vars(p).items():
                if not key.startswith('_'):
                    # Set names on everything -- very useful for debugging
                    val.setName(key)
                    # Set actions
                    if hasattr(self, key):
                        val.setParseAction(getattr(self, key))

        # Root definitions.

        # In TeX parlance, a csname is a control sequence name (a "\foo").
        def csnames(group, names):
            ends_with_alpha = []
            ends_with_nonalpha = []
            for name in names:
                if name[-1].isalpha():
                    ends_with_alpha.append(name)
                else:
                    ends_with_nonalpha.append(name)
            return Regex(r"\\(?P<{}>(?:{})(?![A-Za-z]){})".format(
                group,
                "|".join(map(re.escape, ends_with_alpha)),
                "".join(f"|{s}" for s in map(re.escape, ends_with_nonalpha)),
            ))

        p.float_literal  = Regex(r"[-+]?([0-9]+\.?[0-9]*|\.[0-9]+)")
        p.space          = oneOf(self._space_widths)("space")

        p.style_literal  = oneOf(
            [str(e.value) for e in self._MathStyle])("style_literal")

        p.symbol         = Regex(
            r"[a-zA-Z0-9 +\-*/<>=:,.;!\?&'@()\[\]|\U00000080-\U0001ffff]"
            r"|\\[%${}\[\]_|]"
            + r"|\\(?:{})(?![A-Za-z])".format(
                "|".join(map(re.escape, tex2uni)))
        )("sym").leaveWhitespace()
        p.unknown_symbol = Regex(r"\\[A-Za-z]*")("name")

        p.font           = csnames("font", self._fontnames)
        p.start_group    = (
            Optional(r"\math" + oneOf(self._fontnames)("font")) + "{")
        p.end_group      = Literal("}")

        p.delim          = oneOf(self._delims)

        set_names_and_parse_actions()  # for root definitions.

        # Mutually recursive definitions.  (Minimizing the number of Forward
        # elements is important for speed.)
        p.accent           = Forward()
        p.auto_delim       = Forward()
        p.binom            = Forward()
        p.customspace      = Forward()
        p.frac             = Forward()
        p.dfrac            = Forward()
        p.function         = Forward()
        p.genfrac          = Forward()
        p.group            = Forward()
        p.operatorname     = Forward()
        p.overline         = Forward()
        p.overset          = Forward()
        p.placeable        = Forward()
        p.required_group   = Forward()
        p.simple           = Forward()
        p.optional_group   = Forward()
        p.sqrt             = Forward()
        p.subsuper         = Forward()
        p.token            = Forward()
        p.underset         = Forward()

        set_names_and_parse_actions()  # for mutually recursive definitions.

        p.customspace <<= cmd(r"\hspace", "{" + p.float_literal("space") + "}")

        p.accent <<= (
            csnames("accent", [*self._accent_map, *self._wide_accents])
            - p.placeable("sym"))

        p.function <<= csnames("name", self._function_names)
        p.operatorname <<= cmd(
            r"\operatorname",
            "{" + ZeroOrMore(p.simple | p.unknown_symbol)("name") + "}")

        p.group <<= p.start_group + ZeroOrMore(p.token)("group") + p.end_group

        p.optional_group <<= "{" + ZeroOrMore(p.token)("group") + "}"
        p.required_group <<= "{" + OneOrMore(p.token)("group") + "}"

        p.frac  <<= cmd(
            r"\frac", p.required_group("num") + p.required_group("den"))
        p.dfrac <<= cmd(
            r"\dfrac", p.required_group("num") + p.required_group("den"))
        p.binom <<= cmd(
            r"\binom", p.required_group("num") + p.required_group("den"))

        p.genfrac <<= cmd(
            r"\genfrac",
            "{" + Optional(p.delim)("ldelim") + "}"
            + "{" + Optional(p.delim)("rdelim") + "}"
            + "{" + p.float_literal("rulesize") + "}"
            + "{" + Optional(p.style_literal)("style") + "}"
            + p.required_group("num")
            + p.required_group("den"))

        p.sqrt <<= cmd(
            r"\sqrt{value}",
            Optional("[" + OneOrMore(NotAny("]") + p.token)("root") + "]")
            + p.required_group("value"))

        p.overline <<= cmd(r"\overline", p.required_group("body"))

        p.overset  <<= cmd(
            r"\overset",
            p.optional_group("annotation") + p.optional_group("body"))
        p.underset <<= cmd(
            r"\underset",
            p.optional_group("annotation") + p.optional_group("body"))

        p.placeable     <<= (
            p.accent     # Must be before symbol as all accents are symbols
            | p.symbol   # Must be second to catch all named symbols and single
                         # chars not in a group
            | p.function
            | p.operatorname
            | p.group
            | p.frac
            | p.dfrac
            | p.binom
            | p.genfrac
            | p.overset
            | p.underset
            | p.sqrt
            | p.overline
        )

        p.simple        <<= (
            p.space
            | p.customspace
            | p.font
            | p.subsuper
        )

        p.subsuper      <<= (
            (Optional(p.placeable)("nucleus")
             + OneOrMore(oneOf(["_", "^"]) - p.placeable)("subsuper")
             + Regex("'*")("apostrophes"))
            | Regex("'+")("apostrophes")
            | (p.placeable("nucleus") + Regex("'*")("apostrophes"))
        )

        p.token         <<= (
            p.simple
            | p.auto_delim
            | p.unknown_symbol  # Must be last
        )

        p.auto_delim    <<= (
            r"\left" - (p.delim("left") | Error("Expected a delimiter"))
            + ZeroOrMore(p.simple | p.auto_delim)("mid")
            + r"\right" - (p.delim("right") | Error("Expected a delimiter"))
        )

        # Leaf definitions.
        p.math          = OneOrMore(p.token)
        p.math_string   = QuotedString('$', '\\', unquoteResults=False)
        p.non_math      = Regex(r"(?:(?:\\[$])|[^$])*").leaveWhitespace()
        p.main          = (
            p.non_math + ZeroOrMore(p.math_string + p.non_math) + StringEnd()
        )
        set_names_and_parse_actions()  # for leaf definitions.

        self._expression = p.main
        self._math_expression = p.math

        # To add space to nucleus operators after sub/superscripts
        self._in_subscript_or_superscript = False

    def parse(self, s, fonts_object, fontsize, dpi):
        """
        Parse expression *s* using the given *fonts_object* for
        output, at the given *fontsize* and *dpi*.

        Returns the parse tree of `Node` instances.
        """
        self._state_stack = [
            ParserState(fonts_object, 'default', 'rm', fontsize, dpi)]
        self._em_width_cache = {}
        try:
            result = self._expression.parseString(s)
        except ParseBaseException as err:
            raise ValueError("\n".join(["",
                                        err.line,
                                        " " * (err.column - 1) + "^",
                                        str(err)])) from err
        self._state_stack = None
        self._in_subscript_or_superscript = False
        # prevent operator spacing from leaking into a new expression
        self._em_width_cache = {}
        self._expression.resetCache()
        return result[0]

    def get_state(self):
        """Get the current `State` of the parser."""
        return self._state_stack[-1]

    def pop_state(self):
        """Pop a `State` off of the stack."""
        self._state_stack.pop()

    def push_state(self):
        """Push a new `State` onto the stack, copying the current state."""
        self._state_stack.append(self.get_state().copy())

    def main(self, s, loc, toks):
        return [Hlist(toks)]

    def math_string(self, s, loc, toks):
        return self._math_expression.parseString(toks[0][1:-1])

    def math(self, s, loc, toks):
        hlist = Hlist(toks)
        self.pop_state()
        return [hlist]

    def non_math(self, s, loc, toks):
        s = toks[0].replace(r'\$', '$')
        symbols = [Char(c, self.get_state()) for c in s]
        hlist = Hlist(symbols)
        # We're going into math now, so set font to 'it'
        self.push_state()
        self.get_state().font = mpl.rcParams['mathtext.default']
        return [hlist]

    float_literal = staticmethod(pyparsing_common.convertToFloat)

    def _make_space(self, percentage):
        # In TeX, an em (the unit usually used to measure horizontal lengths)
        # is not the width of the character 'm'; it is the same in different
        # font styles (e.g. roman or italic). Mathtext, however, uses 'm' in
        # the italic style so that horizontal spaces don't depend on the
        # current font style.
        state = self.get_state()
        key = (state.font, state.fontsize, state.dpi)
        width = self._em_width_cache.get(key)
        if width is None:
            metrics = state.fontset.get_metrics(
                'it', mpl.rcParams['mathtext.default'], 'm',
                state.fontsize, state.dpi)
            width = metrics.advance
            self._em_width_cache[key] = width
        return Kern(width * percentage)

    _space_widths = {
        r'\,':         0.16667,   # 3/18 em = 3 mu
        r'\thinspace': 0.16667,   # 3/18 em = 3 mu
        r'\/':         0.16667,   # 3/18 em = 3 mu
        r'\>':         0.22222,   # 4/18 em = 4 mu
        r'\:':         0.22222,   # 4/18 em = 4 mu
        r'\;':         0.27778,   # 5/18 em = 5 mu
        r'\ ':         0.33333,   # 6/18 em = 6 mu
        r'~':          0.33333,   # 6/18 em = 6 mu, nonbreakable
        r'\enspace':   0.5,       # 9/18 em = 9 mu
        r'\quad':      1,         # 1 em = 18 mu
        r'\qquad':     2,         # 2 em = 36 mu
        r'\!':         -0.16667,  # -3/18 em = -3 mu
    }

    def space(self, s, loc, toks):
        num = self._space_widths[toks["space"]]
        box = self._make_space(num)
        return [box]

    def customspace(self, s, loc, toks):
        return [self._make_space(toks["space"])]

    def symbol(self, s, loc, toks):
        c = toks["sym"]
        if c == "-":
            # "U+2212 minus sign is the preferred representation of the unary
            # and binary minus sign rather than the ASCII-derived U+002D
            # hyphen-minus, because minus sign is unambiguous and because it
            # is rendered with a more desirable length, usually longer than a
            # hyphen." (https://www.unicode.org/reports/tr25/)
            c = "\N{MINUS SIGN}"
        try:
            char = Char(c, self.get_state())
        except ValueError as err:
            raise ParseFatalException(s, loc,
                                      "Unknown symbol: %s" % c) from err

        if c in self._spaced_symbols:
            # iterate until we find previous character, needed for cases
            # such as ${ -2}$, $ -2$, or $   -2$.
            prev_char = next((c for c in s[:loc][::-1] if c != ' '), '')
            # Binary operators at start of string should not be spaced
            if (c in self._binary_operators and
                    (len(s[:loc].split()) == 0 or prev_char == '{' or
                     prev_char in self._left_delims)):
                return [char]
            else:
                return [Hlist([self._make_space(0.2),
                               char,
                               self._make_space(0.2)],
                              do_kern=True)]
        elif c in self._punctuation_symbols:
            prev_char = next((c for c in s[:loc][::-1] if c != ' '), '')
            next_char = next((c for c in s[loc + 1:] if c != ' '), '')

            # Do not space commas between brackets
            if c == ',':
                if prev_char == '{' and next_char == '}':
                    return [char]

            # Do not space dots as decimal separators
            if c == '.' and prev_char.isdigit() and next_char.isdigit():
                return [char]
            else:
                return [Hlist([char, self._make_space(0.2)], do_kern=True)]
        return [char]

    def unknown_symbol(self, s, loc, toks):
        raise ParseFatalException(s, loc, f"Unknown symbol: {toks['name']}")

    _accent_map = {
        r'hat':            r'\circumflexaccent',
        r'breve':          r'\combiningbreve',
        r'bar':            r'\combiningoverline',
        r'grave':          r'\combininggraveaccent',
        r'acute':          r'\combiningacuteaccent',
        r'tilde':          r'\combiningtilde',
        r'dot':            r'\combiningdotabove',
        r'ddot':           r'\combiningdiaeresis',
        r'dddot':          r'\combiningthreedotsabove',
        r'ddddot':         r'\combiningfourdotsabove',
        r'vec':            r'\combiningrightarrowabove',
        r'"':              r'\combiningdiaeresis',
        r"`":              r'\combininggraveaccent',
        r"'":              r'\combiningacuteaccent',
        r'~':              r'\combiningtilde',
        r'.':              r'\combiningdotabove',
        r'^':              r'\circumflexaccent',
        r'overrightarrow': r'\rightarrow',
        r'overleftarrow':  r'\leftarrow',
        r'mathring':       r'\circ',
    }

    _wide_accents = set(r"widehat widetilde widebar".split())

    def accent(self, s, loc, toks):
        state = self.get_state()
        thickness = state.get_current_underline_thickness()
        accent = toks["accent"]
        sym = toks["sym"]
        if accent in self._wide_accents:
            accent_box = AutoWidthChar(
                '\\' + accent, sym.width, state, char_class=Accent)
        else:
            accent_box = Accent(self._accent_map[accent], state)
        if accent == 'mathring':
            accent_box.shrink()
            accent_box.shrink()
        centered = HCentered([Hbox(sym.width / 4.0), accent_box])
        centered.hpack(sym.width, 'exactly')
        return Vlist([
                centered,
                Vbox(0., thickness * 2.0),
                Hlist([sym])
                ])

    def function(self, s, loc, toks):
        hlist = self.operatorname(s, loc, toks)
        hlist.function_name = toks["name"]
        return hlist

    def operatorname(self, s, loc, toks):
        self.push_state()
        state = self.get_state()
        state.font = 'rm'
        hlist_list = []
        # Change the font of Chars, but leave Kerns alone
        name = toks["name"]
        for c in name:
            if isinstance(c, Char):
                c.font = 'rm'
                c._update_metrics()
                hlist_list.append(c)
            elif isinstance(c, str):
                hlist_list.append(Char(c, state))
            else:
                hlist_list.append(c)
        next_char_loc = loc + len(name) + 1
        if isinstance(name, ParseResults):
            next_char_loc += len('operatorname{}')
        next_char = next((c for c in s[next_char_loc:] if c != ' '), '')
        delimiters = self._delims | {'^', '_'}
        if (next_char not in delimiters and
                name not in self._overunder_functions):
            # Add thin space except when followed by parenthesis, bracket, etc.
            hlist_list += [self._make_space(self._space_widths[r'\,'])]
        self.pop_state()
        # if followed by a super/subscript, set flag to true
        # This flag tells subsuper to add space after this operator
        if next_char in {'^', '_'}:
            self._in_subscript_or_superscript = True
        else:
            self._in_subscript_or_superscript = False

        return Hlist(hlist_list)

    def start_group(self, s, loc, toks):
        self.push_state()
        # Deal with LaTeX-style font tokens
        if toks.get("font"):
            self.get_state().font = toks.get("font")
        return []

    def group(self, s, loc, toks):
        grp = Hlist(toks.get("group", []))
        return [grp]

    def required_group(self, s, loc, toks):
        return Hlist(toks.get("group", []))

    optional_group = required_group

    def end_group(self, s, loc, toks):
        self.pop_state()
        return []

    def font(self, s, loc, toks):
        self.get_state().font = toks["font"]
        return []

    def is_overunder(self, nucleus):
        if isinstance(nucleus, Char):
            return nucleus.c in self._overunder_symbols
        elif isinstance(nucleus, Hlist) and hasattr(nucleus, 'function_name'):
            return nucleus.function_name in self._overunder_functions
        return False

    def is_dropsub(self, nucleus):
        if isinstance(nucleus, Char):
            return nucleus.c in self._dropsub_symbols
        return False

    def is_slanted(self, nucleus):
        if isinstance(nucleus, Char):
            return nucleus.is_slanted()
        return False

    def is_between_brackets(self, s, loc):
        return False

    def subsuper(self, s, loc, toks):
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
            vlist = Vlist(vlist)
            vlist.shift_amount = shift
            result = Hlist([vlist])
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

        if super is None:
            # node757
            x = Hlist([Kern(subkern), sub])
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

    def _genfrac(self, ldelim, rdelim, rule, style, num, den):
        state = self.get_state()
        thickness = state.get_current_underline_thickness()

        for _ in range(style.value):
            num.shrink()
            den.shrink()
        cnum = HCentered([num])
        cden = HCentered([den])
        width = max(num.width, den.width)
        cnum.hpack(width, 'exactly')
        cden.hpack(width, 'exactly')
        vlist = Vlist([cnum,                      # numerator
                       Vbox(0, thickness * 2.0),  # space
                       Hrule(state, rule),        # rule
                       Vbox(0, thickness * 2.0),  # space
                       cden                       # denominator
                       ])

        # Shift so the fraction line sits in the middle of the
        # equals sign
        metrics = state.fontset.get_metrics(
            state.font, mpl.rcParams['mathtext.default'],
            '=', state.fontsize, state.dpi)
        shift = (cden.height -
                 ((metrics.ymax + metrics.ymin) / 2 -
                  thickness * 3.0))
        vlist.shift_amount = shift

        result = [Hlist([vlist, Hbox(thickness * 2.)])]
        if ldelim or rdelim:
            if ldelim == '':
                ldelim = '.'
            if rdelim == '':
                rdelim = '.'
            return self._auto_sized_delimiter(ldelim, result, rdelim)
        return result

    def style_literal(self, s, loc, toks):
        return self._MathStyle(int(toks["style_literal"]))

    def genfrac(self, s, loc, toks):
        return self._genfrac(
            toks.get("ldelim", ""), toks.get("rdelim", ""),
            toks["rulesize"], toks.get("style", self._MathStyle.TEXTSTYLE),
            toks["num"], toks["den"])

    def frac(self, s, loc, toks):
        return self._genfrac(
            "", "", self.get_state().get_current_underline_thickness(),
            self._MathStyle.TEXTSTYLE, toks["num"], toks["den"])

    def dfrac(self, s, loc, toks):
        return self._genfrac(
            "", "", self.get_state().get_current_underline_thickness(),
            self._MathStyle.DISPLAYSTYLE, toks["num"], toks["den"])

    def binom(self, s, loc, toks):
        return self._genfrac(
            "(", ")", 0,
            self._MathStyle.TEXTSTYLE, toks["num"], toks["den"])

    def _genset(self, s, loc, toks):
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

    overset = underset = _genset

    def sqrt(self, s, loc, toks):
        root = toks.get("root")
        body = toks["value"]
        state = self.get_state()
        thickness = state.get_current_underline_thickness()

        # Determine the height of the body, and add a little extra to
        # the height so it doesn't seem cramped
        height = body.height - body.shift_amount + thickness * 5.0
        depth = body.depth + body.shift_amount
        check = AutoHeightChar(r'\__sqrt__', height, depth, state, always=True)
        height = check.height - check.shift_amount
        depth = check.depth + check.shift_amount

        # Put a little extra space to the left and right of the body
        padded_body = Hlist([Hbox(2 * thickness), body, Hbox(2 * thickness)])
        rightside = Vlist([Hrule(state), Glue('fill'), padded_body])
        # Stretch the glue between the hrule and the body
        rightside.vpack(height + (state.fontsize * state.dpi) / (100.0 * 12.0),
                        'exactly', depth)

        # Add the root and shift it upward so it is above the tick.
        # The value of 0.6 is a hard-coded hack ;)
        if not root:
            root = Box(check.width * 0.5, 0., 0.)
        else:
            root = Hlist(root)
            root.shrink()
            root.shrink()

        root_vlist = Vlist([Hlist([root])])
        root_vlist.shift_amount = -height * 0.6

        hlist = Hlist([root_vlist,               # Root
                       # Negative kerning to put root over tick
                       Kern(-check.width * 0.5),
                       check,                    # Check
                       rightside])               # Body
        return [hlist]

    def overline(self, s, loc, toks):
        body = toks["body"]

        state = self.get_state()
        thickness = state.get_current_underline_thickness()

        height = body.height - body.shift_amount + thickness * 3.0
        depth = body.depth + body.shift_amount

        # Place overline above body
        rightside = Vlist([Hrule(state), Glue('fill'), Hlist([body])])

        # Stretch the glue between the hrule and the body
        rightside.vpack(height + (state.fontsize * state.dpi) / (100.0 * 12.0),
                        'exactly', depth)

        hlist = Hlist([rightside])
        return [hlist]

    def _auto_sized_delimiter(self, front, middle, back):
        state = self.get_state()
        if len(middle):
            height = max(x.height for x in middle)
            depth = max(x.depth for x in middle)
            factor = None
        else:
            height = 0
            depth = 0
            factor = 1.0
        parts = []
        # \left. and \right. aren't supposed to produce any symbols
        if front != '.':
            parts.append(
                AutoHeightChar(front, height, depth, state, factor=factor))
        parts.extend(middle)
        if back != '.':
            parts.append(
                AutoHeightChar(back, height, depth, state, factor=factor))
        hlist = Hlist(parts)
        return hlist

    def auto_delim(self, s, loc, toks):
        return self._auto_sized_delimiter(
            toks["left"],
            # if "mid" in toks ... can be removed when requiring pyparsing 3.
            toks["mid"].asList() if "mid" in toks else [],
            toks["right"])
