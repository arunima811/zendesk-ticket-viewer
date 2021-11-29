from zendesk_viewer.utils import string_utils

def test_chunkstring():
    str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad"
    chunks = list(string_utils.chunkstring(str, 25))
    assert len(chunks) == 6
    assert "".join(chunks) == str