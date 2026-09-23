    def __init__(self):

        family = Regex(
            r'([^%s]|(\\[%s]))*' % (family_punc, family_punc)
        ).setParseAction(self._family)

        size = Regex(
            r"([0-9]+\.?[0-9]*|\.[0-9]+)"
        ).setParseAction(self._size)

        name = Regex(
            r'[a-z]+'
        ).setParseAction(self._name)

        value = Regex(
            r'([^%s]|(\\[%s]))*' % (value_punc, value_punc)
        ).setParseAction(self._value)

        families = (
            family
            + ZeroOrMore(
                Literal(',')
                + family)
        ).setParseAction(self._families)

        point_sizes = (
            size
            + ZeroOrMore(
                Literal(',')
                + size)
        ).setParseAction(self._point_sizes)

        property = (
            (name
             + Suppress(Literal('='))
             + value
             + ZeroOrMore(
                 Suppress(Literal(','))
                 + value))
            | name
        ).setParseAction(self._property)

        pattern = (
            Optional(
                families)
            + Optional(
                Literal('-')
                + point_sizes)
            + ZeroOrMore(
                Literal(':')
                + property)
            + StringEnd()
        )

        self._parser = pattern
        self.ParseException = ParseException
