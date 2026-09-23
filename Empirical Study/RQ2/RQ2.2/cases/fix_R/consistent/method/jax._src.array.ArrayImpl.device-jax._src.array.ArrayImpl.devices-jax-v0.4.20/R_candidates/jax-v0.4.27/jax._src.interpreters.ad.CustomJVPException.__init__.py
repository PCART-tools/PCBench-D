  def __init__(self):
    # TODO(mattjj): track source provenance on AD tracers, improve error
    msg = ("Detected differentiation of a custom_jvp function with respect to "
           "a closed-over value. That isn't supported because the custom JVP "
           "rule only specifies how to differentiate the custom_jvp function "
           "with respect to explicit input parameters. Try passing the "
           "closed-over value into the custom_jvp function as an argument, and "
           "adapting the custom_jvp rule.")
    super().__init__(msg)
