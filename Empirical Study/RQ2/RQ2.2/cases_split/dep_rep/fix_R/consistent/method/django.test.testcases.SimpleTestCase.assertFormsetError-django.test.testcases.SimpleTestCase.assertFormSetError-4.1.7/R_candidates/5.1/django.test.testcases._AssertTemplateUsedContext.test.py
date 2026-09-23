    def test(self):
        self.test_case._assert_template_used(
            self.template_name,
            [t.name for t in self.rendered_templates if t.name is not None],
            self.msg_prefix,
            self.count,
        )
