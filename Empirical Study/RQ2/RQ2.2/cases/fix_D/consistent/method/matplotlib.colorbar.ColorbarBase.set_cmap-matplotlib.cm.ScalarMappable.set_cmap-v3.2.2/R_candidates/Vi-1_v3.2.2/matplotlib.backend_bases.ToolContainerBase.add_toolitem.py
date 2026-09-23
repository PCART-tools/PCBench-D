    def add_toolitem(self, name, group, position, image, description, toggle):
        """
        Add a toolitem to the container

        This method must get implemented per backend

        The callback associated with the button click event,
        must be **EXACTLY** `self.trigger_tool(name)`

        Parameters
        ----------
        name : str
            Name of the tool to add, this gets used as the tool's ID and as the
            default label of the buttons
        group : String
            Name of the group that this tool belongs to
        position : Int
            Position of the tool within its group, if -1 it goes at the End
        image_file : String
            Filename of the image for the button or `None`
        description : String
            Description of the tool, used for the tooltips
        toggle : Bool
            * `True` : The button is a toggle (change the pressed/unpressed
              state between consecutive clicks)
            * `False` : The button is a normal button (returns to unpressed
              state after release)
        """
        raise NotImplementedError
