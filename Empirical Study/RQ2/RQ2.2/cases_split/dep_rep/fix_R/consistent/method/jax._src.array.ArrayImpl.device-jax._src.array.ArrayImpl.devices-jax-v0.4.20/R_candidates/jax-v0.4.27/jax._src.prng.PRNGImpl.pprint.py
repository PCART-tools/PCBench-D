  def pprint(self):
    ty = self.__class__.__name__
    return (pp.text(f"{ty} [{self.tag}] {{{self.name}}}:") +
            pp.nest(2, pp.group(pp.brk() + pp.join(pp.brk(), [
              pp.text(f"{k} = {v}") for k, v in self._asdict().items()
            ]))))
