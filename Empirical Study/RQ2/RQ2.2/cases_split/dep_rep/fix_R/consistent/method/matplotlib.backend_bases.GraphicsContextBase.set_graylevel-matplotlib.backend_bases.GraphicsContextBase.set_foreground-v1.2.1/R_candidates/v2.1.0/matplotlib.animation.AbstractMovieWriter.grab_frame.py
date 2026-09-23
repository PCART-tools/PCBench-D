    @abc.abstractmethod
    def grab_frame(self, **savefig_kwargs):
        '''
        Grab the image information from the figure and save as a movie frame.

        All keyword arguments in savefig_kwargs are passed on to the `savefig`
        command that saves the figure.
        '''
