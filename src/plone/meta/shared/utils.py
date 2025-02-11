from copy import deepcopy


def cleanup_data_for_jinja(data):
    """Take a dictionary and cleanup before passing to Jinja.

    This makes it easier to insert in a Jinja template.
    Note: Initially this changed the dictionary inline, but then any changes
    are also written back to .meta.toml, if that is where the dictionary comes from.
    So return a new dictionary.

    * Fixes multi line strings.

      With this as input:

        classifiers = '''
            Environment :: Web Environment
            Framework :: Plone
        '''

      toml reads it as:

        '    Environment :: Web Environment\n    Framework :: Plone\n'

      We want to have the initial newline back.

    """
    if not data:
        return
    new_data = deepcopy(data)
    for key, value in new_data.items():
        if not isinstance(value, str):
            continue
        if "\n" in value and value.startswith(" "):
            new_data[key] = "\n" + value
    return new_data
