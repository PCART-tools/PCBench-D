  def pprint(self):
    pp_keys = pp.text('shape = ') + pp.text(str(self.shape))
    pp_impl = pp.text('impl = ') + self._impl.pprint()
    return str(pp.group(
      pp.text('PRNGKeyArray:') +
      pp.nest(2, pp.brk() + pp_keys + pp.brk() + pp_impl)))
