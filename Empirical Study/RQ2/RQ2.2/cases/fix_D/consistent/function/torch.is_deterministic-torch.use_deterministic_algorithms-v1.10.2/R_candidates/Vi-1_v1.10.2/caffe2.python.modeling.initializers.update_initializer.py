def update_initializer(initializer_class,
                       operator_name_and_kwargs,
                       default_operator_name_and_kwargs):
    '''
    A helper function to convert from operator_name_and_kwargs to new
    object of type initializer_class. This function serves two purposes:

    1. Support for custom initialization operators being passed in
    2. Allow user to specify a custom Initializer without overwriting
       default operators used for initialization

    If initializer_class is None, creates a default initializer using
    the Initializer class and operator_name_and_kwargs provided

    If operator_name_and_kwargs is None, uses default_operator_name_and_kwargs

    returns an instantiated Initializer object
    '''
    def get_initializer_args():
        return (
            operator_name_and_kwargs or
            default_operator_name_and_kwargs
        )

    if initializer_class is not None:
        init = initializer_class(get_initializer_args()[0],
                                 **get_initializer_args()[1])
    else:
        init = Initializer(
            get_initializer_args()[0],
            **get_initializer_args()[1]
        )
    return init
