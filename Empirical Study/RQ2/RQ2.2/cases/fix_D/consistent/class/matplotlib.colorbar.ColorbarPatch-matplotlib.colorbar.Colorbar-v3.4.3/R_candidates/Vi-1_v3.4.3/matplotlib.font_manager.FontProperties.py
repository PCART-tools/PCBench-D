class FontProperties:
    """
    A class for storing and manipulating font properties.

    The font properties are the six properties described in the
    `W3C Cascading Style Sheet, Level 1
    <http://www.w3.org/TR/1998/REC-CSS2-19980512/>`_ font
    specification and *math_fontfamily* for math fonts:

    - family: A list of font names in decreasing order of priority.
      The items may include a generic font family name, either
      'sans-serif' (default), 'serif', 'cursive', 'fantasy', or 'monospace'.
      In that case, the actual font to be used will be looked up
      from the associated rcParam.

    - style: Either 'normal' (default), 'italic' or 'oblique'.

    - variant: Either 'normal' (default) or 'small-caps'.

    - stretch: A numeric value in the range 0-1000 or one of
      'ultra-condensed', 'extra-condensed', 'condensed',
      'semi-condensed', 'normal' (default), 'semi-expanded', 'expanded',
      'extra-expanded' or 'ultra-expanded'.

    - weight: A numeric value in the range 0-1000 or one of
      'ultralight', 'light', 'normal' (default), 'regular', 'book', 'medium',
      'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy',
      'extra bold', 'black'.

    - size: Either an relative value of 'xx-small', 'x-small',
      'small', 'medium', 'large', 'x-large', 'xx-large' or an
      absolute font size, e.g., 10 (default).

    - math_fontfamily: The family of fonts used to render math text; overrides
      :rc:`mathtext.fontset`. Supported values are the same as the ones
      supported by :rc:`mathtext.fontset`: 'dejavusans', 'dejavuserif', 'cm',
      'stix', 'stixsans' and 'custom'.

    Alternatively, a font may be specified using the absolute path to a font
    file, by using the *fname* kwarg.  However, in this case, it is typically
    simpler to just pass the path (as a `pathlib.Path`, not a `str`) to the
    *font* kwarg of the `.Text` object.

    The preferred usage of font sizes is to use the relative values,
    e.g.,  'large', instead of absolute font sizes, e.g., 12.  This
    approach allows all text sizes to be made larger or smaller based
    on the font manager's default font size.

    This class will also accept a fontconfig_ pattern_, if it is the only
    argument provided.  This support does not depend on fontconfig; we are
    merely borrowing its pattern syntax for use here.

    .. _fontconfig: https://www.freedesktop.org/wiki/Software/fontconfig/
    .. _pattern:
       https://www.freedesktop.org/software/fontconfig/fontconfig-user.html

    Note that Matplotlib's internal font manager and fontconfig use a
    different algorithm to lookup fonts, so the results of the same pattern
    may be different in Matplotlib than in other applications that use
    fontconfig.
    """

    def __init__(self,
                 family = None,
                 style  = None,
                 variant= None,
                 weight = None,
                 stretch= None,
                 size   = None,
                 fname  = None,  # if set, it's a hardcoded filename to use
                 math_fontfamily = None,
                 ):
        self._family = _normalize_font_family(rcParams['font.family'])
        self._slant = rcParams['font.style']
        self._variant = rcParams['font.variant']
        self._weight = rcParams['font.weight']
        self._stretch = rcParams['font.stretch']
        self._size = rcParams['font.size']
        self._file = None
        self._math_fontfamily = None

        if isinstance(family, str):
            # Treat family as a fontconfig pattern if it is the only
            # parameter provided.
            if (style is None and variant is None and weight is None and
                    stretch is None and size is None and fname is None):
                self.set_fontconfig_pattern(family)
                return

        self.set_family(family)
        self.set_style(style)
        self.set_variant(variant)
        self.set_weight(weight)
        self.set_stretch(stretch)
        self.set_file(fname)
        self.set_size(size)
        self.set_math_fontfamily(math_fontfamily)

    @classmethod
    def _from_any(cls, arg):
        """
        Generic constructor which can build a `.FontProperties` from any of the
        following:

        - a `.FontProperties`: it is passed through as is;
        - `None`: a `.FontProperties` using rc values is used;
        - an `os.PathLike`: it is used as path to the font file;
        - a `str`: it is parsed as a fontconfig pattern;
        - a `dict`: it is passed as ``**kwargs`` to `.FontProperties`.
        """
        if isinstance(arg, cls):
            return arg
        elif arg is None:
            return cls()
        elif isinstance(arg, os.PathLike):
            return cls(fname=arg)
        elif isinstance(arg, str):
            return cls(arg)
        else:
            return cls(**arg)

    def __hash__(self):
        l = (tuple(self.get_family()),
             self.get_slant(),
             self.get_variant(),
             self.get_weight(),
             self.get_stretch(),
             self.get_size_in_points(),
             self.get_file(),
             self.get_math_fontfamily())
        return hash(l)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        return self.get_fontconfig_pattern()

    def get_family(self):
        """
        Return a list of font names that comprise the font family.
        """
        return self._family

    def get_name(self):
        """
        Return the name of the font that best matches the font properties.
        """
        return get_font(findfont(self)).family_name

    def get_style(self):
        """
        Return the font style.  Values are: 'normal', 'italic' or 'oblique'.
        """
        return self._slant
    get_slant = get_style

    def get_variant(self):
        """
        Return the font variant.  Values are: 'normal' or 'small-caps'.
        """
        return self._variant

    def get_weight(self):
        """
        Set the font weight.  Options are: A numeric value in the
        range 0-1000 or one of 'light', 'normal', 'regular', 'book',
        'medium', 'roman', 'semibold', 'demibold', 'demi', 'bold',
        'heavy', 'extra bold', 'black'
        """
        return self._weight

    def get_stretch(self):
        """
        Return the font stretch or width.  Options are: 'ultra-condensed',
        'extra-condensed', 'condensed', 'semi-condensed', 'normal',
        'semi-expanded', 'expanded', 'extra-expanded', 'ultra-expanded'.
        """
        return self._stretch

    def get_size(self):
        """
        Return the font size.
        """
        return self._size

    def get_size_in_points(self):
        return self._size

    def get_file(self):
        """
        Return the filename of the associated font.
        """
        return self._file

    def get_fontconfig_pattern(self):
        """
        Get a fontconfig_ pattern_ suitable for looking up the font as
        specified with fontconfig's ``fc-match`` utility.

        This support does not depend on fontconfig; we are merely borrowing its
        pattern syntax for use here.
        """
        return generate_fontconfig_pattern(self)

    def set_family(self, family):
        """
        Change the font family.  May be either an alias (generic name
        is CSS parlance), such as: 'serif', 'sans-serif', 'cursive',
        'fantasy', or 'monospace', a real font name or a list of real
        font names.  Real font names are not supported when
        :rc:`text.usetex` is `True`.
        """
        if family is None:
            family = rcParams['font.family']
        self._family = _normalize_font_family(family)
    set_name = set_family

    def set_style(self, style):
        """
        Set the font style.  Values are: 'normal', 'italic' or 'oblique'.
        """
        if style is None:
            style = rcParams['font.style']
        _api.check_in_list(['normal', 'italic', 'oblique'], style=style)
        self._slant = style
    set_slant = set_style

    def set_variant(self, variant):
        """
        Set the font variant.  Values are: 'normal' or 'small-caps'.
        """
        if variant is None:
            variant = rcParams['font.variant']
        _api.check_in_list(['normal', 'small-caps'], variant=variant)
        self._variant = variant

    def set_weight(self, weight):
        """
        Set the font weight.  May be either a numeric value in the
        range 0-1000 or one of 'ultralight', 'light', 'normal',
        'regular', 'book', 'medium', 'roman', 'semibold', 'demibold',
        'demi', 'bold', 'heavy', 'extra bold', 'black'
        """
        if weight is None:
            weight = rcParams['font.weight']
        try:
            weight = int(weight)
            if weight < 0 or weight > 1000:
                raise ValueError()
        except ValueError:
            if weight not in weight_dict:
                raise ValueError("weight is invalid")
        self._weight = weight

    def set_stretch(self, stretch):
        """
        Set the font stretch or width.  Options are: 'ultra-condensed',
        'extra-condensed', 'condensed', 'semi-condensed', 'normal',
        'semi-expanded', 'expanded', 'extra-expanded' or
        'ultra-expanded', or a numeric value in the range 0-1000.
        """
        if stretch is None:
            stretch = rcParams['font.stretch']
        try:
            stretch = int(stretch)
            if stretch < 0 or stretch > 1000:
                raise ValueError()
        except ValueError as err:
            if stretch not in stretch_dict:
                raise ValueError("stretch is invalid") from err
        self._stretch = stretch

    def set_size(self, size):
        """
        Set the font size.  Either an relative value of 'xx-small',
        'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'
        or an absolute font size, e.g., 12.
        """
        if size is None:
            size = rcParams['font.size']
        try:
            size = float(size)
        except ValueError:
            try:
                scale = font_scalings[size]
            except KeyError as err:
                raise ValueError(
                    "Size is invalid. Valid font size are "
                    + ", ".join(map(str, font_scalings))) from err
            else:
                size = scale * FontManager.get_default_size()
        if size < 1.0:
            _log.info('Fontsize %1.2f < 1.0 pt not allowed by FreeType. '
                      'Setting fontsize = 1 pt', size)
            size = 1.0
        self._size = size

    def set_file(self, file):
        """
        Set the filename of the fontfile to use.  In this case, all
        other properties will be ignored.
        """
        self._file = os.fspath(file) if file is not None else None

    def set_fontconfig_pattern(self, pattern):
        """
        Set the properties by parsing a fontconfig_ *pattern*.

        This support does not depend on fontconfig; we are merely borrowing its
        pattern syntax for use here.
        """
        for key, val in parse_fontconfig_pattern(pattern).items():
            if type(val) == list:
                getattr(self, "set_" + key)(val[0])
            else:
                getattr(self, "set_" + key)(val)

    def get_math_fontfamily(self):
        """
        Return the name of the font family used for math text.

        The default font is :rc:`mathtext.fontset`.
        """
        return self._math_fontfamily

    def set_math_fontfamily(self, fontfamily):
        """
        Set the font family for text in math mode.

        If not set explicitly, :rc:`mathtext.fontset` will be used.

        Parameters
        ----------
        fontfamily : str
            The name of the font family.

            Available font families are defined in the
            matplotlibrc.template file
            :ref:`here <customizing-with-matplotlibrc-files>`

        See Also
        --------
        .text.Text.get_math_fontfamily
        """
        if fontfamily is None:
            fontfamily = rcParams['mathtext.fontset']
        else:
            valid_fonts = _validators['mathtext.fontset'].valid.values()
            # _check_in_list() Validates the parameter math_fontfamily as
            # if it were passed to rcParams['mathtext.fontset']
            _api.check_in_list(valid_fonts, math_fontfamily=fontfamily)
        self._math_fontfamily = fontfamily

    def copy(self):
        """Return a copy of self."""
        new = type(self)()
        vars(new).update(vars(self))
        return new
