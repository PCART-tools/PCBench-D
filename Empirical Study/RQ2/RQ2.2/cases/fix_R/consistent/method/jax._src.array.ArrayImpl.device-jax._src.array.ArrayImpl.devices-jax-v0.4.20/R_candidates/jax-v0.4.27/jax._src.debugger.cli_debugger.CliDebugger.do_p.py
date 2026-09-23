  def do_p(self, arg):
    """p expression
    Evaluates and prints the value of an expression
    """
    try:
      print(repr(self.evaluate(arg)), file=self.stdout)
    except:
      self._error_message()
