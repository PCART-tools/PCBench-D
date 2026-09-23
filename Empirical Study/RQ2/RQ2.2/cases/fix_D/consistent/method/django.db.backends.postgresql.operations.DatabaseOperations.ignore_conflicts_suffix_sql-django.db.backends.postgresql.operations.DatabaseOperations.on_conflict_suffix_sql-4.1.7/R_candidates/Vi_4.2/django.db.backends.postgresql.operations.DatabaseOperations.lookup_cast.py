    def lookup_cast(self, lookup_type, internal_type=None):
        lookup = "%s"

        if lookup_type == "isnull" and internal_type in (
            "CharField",
            "EmailField",
            "TextField",
            "CICharField",
            "CIEmailField",
            "CITextField",
        ):
            return "%s::text"

        # Cast text lookups to text to allow things like filter(x__contains=4)
        if lookup_type in (
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "istartswith",
            "endswith",
            "iendswith",
            "regex",
            "iregex",
        ):
            if internal_type in ("IPAddressField", "GenericIPAddressField"):
                lookup = "HOST(%s)"
            # RemovedInDjango51Warning.
            elif internal_type in ("CICharField", "CIEmailField", "CITextField"):
                lookup = "%s::citext"
            else:
                lookup = "%s::text"

        # Use UPPER(x) for case-insensitive lookups; it's faster.
        if lookup_type in ("iexact", "icontains", "istartswith", "iendswith"):
            lookup = "UPPER(%s)" % lookup

        return lookup
