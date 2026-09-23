def MainOpFunctionThatThrowsCustomErrorInBuilder(inputs, _):
    raise CustomError("This is an intentional exception in builder.")
