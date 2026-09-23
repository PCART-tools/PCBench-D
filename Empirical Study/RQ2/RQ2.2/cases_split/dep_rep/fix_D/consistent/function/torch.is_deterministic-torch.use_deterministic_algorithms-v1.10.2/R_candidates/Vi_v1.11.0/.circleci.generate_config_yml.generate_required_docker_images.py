def generate_required_docker_images(items):
    required_docker_images = set()

    def _requires_docker_image(item_type, item):
        requires = item.get('requires', None)
        if not isinstance(requires, list):
            return
        for requirement in requires:
            requirement = requirement.replace('"', '')
            if requirement.startswith('docker-'):
                required_docker_images.add(requirement)

    _for_all_items(items, _requires_docker_image)
    return required_docker_images
