  def render(self):
    self.update_code(
        self._code, self._highlights, linenostart=self._linenostart)
