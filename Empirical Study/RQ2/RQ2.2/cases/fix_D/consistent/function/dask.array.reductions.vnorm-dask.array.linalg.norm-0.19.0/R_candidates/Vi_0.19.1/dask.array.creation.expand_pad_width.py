def expand_pad_width(array, pad_width):
    if isinstance(pad_width, Integral):
        pad_width = array.ndim * ((pad_width, pad_width),)
    elif (isinstance(pad_width, Sequence) and
          all(isinstance(pw, Integral) for pw in pad_width) and
          len(pad_width) == 1):
        pad_width = array.ndim * ((pad_width[0], pad_width[0]),)
    elif (isinstance(pad_width, Sequence) and
          len(pad_width) == 2 and
          all(isinstance(pw, Integral) for pw in pad_width)):
            pad_width = tuple(
                (pad_width[0], pad_width[1]) for _ in range(array.ndim)
            )
    elif (isinstance(pad_width, Sequence) and
          len(pad_width) == array.ndim and
          all(isinstance(pw, Sequence) for pw in pad_width) and
          all((len(pw) == 2) for pw in pad_width) and
          all(all(isinstance(w, Integral) for w in pw) for pw in pad_width)):
            pad_width = tuple((pw[0], pw[1]) for pw in pad_width)
    else:
        raise TypeError(
            "`pad_width` must be composed of integral typed values."
        )

    return pad_width
