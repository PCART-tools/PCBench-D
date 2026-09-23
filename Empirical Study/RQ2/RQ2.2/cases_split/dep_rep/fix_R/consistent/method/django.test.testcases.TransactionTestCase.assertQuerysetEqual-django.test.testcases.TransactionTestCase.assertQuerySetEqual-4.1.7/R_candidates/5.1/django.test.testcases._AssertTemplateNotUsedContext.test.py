    def test(self):
        rendered_template_names = [
            t.name for t in self.rendered_templates if t.name is not None
        ]
        self.test_case.assertFalse(
            self.template_name in rendered_template_names,
            f"{self.msg_prefix}Template '{self.template_name}' was used "
            f"unexpectedly in rendering the response",
        )
