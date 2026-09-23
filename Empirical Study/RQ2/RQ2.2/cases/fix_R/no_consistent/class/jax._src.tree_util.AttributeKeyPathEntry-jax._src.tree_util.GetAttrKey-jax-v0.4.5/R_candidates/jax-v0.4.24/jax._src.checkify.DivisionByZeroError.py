class DivisionByZeroError(JaxException):

  def __str__(self):
    return 'division by zero'

  def get_effect_type(self):
    return ErrorEffect(DivisionByZeroError, ())
