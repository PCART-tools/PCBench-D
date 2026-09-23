    def is_ajax(self):
        warnings.warn(
            'request.is_ajax() is deprecated. See Django 3.1 release notes '
            'for more details about this deprecation.',
            RemovedInDjango40Warning,
            stacklevel=2,
        )
        return self.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
