    def update_buttons(self):
        valid = True
        for field in self.float_fields:
            if not is_edit_valid(field):
                valid = False
        for btn_type in (QtWidgets.QDialogButtonBox.Ok,
                         QtWidgets.QDialogButtonBox.Apply):
            btn = self.bbox.button(btn_type)
            if btn is not None:
                btn.setEnabled(valid)
