  def __init__(self, *args, name_stack: source_info_util.NameStack):
    super().__init__(*args)
    self.name_stack = name_stack
