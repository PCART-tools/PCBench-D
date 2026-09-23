    def _check_trim(
        self,
        count: int,
        max: int,
        obj: list,
        element: str,
        css: str | None = None,
        value: str = "...",
    ) -> bool:
        """
        Indicates whether to break render loops and append a trimming indicator

        Parameters
        ----------
        count : int
            The loop count of previous visible items.
        max : int
            The allowable rendered items in the loop.
        obj : list
            The current render collection of the rendered items.
        element : str
            The type of element to append in the case a trimming indicator is needed.
        css : str, optional
            The css to add to the trimming indicator element.
        value : str, optional
            The value of the elements display if necessary.

        Returns
        -------
        result : bool
            Whether a trimming element was required and appended.
        """
        if count > max:
            if element == "row":
                obj.append(self._generate_trimmed_row(max))
            else:
                obj.append(_element(element, css, value, True, attributes=""))
            return True
        return False
