  def run(self):
    while True:
      try:
        self.cmdloop()
        break
      except KeyboardInterrupt:
        print('--KeyboardInterrupt--', file=sys.stdout)
