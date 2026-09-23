  def __init__(self, *args, user_repr, **kwargs):
    super().__init__(*args, **kwargs)
    self.user_repr = user_repr
