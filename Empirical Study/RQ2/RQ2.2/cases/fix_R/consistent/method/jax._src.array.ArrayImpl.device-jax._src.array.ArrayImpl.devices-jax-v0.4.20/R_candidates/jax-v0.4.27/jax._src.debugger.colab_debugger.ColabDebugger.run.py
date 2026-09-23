  def run(self):
    self._debugger_view.render()
    while True:
      if not self.cmdloop():
        return
