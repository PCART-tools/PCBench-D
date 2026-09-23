    def _check_image_library_installed(self):
        try:
            from PIL import Image  # NOQA
        except ImportError:
            return [
                checks.Error(
                    'Cannot use ImageField because Pillow is not installed.',
                    hint=('Get Pillow at https://pypi.python.org/pypi/Pillow '
                          'or run command "pip install Pillow".'),
                    obj=self,
                    id='fields.E210',
                )
            ]
        else:
            return []
