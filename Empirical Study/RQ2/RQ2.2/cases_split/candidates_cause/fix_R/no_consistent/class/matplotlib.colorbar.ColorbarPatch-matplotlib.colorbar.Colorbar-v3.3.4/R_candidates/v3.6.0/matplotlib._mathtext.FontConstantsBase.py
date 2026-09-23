class FontConstantsBase:
    """
    A set of constants that controls how certain things, such as sub-
    and superscripts are laid out.  These are all metrics that can't
    be reliably retrieved from the font metrics in the font itself.
    """
    # Percentage of x-height of additional horiz. space after sub/superscripts
    script_space = 0.05

    # Percentage of x-height that sub/superscripts drop below the baseline
    subdrop = 0.4

    # Percentage of x-height that superscripts are raised from the baseline
    sup1 = 0.7

    # Percentage of x-height that subscripts drop below the baseline
    sub1 = 0.3

    # Percentage of x-height that subscripts drop below the baseline when a
    # superscript is present
    sub2 = 0.5

    # Percentage of x-height that sub/superscripts are offset relative to the
    # nucleus edge for non-slanted nuclei
    delta = 0.025

    # Additional percentage of last character height above 2/3 of the
    # x-height that superscripts are offset relative to the subscript
    # for slanted nuclei
    delta_slanted = 0.2

    # Percentage of x-height that superscripts and subscripts are offset for
    # integrals
    delta_integral = 0.1
