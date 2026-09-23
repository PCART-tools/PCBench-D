def colormaps():
    """
    Matplotlib provides a number of colormaps, and others can be added using
    :func:`~matplotlib.cm.register_cmap`.  This function documents the built-in
    colormaps, and will also return a list of all registered colormaps if
    called.

    You can set the colormap for an image, pcolor, scatter, etc,
    using a keyword argument::

      imshow(X, cmap=cm.hot)

    or using the :func:`set_cmap` function::

      imshow(X)
      pyplot.set_cmap('hot')
      pyplot.set_cmap('jet')

    In interactive mode, :func:`set_cmap` will update the colormap post-hoc,
    allowing you to see which one works best for your data.

    All built-in colormaps can be reversed by appending ``_r``: For instance,
    ``gray_r`` is the reverse of ``gray``.

    There are several common color schemes used in visualization:

    Sequential schemes
      for unipolar data that progresses from low to high
    Diverging schemes
      for bipolar data that emphasizes positive or negative deviations from a
      central value
    Cyclic schemes
      for plotting values that wrap around at the endpoints, such as phase
      angle, wind direction, or time of day
    Qualitative schemes
      for nominal data that has no inherent ordering, where color is used
      only to distinguish categories

    Matplotlib ships with 4 perceptually uniform colormaps which are
    the recommended colormaps for sequential data:

      =========   ===================================================
      Colormap    Description
      =========   ===================================================
      inferno     perceptually uniform shades of black-red-yellow
      magma       perceptually uniform shades of black-red-white
      plasma      perceptually uniform shades of blue-red-yellow
      viridis     perceptually uniform shades of blue-green-yellow
      =========   ===================================================

    The following colormaps are based on the `ColorBrewer
    <https://colorbrewer2.org>`_ color specifications and designs developed by
    Cynthia Brewer:

    ColorBrewer Diverging (luminance is highest at the midpoint, and
    decreases towards differently-colored endpoints):

      ========  ===================================
      Colormap  Description
      ========  ===================================
      BrBG      brown, white, blue-green
      PiYG      pink, white, yellow-green
      PRGn      purple, white, green
      PuOr      orange, white, purple
      RdBu      red, white, blue
      RdGy      red, white, gray
      RdYlBu    red, yellow, blue
      RdYlGn    red, yellow, green
      Spectral  red, orange, yellow, green, blue
      ========  ===================================

    ColorBrewer Sequential (luminance decreases monotonically):

      ========  ====================================
      Colormap  Description
      ========  ====================================
      Blues     white to dark blue
      BuGn      white, light blue, dark green
      BuPu      white, light blue, dark purple
      GnBu      white, light green, dark blue
      Greens    white to dark green
      Greys     white to black (not linear)
      Oranges   white, orange, dark brown
      OrRd      white, orange, dark red
      PuBu      white, light purple, dark blue
      PuBuGn    white, light purple, dark green
      PuRd      white, light purple, dark red
      Purples   white to dark purple
      RdPu      white, pink, dark purple
      Reds      white to dark red
      YlGn      light yellow, dark green
      YlGnBu    light yellow, light green, dark blue
      YlOrBr    light yellow, orange, dark brown
      YlOrRd    light yellow, orange, dark red
      ========  ====================================

    ColorBrewer Qualitative:

    (For plotting nominal data, `.ListedColormap` is used,
    not `.LinearSegmentedColormap`.  Different sets of colors are
    recommended for different numbers of categories.)

    * Accent
    * Dark2
    * Paired
    * Pastel1
    * Pastel2
    * Set1
    * Set2
    * Set3

    A set of colormaps derived from those of the same name provided
    with Matlab are also included:

      =========   =======================================================
      Colormap    Description
      =========   =======================================================
      autumn      sequential linearly-increasing shades of red-orange-yellow
      bone        sequential increasing black-white colormap with
                  a tinge of blue, to emulate X-ray film
      cool        linearly-decreasing shades of cyan-magenta
      copper      sequential increasing shades of black-copper
      flag        repetitive red-white-blue-black pattern (not cyclic at
                  endpoints)
      gray        sequential linearly-increasing black-to-white
                  grayscale
      hot         sequential black-red-yellow-white, to emulate blackbody
                  radiation from an object at increasing temperatures
      jet         a spectral map with dark endpoints, blue-cyan-yellow-red;
                  based on a fluid-jet simulation by NCSA [#]_
      pink        sequential increasing pastel black-pink-white, meant
                  for sepia tone colorization of photographs
      prism       repetitive red-yellow-green-blue-purple-...-green pattern
                  (not cyclic at endpoints)
      spring      linearly-increasing shades of magenta-yellow
      summer      sequential linearly-increasing shades of green-yellow
      winter      linearly-increasing shades of blue-green
      =========   =======================================================

    A set of palettes from the `Yorick scientific visualisation
    package <https://dhmunro.github.io/yorick-doc/>`_, an evolution of
    the GIST package, both by David H. Munro are included:

      ============  =======================================================
      Colormap      Description
      ============  =======================================================
      gist_earth    mapmaker's colors from dark blue deep ocean to green
                    lowlands to brown highlands to white mountains
      gist_heat     sequential increasing black-red-orange-white, to emulate
                    blackbody radiation from an iron bar as it grows hotter
      gist_ncar     pseudo-spectral black-blue-green-yellow-red-purple-white
                    colormap from National Center for Atmospheric
                    Research [#]_
      gist_rainbow  runs through the colors in spectral order from red to
                    violet at full saturation (like *hsv* but not cyclic)
      gist_stern    "Stern special" color table from Interactive Data
                    Language software
      ============  =======================================================

    A set of cyclic colormaps:

      ================  =================================================
      Colormap          Description
      ================  =================================================
      hsv               red-yellow-green-cyan-blue-magenta-red, formed by
                        changing the hue component in the HSV color space
      twilight          perceptually uniform shades of
                        white-blue-black-red-white
      twilight_shifted  perceptually uniform shades of
                        black-blue-white-red-black
      ================  =================================================

    Other miscellaneous schemes:

      ============= =======================================================
      Colormap      Description
      ============= =======================================================
      afmhot        sequential black-orange-yellow-white blackbody
                    spectrum, commonly used in atomic force microscopy
      brg           blue-red-green
      bwr           diverging blue-white-red
      coolwarm      diverging blue-gray-red, meant to avoid issues with 3D
                    shading, color blindness, and ordering of colors [#]_
      CMRmap        "Default colormaps on color images often reproduce to
                    confusing grayscale images. The proposed colormap
                    maintains an aesthetically pleasing color image that
                    automatically reproduces to a monotonic grayscale with
                    discrete, quantifiable saturation levels." [#]_
      cubehelix     Unlike most other color schemes cubehelix was designed
                    by D.A. Green to be monotonically increasing in terms
                    of perceived brightness. Also, when printed on a black
                    and white postscript printer, the scheme results in a
                    greyscale with monotonically increasing brightness.
                    This color scheme is named cubehelix because the (r, g, b)
                    values produced can be visualised as a squashed helix
                    around the diagonal in the (r, g, b) color cube.
      gnuplot       gnuplot's traditional pm3d scheme
                    (black-blue-red-yellow)
      gnuplot2      sequential color printable as gray
                    (black-blue-violet-yellow-white)
      ocean         green-blue-white
      rainbow       spectral purple-blue-green-yellow-orange-red colormap
                    with diverging luminance
      seismic       diverging blue-white-red
      nipy_spectral black-purple-blue-green-yellow-red-white spectrum,
                    originally from the Neuroimaging in Python project
      terrain       mapmaker's colors, blue-green-yellow-brown-white,
                    originally from IGOR Pro
      turbo         Spectral map (purple-blue-green-yellow-orange-red) with
                    a bright center and darker endpoints. A smoother
                    alternative to jet.
      ============= =======================================================

    The following colormaps are redundant and may be removed in future
    versions.  It's recommended to use the names in the descriptions
    instead, which produce identical output:

      =========  =======================================================
      Colormap   Description
      =========  =======================================================
      gist_gray  identical to *gray*
      gist_yarg  identical to *gray_r*
      binary     identical to *gray_r*
      =========  =======================================================

    .. rubric:: Footnotes

    .. [#] Rainbow colormaps, ``jet`` in particular, are considered a poor
      choice for scientific visualization by many researchers: `Rainbow Color
      Map (Still) Considered Harmful
      <https://ieeexplore.ieee.org/document/4118486/?arnumber=4118486>`_

    .. [#] Resembles "BkBlAqGrYeOrReViWh200" from NCAR Command
      Language. See `Color Table Gallery
      <https://www.ncl.ucar.edu/Document/Graphics/color_table_gallery.shtml>`_

    .. [#] See `Diverging Color Maps for Scientific Visualization
      <http://www.kennethmoreland.com/color-maps/>`_ by Kenneth Moreland.

    .. [#] See `A Color Map for Effective Black-and-White Rendering of
      Color-Scale Images
      <https://www.mathworks.com/matlabcentral/fileexchange/2662-cmrmap-m>`_
      by Carey Rappaport
    """
    return sorted(cm._cmap_registry)
