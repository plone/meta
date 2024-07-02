import toml


def dump_string(value):
    if "\n" in value:
        # Return a multi line string as a multi line string,
        # instead of on one line with literal '\n' in it.
        return f"'''\n{value}'''"
    return toml.encoder._dump_str(value)


class TomlArraySeparatorEncoderWithNewline(toml.TomlArraySeparatorEncoder):
    """Special version indenting the first element of and array.

    In https://github.com/zopefoundation/meta/issues/118 we suggest to switch
    to Python 3.11 and its built-in toml support. We'll see if this path is
    still needed then.
    """

    def __init__(self, _dict=dict, preserve=False, separator=",",
                 indent_first_line=False):
        super(TomlArraySeparatorEncoderWithNewline, self).__init__(
            _dict=_dict, preserve=preserve, separator=separator)
        self.indent_first_line = indent_first_line
        self.dump_funcs[str] = dump_string

    def dump_list(self, v):
        t = []
        retval = "["
        if self.indent_first_line:
            retval += self.separator.strip(',')
        for u in v:
            t.append(self.dump_value(u))
        while t != []:
            s = []
            for u in t:
                if isinstance(u, list):
                    for r in u:
                        s.append(r)
                else:
                    retval += " " + u + self.separator
            t = s
        retval += " ]"
        return retval
