    def _write_cell(self, s, kind='td', indent=0, tags=None):
        if tags is not None:
            start_tag = '<%s %s>' % (kind, tags)
        else:
            start_tag = '<%s>' % kind

        if self.escape:
            # escape & first to prevent double escaping of &
            esc = OrderedDict(
                [('&', r'&amp;'), ('<', r'&lt;'), ('>', r'&gt;')]
            )
        else:
            esc = {}
        rs = com.pprint_thing(s, escape_chars=esc).strip()
        self.write(
            '%s%s</%s>' % (start_tag, rs, kind), indent)
