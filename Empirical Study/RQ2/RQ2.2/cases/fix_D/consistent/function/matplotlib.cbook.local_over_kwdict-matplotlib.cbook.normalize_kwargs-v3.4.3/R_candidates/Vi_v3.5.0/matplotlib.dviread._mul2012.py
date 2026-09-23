def _mul2012(num1, num2):
    """Multiply two numbers in 20.12 fixed point format."""
    # Separated into a function because >> has surprising precedence
    return (num1*num2) >> 20
