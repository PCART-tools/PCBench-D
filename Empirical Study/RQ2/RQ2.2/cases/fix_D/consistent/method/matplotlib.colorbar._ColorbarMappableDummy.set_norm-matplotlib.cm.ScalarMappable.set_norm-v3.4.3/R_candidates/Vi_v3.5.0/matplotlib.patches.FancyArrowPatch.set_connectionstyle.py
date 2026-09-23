    def set_connectionstyle(self, connectionstyle, **kw):
        """
        Set the connection style. Old attributes are forgotten.

        Parameters
        ----------
        connectionstyle : str or `.ConnectionStyle` or None, optional
            Can be a string with connectionstyle name with
            optional comma-separated attributes, e.g.::

                set_connectionstyle("arc,angleA=0,armA=30,rad=10")

            Alternatively, the attributes can be provided as keywords, e.g.::

                set_connectionstyle("arc", angleA=0,armA=30,rad=10)

            Without any arguments (or with ``connectionstyle=None``), return
            available styles as a list of strings.
        """

        if connectionstyle is None:
            return ConnectionStyle.pprint_styles()

        if (isinstance(connectionstyle, ConnectionStyle._Base) or
                callable(connectionstyle)):
            self._connector = connectionstyle
        else:
            self._connector = ConnectionStyle(connectionstyle, **kw)
        self.stale = True
