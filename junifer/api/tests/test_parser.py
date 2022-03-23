import sys
from pathlib import Path
import tempfile
import pytest

from junifer.api.parser import parse_yaml


def test_parse_yaml():
    """Test parse yaml"""
    with pytest.raises(ValueError, match='does not exist'):
        parse_yaml('foo.yaml')

    with tempfile.TemporaryDirectory() as _tmpdir:
        fname = Path(_tmpdir) / 'test.yaml'
        with open(fname, 'w') as f:
            f.write('foo: bar\n')
            f.write('with: junifer.configs.juseless\n')

        assert 'junifer.configs.juseless' not in sys.modules
        contents = parse_yaml(fname)
        assert 'foo' in contents
        assert 'bar' == contents['foo']
        assert 'with' not in contents
        assert 'junifer.configs.juseless' in sys.modules

        assert 'junifer.testing.registry' not in sys.modules

        with open(fname, 'w') as f:
            f.write('foo: bar\n')
            f.write('with:\n')
            f.write('  - junifer.configs.juseless\n')
            f.write('  - junifer.testing.registry\n')

        contents = parse_yaml(fname.as_posix())
        assert 'foo' in contents
        assert 'bar' == contents['foo']
        assert 'with' not in contents
        assert 'junifer.testing.registry' in sys.modules