  def do_pp(self, arg):
    """pp expression
    Evaluates and pretty-prints the value of an expression
    """
    try:
      print(pprint.pformat(self.evaluate(arg)), file=self.stdout)
    except:
      self._error_message()
