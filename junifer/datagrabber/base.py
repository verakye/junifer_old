from pathlib import Path

from ..utils.logging import raise_error


def _validate_types(types):
    """
    Validate the types
    """
    if not isinstance(types, list):
        raise_error("types must be a list", TypeError)
    if any(not isinstance(x, str) for x in types):
        raise_error("types must be a list of strings", TypeError)


def _validate_patterns(types, patterns):
    """
    Validate the patterns.
    """
    if not isinstance(types, list):
        raise_error("types must be a list", TypeError)
    if not isinstance(patterns, dict):
        raise_error("patterns must be a dict", TypeError)
    if len(types) != len(patterns):
        raise ValueError("types and patterns must have the same length")
    for i in range(len(types)):
        if not isinstance(types[i], str):
            raise_error("types must be a list of strings", TypeError)

    if any(x not in patterns for x in types):
        raise_error("patterns must contain all types", TypeError)


class BaseDataGrabber:
    def __init__(self, workdir, types):
        _validate_types(types)
        if not isinstance(workdir, Path):
            workdir = Path(workdir)
        self.workdir = workdir
        self.types = types

    def __iter__(self):
        for elem in self.get_elements():
            yield elem

    def __getitem__(self, element):
        raise NotImplementedError('__getitem__ not implemented')

    def get_elements(self):
        raise NotImplementedError('get_elements not implemented')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass


class BIDSDataGrabber(BaseDataGrabber):
    def __init__(self, workdir, types, patterns):
        _validate_patterns(types, patterns)
        super().__init__(workdir, types)
        self.patterns = patterns

    def get_elements(self):
        elems = [x for x in self.workdir.iterdir() if x.is_dir()]
        return elems

    def __getitem__(self, element):
        pass
