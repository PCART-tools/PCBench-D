    @classmethod
    def from_custom_template(
        cls, searchpath, html_table: str | None = None, html_style: str | None = None
    ):
        """
        Factory function for creating a subclass of ``Styler``.

        Uses custom templates and Jinja environment.

        .. versionchanged:: 1.3.0

        Parameters
        ----------
        searchpath : str or list
            Path or paths of directories containing the templates.
        html_table : str
            Name of your custom template to replace the html_table template.

            .. versionadded:: 1.3.0

        html_style : str
            Name of your custom template to replace the html_style template.

            .. versionadded:: 1.3.0

        Returns
        -------
        MyStyler : subclass of Styler
            Has the correct ``env``,``template_html``, ``template_html_table`` and
            ``template_html_style`` class attributes set.
        """
        loader = jinja2.ChoiceLoader([jinja2.FileSystemLoader(searchpath), cls.loader])

        # mypy doesn't like dynamically-defined classes
        # error: Variable "cls" is not valid as a type
        # error: Invalid base class "cls"
        class MyStyler(cls):  # type: ignore[valid-type,misc]
            env = jinja2.Environment(loader=loader)
            if html_table:
                template_html_table = env.get_template(html_table)
            if html_style:
                template_html_style = env.get_template(html_style)

        return MyStyler
