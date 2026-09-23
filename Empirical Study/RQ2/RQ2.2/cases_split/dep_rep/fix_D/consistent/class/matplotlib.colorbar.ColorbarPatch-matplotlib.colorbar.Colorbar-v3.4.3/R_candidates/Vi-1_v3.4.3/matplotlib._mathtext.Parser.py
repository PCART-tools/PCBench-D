class Parser:
    """
    A pyparsing-based parser for strings containing math expressions.

    Raw text may also appear outside of pairs of ``$``.

    The grammar is based directly on that in TeX, though it cuts a few corners.
    """

    class _MathStyle(enum.Enum):
        DISPLAYSTYLE = enum.auto()
        TEXTSTYLE = enum.auto()
        SCRIPTSTYLE = enum.auto()
        SCRIPTSCRIPTSTYLE = enum.auto()

    _binary_operators = set('''
      + * -
      \\pm             \\sqcap                   \\rhd
      \\mp             \\sqcup                   \\unlhd
      \\times          \\vee                     \\unrhd
      \\div            \\wedge                   \\oplus
      \\ast            \\setminus                \\ominus
      \\star           \\wr                      \\otimes
      \\circ           \\diamond                 \\oslash
      \\bullet         \\bigtriangleup           \\odot
      \\cdot           \\bigtriangledown         \\bigcirc
      \\cap            \\triangleleft            \\dagger
      \\cup            \\triangleright           \\ddagger
      \\uplus          \\lhd                     \\amalg'''.split())

    _relation_symbols = set('''
      = < > :
      \\leq        \\geq        \\equiv   \\models
      \\prec       \\succ       \\sim     \\perp
      \\preceq     \\succeq     \\simeq   \\mid
      \\ll         \\gg         \\asymp   \\parallel
      \\subset     \\supset     \\approx  \\bowtie
      \\subseteq   \\supseteq   \\cong    \\Join
      \\sqsubset   \\sqsupset   \\neq     \\smile
      \\sqsubseteq \\sqsupseteq \\doteq   \\frown
      \\in         \\ni         \\propto  \\vdash
      \\dashv      \\dots       \\dotplus \\doteqdot'''.split())

    _arrow_symbols = set('''
      \\leftarrow              \\longleftarrow           \\uparrow
      \\Leftarrow              \\Longleftarrow           \\Uparrow
      \\rightarrow             \\longrightarrow          \\downarrow
      \\Rightarrow             \\Longrightarrow          \\Downarrow
      \\leftrightarrow         \\longleftrightarrow      \\updownarrow
      \\Leftrightarrow         \\Longleftrightarrow      \\Updownarrow
      \\mapsto                 \\longmapsto              \\nearrow
      \\hookleftarrow          \\hookrightarrow          \\searrow
      \\leftharpoonup          \\rightharpoonup          \\swarrow
      \\leftharpoondown        \\rightharpoondown        \\nwarrow
      \\rightleftharpoons      \\leadsto'''.split())

    _spaced_symbols = _binary_operators | _relation_symbols | _arrow_symbols

    _punctuation_symbols = set(r', ; . ! \ldotp \cdotp'.split())

    _overunder_symbols = set(r'''
       \sum \prod \coprod \bigcap \bigcup \bigsqcup \bigvee
       \bigwedge \bigodot \bigotimes \bigoplus \biguplus
       '''.split())

    _overunder_functions = set(
        "lim liminf limsup sup max min".split())

    _dropsub_symbols = set(r'''\int \oint'''.split())

    _fontnames = set("rm cal it tt sf bf default bb frak scr regular".split())

    _function_names = set("""
      arccos csc ker min arcsin deg lg Pr arctan det lim sec arg dim
      liminf sin cos exp limsup sinh cosh gcd ln sup cot hom log tan
      coth inf max tanh""".split())

    _ambi_delim = set("""
      | \\| / \\backslash \\uparrow \\downarrow \\updownarrow \\Uparrow
      \\Downarrow \\Updownarrow . \\vert \\Vert \\\\|""".split())

    _left_delim = set(r"( [ \{ < \lfloor \langle \lceil".split())

    _right_delim = set(r") ] \} > \rfloor \rangle \rceil".split())

    def __init__(self):
        p = types.SimpleNamespace()
        # All forward declarations are here
        p.accent           = Forward()
        p.ambi_delim       = Forward()
        p.apostrophe       = Forward()
        p.auto_delim       = Forward()
        p.binom            = Forward()
        p.bslash           = Forward()
        p.c_over_c         = Forward()
        p.customspace      = Forward()
        p.end_group        = Forward()
        p.float_literal    = Forward()
        p.font             = Forward()
        p.frac             = Forward()
        p.dfrac            = Forward()
        p.function         = Forward()
        p.genfrac          = Forward()
        p.group            = Forward()
        p.int_literal      = Forward()
        p.latexfont        = Forward()
        p.lbracket         = Forward()
        p.left_delim       = Forward()
        p.lbrace           = Forward()
        p.main             = Forward()
        p.math             = Forward()
        p.math_string      = Forward()
        p.non_math         = Forward()
        p.operatorname     = Forward()
        p.overline         = Forward()
        p.overset          = Forward()
        p.placeable        = Forward()
        p.rbrace           = Forward()
        p.rbracket         = Forward()
        p.required_group   = Forward()
        p.right_delim      = Forward()
        p.right_delim_safe = Forward()
        p.simple           = Forward()
        p.simple_group     = Forward()
        p.single_symbol    = Forward()
        p.accentprefixed   = Forward()
        p.space            = Forward()
        p.sqrt             = Forward()
        p.start_group      = Forward()
        p.subsuper         = Forward()
        p.subsuperop       = Forward()
        p.symbol           = Forward()
        p.symbol_name      = Forward()
        p.token            = Forward()
        p.underset         = Forward()
        p.unknown_symbol   = Forward()

        # Set names on everything -- very useful for debugging
        for key, val in vars(p).items():
            if not key.startswith('_'):
                val.setName(key)

        p.float_literal <<= Regex(r"[-+]?([0-9]+\.?[0-9]*|\.[0-9]+)")
        p.int_literal   <<= Regex("[-+]?[0-9]+")

        p.lbrace        <<= Literal('{').suppress()
        p.rbrace        <<= Literal('}').suppress()
        p.lbracket      <<= Literal('[').suppress()
        p.rbracket      <<= Literal(']').suppress()
        p.bslash        <<= Literal('\\')

        p.space         <<= oneOf(list(self._space_widths))
        p.customspace   <<= (
            Suppress(Literal(r'\hspace'))
            - ((p.lbrace + p.float_literal + p.rbrace)
               | Error(r"Expected \hspace{n}"))
        )

        unicode_range = "\U00000080-\U0001ffff"
        p.single_symbol <<= Regex(
            r"([a-zA-Z0-9 +\-*/<>=:,.;!\?&'@()\[\]|%s])|(\\[%%${}\[\]_|])" %
            unicode_range)
        p.accentprefixed <<= Suppress(p.bslash) + oneOf(self._accentprefixed)
        p.symbol_name   <<= (
            Combine(p.bslash + oneOf(list(tex2uni)))
            + FollowedBy(Regex("[^A-Za-z]").leaveWhitespace() | StringEnd())
        )
        p.symbol        <<= (p.single_symbol | p.symbol_name).leaveWhitespace()

        p.apostrophe    <<= Regex("'+")

        p.c_over_c      <<= (
            Suppress(p.bslash)
            + oneOf(list(self._char_over_chars))
        )

        p.accent        <<= Group(
            Suppress(p.bslash)
            + oneOf([*self._accent_map, *self._wide_accents])
            - p.placeable
        )

        p.function      <<= (
            Suppress(p.bslash)
            + oneOf(list(self._function_names))
        )

        p.start_group    <<= Optional(p.latexfont) + p.lbrace
        p.end_group      <<= p.rbrace.copy()
        p.simple_group   <<= Group(p.lbrace + ZeroOrMore(p.token) + p.rbrace)
        p.required_group <<= Group(p.lbrace + OneOrMore(p.token) + p.rbrace)
        p.group          <<= Group(
            p.start_group + ZeroOrMore(p.token) + p.end_group
        )

        p.font          <<= Suppress(p.bslash) + oneOf(list(self._fontnames))
        p.latexfont     <<= (
            Suppress(p.bslash)
            + oneOf(['math' + x for x in self._fontnames])
        )

        p.frac          <<= Group(
            Suppress(Literal(r"\frac"))
            - ((p.required_group + p.required_group)
               | Error(r"Expected \frac{num}{den}"))
        )

        p.dfrac         <<= Group(
            Suppress(Literal(r"\dfrac"))
            - ((p.required_group + p.required_group)
               | Error(r"Expected \dfrac{num}{den}"))
        )

        p.binom         <<= Group(
            Suppress(Literal(r"\binom"))
            - ((p.required_group + p.required_group)
               | Error(r"Expected \binom{num}{den}"))
        )

        p.ambi_delim    <<= oneOf(list(self._ambi_delim))
        p.left_delim    <<= oneOf(list(self._left_delim))
        p.right_delim   <<= oneOf(list(self._right_delim))
        p.right_delim_safe <<= oneOf([*(self._right_delim - {'}'}), r'\}'])

        p.genfrac <<= Group(
            Suppress(Literal(r"\genfrac"))
            - (((p.lbrace
                 + Optional(p.ambi_delim | p.left_delim, default='')
                 + p.rbrace)
                + (p.lbrace
                   + Optional(p.ambi_delim | p.right_delim_safe, default='')
                   + p.rbrace)
                + (p.lbrace + p.float_literal + p.rbrace)
                + p.simple_group + p.required_group + p.required_group)
               | Error("Expected "
                       r"\genfrac{ldelim}{rdelim}{rulesize}{style}{num}{den}"))
        )

        p.sqrt <<= Group(
            Suppress(Literal(r"\sqrt"))
            - ((Group(Optional(
                p.lbracket + OneOrMore(~p.rbracket + p.token) + p.rbracket))
                + p.required_group)
               | Error("Expected \\sqrt{value}"))
        )

        p.overline <<= Group(
            Suppress(Literal(r"\overline"))
            - (p.required_group | Error("Expected \\overline{value}"))
        )

        p.overset <<= Group(
            Suppress(Literal(r"\overset"))
            - ((p.simple_group + p.simple_group)
               | Error("Expected \\overset{body}{annotation}"))
        )

        p.underset <<= Group(
            Suppress(Literal(r"\underset"))
            - ((p.simple_group + p.simple_group)
               | Error("Expected \\underset{body}{annotation}"))
        )

        p.unknown_symbol <<= Combine(p.bslash + Regex("[A-Za-z]*"))

        p.operatorname <<= Group(
            Suppress(Literal(r"\operatorname"))
            - ((p.lbrace + ZeroOrMore(p.simple | p.unknown_symbol) + p.rbrace)
               | Error("Expected \\operatorname{value}"))
        )

        p.placeable     <<= (
            p.accentprefixed  # Must be before accent so named symbols that are
                              # prefixed with an accent name work
            | p.accent   # Must be before symbol as all accents are symbols
            | p.symbol   # Must be third to catch all named symbols and single
                         # chars not in a group
            | p.c_over_c
            | p.function
            | p.group
            | p.frac
            | p.dfrac
            | p.binom
            | p.genfrac
            | p.overset
            | p.underset
            | p.sqrt
            | p.overline
            | p.operatorname
        )

        p.simple        <<= (
            p.space
            | p.customspace
            | p.font
            | p.subsuper
        )

        p.subsuperop    <<= oneOf(["_", "^"])

        p.subsuper      <<= Group(
            (Optional(p.placeable)
             + OneOrMore(p.subsuperop - p.placeable)
             + Optional(p.apostrophe))
            | (p.placeable + Optional(p.apostrophe))
            | p.apostrophe
        )

        p.token         <<= (
            p.simple
            | p.auto_delim
            | p.unknown_symbol  # Must be last
        )

        p.auto_delim    <<= (
            Suppress(Literal(r"\left"))
            - ((p.left_delim | p.ambi_delim)
               | Error("Expected a delimiter"))
            + Group(ZeroOrMore(p.simple | p.auto_delim))
            + Suppress(Literal(r"\right"))
            - ((p.right_delim | p.ambi_delim)
               | Error("Expected a delimiter"))
        )

        p.math          <<= OneOrMore(p.token)

        p.math_string   <<= QuotedString('$', '\\', unquoteResults=False)

        p.non_math      <<= Regex(r"(?:(?:\\[$])|[^$])*").leaveWhitespace()

        p.main          <<= (
            p.non_math + ZeroOrMore(p.math_string + p.non_math) + StringEnd()
        )

        # Set actions
        for key, val in vars(p).items():
            if not key.startswith('_'):
                if hasattr(self, key):
                    val.setParseAction(getattr(self, key))

        self._expression = p.main
        self._math_expression = p.math

    def parse(self, s, fonts_object, fontsize, dpi):
        """
        Parse expression *s* using the given *fonts_object* for
        output, at the given *fontsize* and *dpi*.

        Returns the parse tree of `Node` instances.
        """
        self._state_stack = [
            self.State(fonts_object, 'default', 'rm', fontsize, dpi)]
        self._em_width_cache = {}
        try:
            result = self._expression.parseString(s)
        except ParseBaseException as err:
            raise ValueError("\n".join(["",
                                        err.line,
                                        " " * (err.column - 1) + "^",
                                        str(err)])) from err
        self._state_stack = None
        self._em_width_cache = {}
        self._expression.resetCache()
        return result[0]

    # The state of the parser is maintained in a stack.  Upon
    # entering and leaving a group { } or math/non-math, the stack
    # is pushed and popped accordingly.  The current state always
    # exists in the top element of the stack.
    class State:
        """
        Stores the state of the parser.

        States are pushed and popped from a stack as necessary, and
        the "current" state is always at the top of the stack.
        """
        def __init__(self, font_output, font, font_class, fontsize, dpi):
            self.font_output = font_output
            self._font = font
            self.font_class = font_class
            self.fontsize = fontsize
            self.dpi = dpi

        def copy(self):
            return Parser.State(
                self.font_output,
                self.font,
                self.font_class,
                self.fontsize,
                self.dpi)

        @property
        def font(self):
            return self._font

        @font.setter
        def font(self, name):
            if name in ('rm', 'it', 'bf'):
                self.font_class = name
            self._font = name

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
        symbols = [Char(c, self.get_state(), math=False) for c in s]
        hlist = Hlist(symbols)
        # We're going into math now, so set font to 'it'
        self.push_state()
        self.get_state().font = mpl.rcParams['mathtext.default']
        return [hlist]

    def _make_space(self, percentage):
        # All spaces are relative to em width
        state = self.get_state()
        key = (state.font, state.fontsize, state.dpi)
        width = self._em_width_cache.get(key)
        if width is None:
            metrics = state.font_output.get_metrics(
                state.font, mpl.rcParams['mathtext.default'], 'm',
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
        tok, = toks
        num = self._space_widths[tok]
        box = self._make_space(num)
        return [box]

    def customspace(self, s, loc, toks):
        return [self._make_space(float(toks[0]))]

    def symbol(self, s, loc, toks):
        c, = toks
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
                     prev_char in self._left_delim)):
                return [char]
            else:
                return [Hlist([self._make_space(0.2),
                               char,
                               self._make_space(0.2)],
                              do_kern=True)]
        elif c in self._punctuation_symbols:

            # Do not space commas between brackets
            if c == ',':
                prev_char = next((c for c in s[:loc][::-1] if c != ' '), '')
                next_char = next((c for c in s[loc + 1:] if c != ' '), '')
                if prev_char == '{' and next_char == '}':
                    return [char]

            # Do not space dots as decimal separators
            if c == '.' and s[loc - 1].isdigit() and s[loc + 1].isdigit():
                return [char]
            else:
                return [Hlist([char, self._make_space(0.2)], do_kern=True)]
        return [char]

    accentprefixed = symbol

    def unknown_symbol(self, s, loc, toks):
        c, = toks
        raise ParseFatalException(s, loc, "Unknown symbol: %s" % c)

    _char_over_chars = {
        # The first 2 entries in the tuple are (font, char, sizescale) for
        # the two symbols under and over.  The third element is the space
        # (in multiples of underline height)
        r'AA': (('it', 'A', 1.0), (None, '\\circ', 0.5), 0.0),
    }

    def c_over_c(self, s, loc, toks):
        sym, = toks
        state = self.get_state()
        thickness = state.font_output.get_underline_thickness(
            state.font, state.fontsize, state.dpi)

        under_desc, over_desc, space = \
            self._char_over_chars.get(sym, (None, None, 0.0))
        if under_desc is None:
            raise ParseFatalException("Error parsing symbol")

        over_state = state.copy()
        if over_desc[0] is not None:
            over_state.font = over_desc[0]
        over_state.fontsize *= over_desc[2]
        over = Accent(over_desc[1], over_state)

        under_state = state.copy()
        if under_desc[0] is not None:
            under_state.font = under_desc[0]
        under_state.fontsize *= under_desc[2]
        under = Char(under_desc[1], under_state)

        width = max(over.width, under.width)

        over_centered = HCentered([over])
        over_centered.hpack(width, 'exactly')

        under_centered = HCentered([under])
        under_centered.hpack(width, 'exactly')

        return Vlist([
                over_centered,
                Vbox(0., thickness * space),
                under_centered
                ])

    _accent_map = {
        r'hat':            r'\circumflexaccent',
        r'breve':          r'\combiningbreve',
        r'bar':            r'\combiningoverline',
        r'grave':          r'\combininggraveaccent',
        r'acute':          r'\combiningacuteaccent',
        r'tilde':          r'\combiningtilde',
        r'dot':            r'\combiningdotabove',
        r'ddot':           r'\combiningdiaeresis',
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

    # make a lambda and call it to get the namespace right
    _accentprefixed = (lambda am: [
        p for p in tex2uni
        if any(p.startswith(a) and a != p for a in am)
    ])(set(_accent_map))

    def accent(self, s, loc, toks):
        state = self.get_state()
        thickness = state.font_output.get_underline_thickness(
            state.font, state.fontsize, state.dpi)
        (accent, sym), = toks
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
        hlist.function_name, = toks
        return hlist

    def operatorname(self, s, loc, toks):
        self.push_state()
        state = self.get_state()
        state.font = 'rm'
        hlist_list = []
        # Change the font of Chars, but leave Kerns alone
        for c in toks[0]:
            if isinstance(c, Char):
                c.font = 'rm'
                c._update_metrics()
                hlist_list.append(c)
            elif isinstance(c, str):
                hlist_list.append(Char(c, state))
            else:
                hlist_list.append(c)
        next_char_loc = loc + len(toks[0]) + 1
        if isinstance(toks[0], ParseResults):
            next_char_loc += len('operatorname{}')
        next_char = next((c for c in s[next_char_loc:] if c != ' '), '')
        delimiters = self._left_delim | self._ambi_delim | self._right_delim
        delimiters |= {'^', '_'}
        if (next_char not in delimiters and
                toks[0] not in self._overunder_functions):
            # Add thin space except when followed by parenthesis, bracket, etc.
            hlist_list += [self._make_space(self._space_widths[r'\,'])]
        self.pop_state()
        return Hlist(hlist_list)

    def start_group(self, s, loc, toks):
        self.push_state()
        # Deal with LaTeX-style font tokens
        if len(toks):
            self.get_state().font = toks[0][4:]
        return []

    def group(self, s, loc, toks):
        grp = Hlist(toks[0])
        return [grp]
    required_group = simple_group = group

    def end_group(self, s, loc, toks):
        self.pop_state()
        return []

    def font(self, s, loc, toks):
        name, = toks
        self.get_state().font = name
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
        assert len(toks) == 1

        nucleus = None
        sub = None
        super = None

        # Pick all of the apostrophes out, including first apostrophes that
        # have been parsed as characters
        napostrophes = 0
        new_toks = []
        for tok in toks[0]:
            if isinstance(tok, str) and tok not in ('^', '_'):
                napostrophes += len(tok)
            elif isinstance(tok, Char) and tok.c == "'":
                napostrophes += 1
            else:
                new_toks.append(tok)
        toks = new_toks

        if len(toks) == 0:
            assert napostrophes
            nucleus = Hbox(0.0)
        elif len(toks) == 1:
            if not napostrophes:
                return toks[0]  # .asList()
            else:
                nucleus = toks[0]
        elif len(toks) in (2, 3):
            # single subscript or superscript
            nucleus = toks[0] if len(toks) == 3 else Hbox(0.0)
            op, next = toks[-2:]
            if op == '_':
                sub = next
            else:
                super = next
        elif len(toks) in (4, 5):
            # subscript and superscript
            nucleus = toks[0] if len(toks) == 5 else Hbox(0.0)
            op1, next1, op2, next2 = toks[-4:]
            if op1 == op2:
                if op1 == '_':
                    raise ParseFatalException("Double subscript")
                else:
                    raise ParseFatalException("Double superscript")
            if op1 == '_':
                sub = next1
                super = next2
            else:
                super = next1
                sub = next2
        else:
            raise ParseFatalException(
                "Subscript/superscript sequence is too long. "
                "Use braces { } to remove ambiguity.")

        state = self.get_state()
        rule_thickness = state.font_output.get_underline_thickness(
            state.font, state.fontsize, state.dpi)
        xHeight = state.font_output.get_xheight(
            state.font, state.fontsize, state.dpi)

        if napostrophes:
            if super is None:
                super = Hlist([])
            for i in range(napostrophes):
                super.children.extend(self.symbol(s, loc, ['\\prime']))
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
                shift = hlist.height + vgap
            vlist = Vlist(vlist)
            vlist.shift_amount = shift + nucleus.depth
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
        result = Hlist([nucleus, x])

        return [result]

    def _genfrac(self, ldelim, rdelim, rule, style, num, den):
        state = self.get_state()
        thickness = state.font_output.get_underline_thickness(
            state.font, state.fontsize, state.dpi)

        rule = float(rule)

        if style is not self._MathStyle.DISPLAYSTYLE:
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
        metrics = state.font_output.get_metrics(
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

    def genfrac(self, s, loc, toks):
        args, = toks
        return self._genfrac(*args)

    def frac(self, s, loc, toks):
        state = self.get_state()
        thickness = state.font_output.get_underline_thickness(
            state.font, state.fontsize, state.dpi)
        (num, den), = toks
        return self._genfrac('', '', thickness, self._MathStyle.TEXTSTYLE,
                             num, den)

    def dfrac(self, s, loc, toks):
        state = self.get_state()
        thickness = state.font_output.get_underline_thickness(
            state.font, state.fontsize, state.dpi)
        (num, den), = toks
        return self._genfrac('', '', thickness, self._MathStyle.DISPLAYSTYLE,
                             num, den)

    def binom(self, s, loc, toks):
        (num, den), = toks
        return self._genfrac('(', ')', 0.0, self._MathStyle.TEXTSTYLE,
                             num, den)

    def _genset(self, state, annotation, body, overunder):
        thickness = state.font_output.get_underline_thickness(
            state.font, state.fontsize, state.dpi)

        annotation.shrink()

        cannotation = HCentered([annotation])
        cbody = HCentered([body])
        width = max(cannotation.width, cbody.width)
        cannotation.hpack(width, 'exactly')
        cbody.hpack(width, 'exactly')

        vgap = thickness * 3
        if overunder == "under":
            vlist = Vlist([cbody,                       # body
                           Vbox(0, vgap),               # space
                           cannotation                  # annotation
                           ])
            # Shift so the body sits in the same vertical position
            shift_amount = cbody.depth + cannotation.height + vgap

            vlist.shift_amount = shift_amount
        else:
            vlist = Vlist([cannotation,                 # annotation
                           Vbox(0, vgap),               # space
                           cbody                        # body
                           ])

        # To add horizontal gap between symbols: wrap the Vlist into
        # an Hlist and extend it with an Hbox(0, horizontal_gap)
        return vlist

    def sqrt(self, s, loc, toks):
        (root, body), = toks
        state = self.get_state()
        thickness = state.font_output.get_underline_thickness(
            state.font, state.fontsize, state.dpi)

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
        (body,), = toks

        state = self.get_state()
        thickness = state.font_output.get_underline_thickness(
            state.font, state.fontsize, state.dpi)

        height = body.height - body.shift_amount + thickness * 3.0
        depth = body.depth + body.shift_amount

        # Place overline above body
        rightside = Vlist([Hrule(state), Glue('fill'), Hlist([body])])

        # Stretch the glue between the hrule and the body
        rightside.vpack(height + (state.fontsize * state.dpi) / (100.0 * 12.0),
                        'exactly', depth)

        hlist = Hlist([rightside])
        return [hlist]

    def overset(self, s, loc, toks):
        assert len(toks) == 1
        assert len(toks[0]) == 2

        state = self.get_state()
        annotation, body = toks[0]

        return self._genset(state, annotation, body, overunder="over")

    def underset(self, s, loc, toks):
        assert len(toks) == 1
        assert len(toks[0]) == 2

        state = self.get_state()
        annotation, body = toks[0]

        return self._genset(state, annotation, body, overunder="under")

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
        front, middle, back = toks

        return self._auto_sized_delimiter(front, middle.asList(), back)
