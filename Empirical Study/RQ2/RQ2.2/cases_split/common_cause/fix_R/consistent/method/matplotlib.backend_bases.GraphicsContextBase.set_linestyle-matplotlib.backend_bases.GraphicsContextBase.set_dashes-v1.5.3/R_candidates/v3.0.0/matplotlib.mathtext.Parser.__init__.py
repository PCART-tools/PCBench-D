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
        p.placeable        = Forward()
        p.rbrace           = Forward()
        p.rbracket         = Forward()
        p.required_group   = Forward()
        p.right_delim      = Forward()
        p.right_delim_safe = Forward()
        p.simple           = Forward()
        p.simple_group     = Forward()
        p.single_symbol    = Forward()
        p.snowflake        = Forward()
        p.space            = Forward()
        p.sqrt             = Forward()
        p.stackrel         = Forward()
        p.start_group      = Forward()
        p.subsuper         = Forward()
        p.subsuperop       = Forward()
        p.symbol           = Forward()
        p.symbol_name      = Forward()
        p.token            = Forward()
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
        p.customspace   <<= (Suppress(Literal(r'\hspace'))
                          - ((p.lbrace + p.float_literal + p.rbrace)
                            | Error(r"Expected \hspace{n}")))

        unicode_range =  "\U00000080-\U0001ffff"
        p.single_symbol <<= Regex(r"([a-zA-Z0-9 +\-*/<>=:,.;!\?&'@()\[\]|%s])|(\\[%%${}\[\]_|])" %
                               unicode_range)
        p.snowflake     <<= Suppress(p.bslash) + oneOf(self._snowflake)
        p.symbol_name   <<= (Combine(p.bslash + oneOf(list(tex2uni))) +
                          FollowedBy(Regex("[^A-Za-z]").leaveWhitespace() | StringEnd()))
        p.symbol        <<= (p.single_symbol | p.symbol_name).leaveWhitespace()

        p.apostrophe    <<= Regex("'+")

        p.c_over_c      <<= Suppress(p.bslash) + oneOf(list(self._char_over_chars))

        p.accent        <<= Group(
                             Suppress(p.bslash)
                           + oneOf([*self._accent_map, *self._wide_accents])
                           - p.placeable
                         )

        p.function      <<= Suppress(p.bslash) + oneOf(list(self._function_names))

        p.start_group   <<= Optional(p.latexfont) + p.lbrace
        p.end_group     <<= p.rbrace.copy()
        p.simple_group  <<= Group(p.lbrace + ZeroOrMore(p.token) + p.rbrace)
        p.required_group<<= Group(p.lbrace + OneOrMore(p.token) + p.rbrace)
        p.group         <<= Group(p.start_group + ZeroOrMore(p.token) + p.end_group)

        p.font          <<= Suppress(p.bslash) + oneOf(list(self._fontnames))
        p.latexfont     <<= Suppress(p.bslash) + oneOf(['math' + x for x in self._fontnames])

        p.frac          <<= Group(
                             Suppress(Literal(r"\frac"))
                           - ((p.required_group + p.required_group) | Error(r"Expected \frac{num}{den}"))
                         )

        p.dfrac         <<= Group(
                             Suppress(Literal(r"\dfrac"))
                           - ((p.required_group + p.required_group) | Error(r"Expected \dfrac{num}{den}"))
                         )

        p.stackrel      <<= Group(
                             Suppress(Literal(r"\stackrel"))
                           - ((p.required_group + p.required_group) | Error(r"Expected \stackrel{num}{den}"))
                         )

        p.binom         <<= Group(
                             Suppress(Literal(r"\binom"))
                           - ((p.required_group + p.required_group) | Error(r"Expected \binom{num}{den}"))
                         )

        p.ambi_delim    <<= oneOf(list(self._ambi_delim))
        p.left_delim    <<= oneOf(list(self._left_delim))
        p.right_delim   <<= oneOf(list(self._right_delim))
        p.right_delim_safe <<= oneOf([*(self._right_delim - {'}'}), r'\}'])

        p.genfrac       <<= Group(
                             Suppress(Literal(r"\genfrac"))
                           - (((p.lbrace + Optional(p.ambi_delim | p.left_delim, default='') + p.rbrace)
                           +   (p.lbrace + Optional(p.ambi_delim | p.right_delim_safe, default='') + p.rbrace)
                           +   (p.lbrace + p.float_literal + p.rbrace)
                           +   p.simple_group + p.required_group + p.required_group)
                           | Error(r"Expected \genfrac{ldelim}{rdelim}{rulesize}{style}{num}{den}"))
                         )

        p.sqrt          <<= Group(
                             Suppress(Literal(r"\sqrt"))
                           - ((Optional(p.lbracket + p.int_literal + p.rbracket, default=None)
                              + p.required_group)
                           | Error("Expected \\sqrt{value}"))
                         )

        p.overline      <<= Group(
                             Suppress(Literal(r"\overline"))
                           - (p.required_group | Error("Expected \\overline{value}"))
                         )

        p.unknown_symbol<<= Combine(p.bslash + Regex("[A-Za-z]*"))

        p.operatorname  <<= Group(
                             Suppress(Literal(r"\operatorname"))
                           - ((p.lbrace + ZeroOrMore(p.simple | p.unknown_symbol) + p.rbrace)
                              | Error("Expected \\operatorname{value}"))
                         )

        p.placeable     <<= ( p.snowflake # this needs to be before accent so named symbols
                                          # that are prefixed with an accent name work
                         | p.accent # Must be before symbol as all accents are symbols
                         | p.symbol # Must be third to catch all named symbols and single chars not in a group
                         | p.c_over_c
                         | p.function
                         | p.group
                         | p.frac
                         | p.dfrac
                         | p.stackrel
                         | p.binom
                         | p.genfrac
                         | p.sqrt
                         | p.overline
                         | p.operatorname
                         )

        p.simple        <<= ( p.space
                         | p.customspace
                         | p.font
                         | p.subsuper
                         )

        p.subsuperop    <<= oneOf(["_", "^"])

        p.subsuper      <<= Group(
                             (Optional(p.placeable) + OneOrMore(p.subsuperop - p.placeable) + Optional(p.apostrophe))
                           | (p.placeable + Optional(p.apostrophe))
                           | p.apostrophe
                         )

        p.token         <<= ( p.simple
                         | p.auto_delim
                         | p.unknown_symbol # Must be last
                         )

        p.auto_delim    <<= (Suppress(Literal(r"\left"))
                          - ((p.left_delim | p.ambi_delim) | Error("Expected a delimiter"))
                          + Group(ZeroOrMore(p.simple | p.auto_delim))
                          + Suppress(Literal(r"\right"))
                          - ((p.right_delim | p.ambi_delim) | Error("Expected a delimiter"))
                         )

        p.math          <<= OneOrMore(p.token)

        p.math_string   <<= QuotedString('$', '\\', unquoteResults=False)

        p.non_math      <<= Regex(r"(?:(?:\\[$])|[^$])*").leaveWhitespace()

        p.main          <<= (p.non_math + ZeroOrMore(p.math_string + p.non_math)) + StringEnd()

        # Set actions
        for key, val in vars(p).items():
            if not key.startswith('_'):
                if hasattr(self, key):
                    val.setParseAction(getattr(self, key))

        self._expression = p.main
        self._math_expression = p.math
