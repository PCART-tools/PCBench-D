    @docstring.dedent_interpd
    def legend(self, *args, **kwargs):
        """
        Place a legend on the figure.

        To make a legend from existing artists on every axes::

          legend()

        To make a legend for a list of lines and labels::

          legend( (line1, line2, line3),
                  ('label1', 'label2', 'label3'),
                  loc='upper right')

        These can also be specified by keyword::

          legend(handles=(line1, line2, line3),
                labels=('label1', 'label2', 'label3'),
                loc='upper right')

        Parameters
        ----------

        handles : sequence of `.Artist`, optional
            A list of Artists (lines, patches) to be added to the legend.
            Use this together with *labels*, if you need full control on what
            is shown in the legend and the automatic mechanism described above
            is not sufficient.

            The length of handles and labels should be the same in this
            case. If they are not, they are truncated to the smaller length.

        labels : sequence of strings, optional
            A list of labels to show next to the artists.
            Use this together with *handles*, if you need full control on what
            is shown in the legend and the automatic mechanism described above
            is not sufficient.

        Other Parameters
        ----------------

        %(_legend_kw_doc)s

        Returns
        -------
        :class:`matplotlib.legend.Legend` instance

        Notes
        -----
        Not all kinds of artist are supported by the legend command. See
        :doc:`/tutorials/intermediate/legend_guide` for details.
        """

        handles, labels, extra_args, kwargs = mlegend._parse_legend_args(
                self.axes,
                *args,
                **kwargs)
        # check for third arg
        if len(extra_args):
            # cbook.warn_deprecated(
            #     "2.1",
            #     "Figure.legend will accept no more than two "
            #     "positional arguments in the future.  Use "
            #     "'fig.legend(handles, labels, loc=location)' "
            #     "instead.")
            # kwargs['loc'] = extra_args[0]
            # extra_args = extra_args[1:]
            pass
        l = mlegend.Legend(self, handles, labels, *extra_args, **kwargs)
        self.legends.append(l)
        l._remove_method = self.legends.remove
        self.stale = True
        return l
