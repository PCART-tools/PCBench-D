    def __init__(self) -> None:
        p = types.SimpleNamespace()

        def set_names_and_parse_actions() -> None:
            for key, val in vars(p).items():
                if not key.startswith('_'):
                    # Set names on (almost) everything -- very useful for debugging
                    # token, placeable, and auto_delim are forward references which
                    # are left without names to ensure useful error messages
                    if key not in ("token", "placeable", "auto_delim"):
                        val.setName(key)
                    # Set actions
                    if hasattr(self, key):
                        val.setParseAction(getattr(self, key))

        # Root definitions.

        # In TeX parlance, a csname is a control sequence name (a "\foo").
        def csnames(group: str, names: Iterable[str]) -> Regex:
            ends_with_alpha = []
            ends_with_nonalpha = []
            for name in names:
                if name[-1].isalpha():
                    ends_with_alpha.append(name)
                else:
                    ends_with_nonalpha.append(name)
            return Regex(
                r"\\(?P<{group}>(?:{alpha})(?![A-Za-z]){additional}{nonalpha})".format(
                    group=group,
                    alpha="|".join(map(re.escape, ends_with_alpha)),
                    additional="|" if ends_with_nonalpha else "",
                    nonalpha="|".join(map(re.escape, ends_with_nonalpha)),
                )
            )

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
        p.unknown_symbol = Regex(r"\\[A-Za-z]+")("name")

        p.font           = csnames("font", self._fontnames)
        p.start_group    = Optional(r"\math" + oneOf(self._fontnames)("font")) + "{"
        p.end_group      = Literal("}")

        p.delim          = oneOf(self._delims)

        # Mutually recursive definitions.  (Minimizing the number of Forward
        # elements is important for speed.)
        p.auto_delim       = Forward()
        p.placeable        = Forward()
        p.named_placeable  = Forward()
        p.required_group   = Forward()
        p.optional_group   = Forward()
        p.token            = Forward()

        # Workaround for placable being part of a cycle of definitions
        # calling `p.placeable("name")` results in a copy, so not guaranteed
        # to get the definition added after it is used.
        # ref https://github.com/matplotlib/matplotlib/issues/25204
        # xref https://github.com/pyparsing/pyparsing/issues/95
        p.named_placeable <<= p.placeable

        set_names_and_parse_actions()  # for mutually recursive definitions.

        p.optional_group <<= "{" + ZeroOrMore(p.token)("group") + "}"
        p.required_group <<= "{" + OneOrMore(p.token)("group") + "}"

        p.customspace = cmd(r"\hspace", "{" + p.float_literal("space") + "}")

        p.accent = (
            csnames("accent", [*self._accent_map, *self._wide_accents])
            - p.named_placeable("sym"))

        p.function = csnames("name", self._function_names)

        p.group = p.start_group + ZeroOrMore(p.token)("group") + p.end_group
        p.unclosed_group = (p.start_group + ZeroOrMore(p.token)("group") + StringEnd())

        p.frac  = cmd(r"\frac", p.required_group("num") + p.required_group("den"))
        p.dfrac = cmd(r"\dfrac", p.required_group("num") + p.required_group("den"))
        p.binom = cmd(r"\binom", p.required_group("num") + p.required_group("den"))

        p.genfrac = cmd(
            r"\genfrac",
            "{" + Optional(p.delim)("ldelim") + "}"
            + "{" + Optional(p.delim)("rdelim") + "}"
            + "{" + p.float_literal("rulesize") + "}"
            + "{" + Optional(p.style_literal)("style") + "}"
            + p.required_group("num")
            + p.required_group("den"))

        p.sqrt = cmd(
            r"\sqrt{value}",
            Optional("[" + OneOrMore(NotAny("]") + p.token)("root") + "]")
            + p.required_group("value"))

        p.overline = cmd(r"\overline", p.required_group("body"))

        p.overset  = cmd(
            r"\overset",
            p.optional_group("annotation") + p.optional_group("body"))
        p.underset = cmd(
            r"\underset",
            p.optional_group("annotation") + p.optional_group("body"))

        p.text = cmd(r"\text", QuotedString('{', '\\', endQuoteChar="}"))

        p.substack = cmd(r"\substack",
                           nested_expr(opener="{", closer="}",
                                       content=Group(OneOrMore(p.token)) +
                                       ZeroOrMore(Literal("\\\\").suppress()))("parts"))

        p.subsuper = (
            (Optional(p.placeable)("nucleus")
             + OneOrMore(oneOf(["_", "^"]) - p.placeable)("subsuper")
             + Regex("'*")("apostrophes"))
            | Regex("'+")("apostrophes")
            | (p.named_placeable("nucleus") + Regex("'*")("apostrophes"))
        )

        p.simple = p.space | p.customspace | p.font | p.subsuper

        p.token <<= (
            p.simple
            | p.auto_delim
            | p.unclosed_group
            | p.unknown_symbol  # Must be last
        )

        p.operatorname = cmd(r"\operatorname", "{" + ZeroOrMore(p.simple)("name") + "}")

        p.boldsymbol = cmd(
            r"\boldsymbol", "{" + ZeroOrMore(p.simple)("value") + "}")

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
            | p.text
            | p.boldsymbol
            | p.substack
        )

        mdelim = r"\middle" - (p.delim("mdelim") | Error("Expected a delimiter"))
        p.auto_delim    <<= (
            r"\left" - (p.delim("left") | Error("Expected a delimiter"))
            + ZeroOrMore(p.simple | p.auto_delim | mdelim)("mid")
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
