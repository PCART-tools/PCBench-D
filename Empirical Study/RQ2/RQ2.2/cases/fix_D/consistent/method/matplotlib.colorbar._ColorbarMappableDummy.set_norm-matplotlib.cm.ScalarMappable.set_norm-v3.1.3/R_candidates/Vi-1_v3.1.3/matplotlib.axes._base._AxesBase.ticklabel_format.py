    def ticklabel_format(self, *, axis='both', style='', scilimits=None,
                         useOffset=None, useLocale=None, useMathText=None):
        r"""
        Change the `~matplotlib.ticker.ScalarFormatter` used by
        default for linear axes.

        Optional keyword arguments:

          ==============   =========================================
          Keyword          Description
          ==============   =========================================
          *axis*           [ 'x' | 'y' | 'both' ]
          *style*          [ 'sci' (or 'scientific') | 'plain' ]
                           plain turns off scientific notation
          *scilimits*      (m, n), pair of integers; if *style*
                           is 'sci', scientific notation will
                           be used for numbers outside the range
                           10\ :sup:`m` to 10\ :sup:`n`.
                           Use (0,0) to include all numbers.
                           Use (m,m) where m <> 0 to fix the order
                           of magnitude to 10\ :sup:`m`.
          *useOffset*      [ bool | offset ]; if True,
                           the offset will be calculated as needed;
                           if False, no offset will be used; if a
                           numeric offset is specified, it will be
                           used.
          *useLocale*      If True, format the number according to
                           the current locale.  This affects things
                           such as the character used for the
                           decimal separator.  If False, use
                           C-style (English) formatting.  The
                           default setting is controlled by the
                           axes.formatter.use_locale rcparam.
          *useMathText*    If True, render the offset and scientific
                           notation in mathtext
          ==============   =========================================

        Only the major ticks are affected.
        If the method is called when the `~matplotlib.ticker.ScalarFormatter`
        is not the `~matplotlib.ticker.Formatter` being used, an
        `AttributeError` will be raised.
        """
        style = style.lower()
        axis = axis.lower()
        if scilimits is not None:
            try:
                m, n = scilimits
                m + n + 1  # check that both are numbers
            except (ValueError, TypeError):
                raise ValueError("scilimits must be a sequence of 2 integers")
        if style[:3] == 'sci':
            sb = True
        elif style == 'plain':
            sb = False
        elif style == '':
            sb = None
        else:
            raise ValueError("%s is not a valid style value")
        try:
            if sb is not None:
                if axis == 'both' or axis == 'x':
                    self.xaxis.major.formatter.set_scientific(sb)
                if axis == 'both' or axis == 'y':
                    self.yaxis.major.formatter.set_scientific(sb)
            if scilimits is not None:
                if axis == 'both' or axis == 'x':
                    self.xaxis.major.formatter.set_powerlimits(scilimits)
                if axis == 'both' or axis == 'y':
                    self.yaxis.major.formatter.set_powerlimits(scilimits)
            if useOffset is not None:
                if axis == 'both' or axis == 'x':
                    self.xaxis.major.formatter.set_useOffset(useOffset)
                if axis == 'both' or axis == 'y':
                    self.yaxis.major.formatter.set_useOffset(useOffset)
            if useLocale is not None:
                if axis == 'both' or axis == 'x':
                    self.xaxis.major.formatter.set_useLocale(useLocale)
                if axis == 'both' or axis == 'y':
                    self.yaxis.major.formatter.set_useLocale(useLocale)
            if useMathText is not None:
                if axis == 'both' or axis == 'x':
                    self.xaxis.major.formatter.set_useMathText(useMathText)
                if axis == 'both' or axis == 'y':
                    self.yaxis.major.formatter.set_useMathText(useMathText)
        except AttributeError:
            raise AttributeError(
                "This method only works with the ScalarFormatter.")
