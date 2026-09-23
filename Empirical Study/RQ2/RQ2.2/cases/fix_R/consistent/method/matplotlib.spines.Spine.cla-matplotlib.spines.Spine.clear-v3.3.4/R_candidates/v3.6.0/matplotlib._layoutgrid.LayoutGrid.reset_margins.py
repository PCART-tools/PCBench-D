    def reset_margins(self):
        """
        Reset all the margins to zero.  Must do this after changing
        figure size, for instance, because the relative size of the
        axes labels etc changes.
        """
        for todo in ['left', 'right', 'bottom', 'top',
                     'leftcb', 'rightcb', 'bottomcb', 'topcb']:
            self.edit_margins(todo, 0.0)
