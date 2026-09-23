    def pick(self, *args):
        """Trigger pick event

        Call signature::

            pick(mouseevent)

        each child artist will fire a pick event if mouseevent is over
        the artist and the artist has picker set
        """
        martist.Artist.pick(self, args[0])
