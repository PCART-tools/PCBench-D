  def _error_message(self):
    exc_info = sys.exc_info()[:2]
    msg = traceback.format_exception_only(*exc_info)[-1].strip()
    print('***', msg, file=self.stdout)
