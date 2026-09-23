  def __str__(self):
    return '\n'.join(f'at mapped index {", ".join(map(str, idx))}: {e}'
                     for idx, e in self.error_mapping.items())
