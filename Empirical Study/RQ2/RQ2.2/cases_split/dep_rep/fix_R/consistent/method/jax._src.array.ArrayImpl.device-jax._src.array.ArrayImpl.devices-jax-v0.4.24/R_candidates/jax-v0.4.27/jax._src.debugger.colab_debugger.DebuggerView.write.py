  def write(self, text):
    self._interaction_log.append(colab_lib.pre(text))
