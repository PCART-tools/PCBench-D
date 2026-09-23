    @staticmethod
    def _is_domain_match(domain, hostname):
        """Implements domain matching adhering to RFC 6265."""
        if hostname == domain:
            return True

        if not hostname.endswith(domain):
            return False

        non_matching = hostname[:-len(domain)]

        if not non_matching.endswith("."):
            return False

        return not is_ip_address(hostname)
