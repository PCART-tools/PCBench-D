  def default(self, arg):
    """Evaluates an expression."""
    try:
      print(repr(self.evaluate(arg)), file=self.stdout)
    except:
      self._error_message()
