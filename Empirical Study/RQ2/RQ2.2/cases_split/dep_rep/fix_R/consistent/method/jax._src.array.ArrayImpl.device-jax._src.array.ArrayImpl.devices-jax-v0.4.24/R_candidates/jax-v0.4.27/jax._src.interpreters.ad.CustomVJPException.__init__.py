  def __init__(self):
    # TODO(mattjj): track source provenance on AD tracers, improve error
    msg = ("Detected differentiation of a custom_vjp function with respect to "
           "a closed-over value. That isn't supported because the custom VJP "
           "rule only specifies how to differentiate the custom_vjp function "
           "with respect to explicit input parameters. Try passing the "
           "closed-over value into the custom_vjp function as an argument, and "
           "adapting the custom_vjp fwd and bwd rules.")
    super().__init__(msg)
