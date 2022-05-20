import sys

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

test_args = ["test1", "test2", "test3"]
with patch.object(sys, 'argv', test_args):
    import arg


def test_arg():
    arg_ = arg.Arg()
    assert arg_.env == 'test3'
