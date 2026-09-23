    def __repr__(self):
        tpl = textwrap.dedent(
            """\
        {cls}({data},
        {lead}closed='{closed}',
        {lead}dtype='{dtype}')"""
        )
        return tpl.format(
            cls=self.__class__.__name__,
            data=self._format_data(),
            lead=" " * len(self.__class__.__name__) + " ",
            closed=self.closed,
            dtype=self.dtype,
        )
