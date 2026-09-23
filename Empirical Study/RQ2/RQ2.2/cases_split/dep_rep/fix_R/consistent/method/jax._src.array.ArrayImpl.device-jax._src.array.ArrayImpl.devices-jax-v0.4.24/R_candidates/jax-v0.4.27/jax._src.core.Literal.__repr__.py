  def __repr__(self):
    if hasattr(self, 'hash'):
      return f'{self.val}'
    else:
      return f'Literal(val={self.val})'
