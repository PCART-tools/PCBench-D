class SimplifiedTraceback(Exception):
  def __str__(self):
    return _simplified_tb_msg
