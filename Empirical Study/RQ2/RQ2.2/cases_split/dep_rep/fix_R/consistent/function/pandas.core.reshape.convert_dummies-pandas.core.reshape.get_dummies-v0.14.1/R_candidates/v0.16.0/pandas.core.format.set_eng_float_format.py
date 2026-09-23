def set_eng_float_format(accuracy=3, use_eng_prefix=False):
    """
    Alter default behavior on how float is formatted in DataFrame.
    Format float in engineering format. By accuracy, we mean the number of
    decimal digits after the floating point.

    See also EngFormatter.
    """

    set_option("display.float_format", EngFormatter(accuracy, use_eng_prefix))
    set_option("display.column_space", max(12, accuracy + 9))
