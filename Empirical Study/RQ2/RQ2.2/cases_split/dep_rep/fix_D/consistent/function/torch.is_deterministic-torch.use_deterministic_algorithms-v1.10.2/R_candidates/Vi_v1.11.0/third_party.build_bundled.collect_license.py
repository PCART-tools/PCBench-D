def collect_license(current):
    collected = {}
    for root, dirs, files in os.walk(current):
        license = list(licenses & set(files))
        if license:
            name = root.split('/')[-1]
            license_file = os.path.join(root, license[0])
            try:
                ident = identify_license(license_file)
            except ValueError:
                raise ValueError('could not identify license file '
                                 f'for {root}') from None
            val = {
                'Name': name,
                'Files': [root],
                'License': ident,
                'License_file': [license_file],
            }
            if name in collected:
                # Only add it if the license is different
                if collected[name]['License'] == ident:
                    collected[name]['Files'].append(root)
                    collected[name]['License_file'].append(license_file)
                else:
                    collected[name + f' ({root})'] = val
            else:
                collected[name] = val
    return collected
