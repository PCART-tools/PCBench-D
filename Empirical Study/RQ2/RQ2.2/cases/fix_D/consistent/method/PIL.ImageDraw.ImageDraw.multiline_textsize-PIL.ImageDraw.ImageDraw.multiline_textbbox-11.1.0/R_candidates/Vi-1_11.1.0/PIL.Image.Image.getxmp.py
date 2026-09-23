    def getxmp(self) -> dict[str, Any]:
        """
        Returns a dictionary containing the XMP tags.
        Requires defusedxml to be installed.

        :returns: XMP tags in a dictionary.
        """

        def get_name(tag: str) -> str:
            return re.sub("^{[^}]+}", "", tag)

        def get_value(element: Element) -> str | dict[str, Any] | None:
            value: dict[str, Any] = {get_name(k): v for k, v in element.attrib.items()}
            children = list(element)
            if children:
                for child in children:
                    name = get_name(child.tag)
                    child_value = get_value(child)
                    if name in value:
                        if not isinstance(value[name], list):
                            value[name] = [value[name]]
                        value[name].append(child_value)
                    else:
                        value[name] = child_value
            elif value:
                if element.text:
                    value["text"] = element.text
            else:
                return element.text
            return value

        if ElementTree is None:
            warnings.warn("XMP data cannot be read without defusedxml dependency")
            return {}
        if "xmp" not in self.info:
            return {}
        root = ElementTree.fromstring(self.info["xmp"].rstrip(b"\x00"))
        return {get_name(root.tag): get_value(root)}
