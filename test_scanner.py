from scanner import get_single_ports

def test_valid_ports():
    result = get_single_ports("22,80")
    assert result == [22,80]

def test_invalid_ports():
    result = get_single_ports("ABC")
    assert result == []

def test_mixed_ports():
    result = get_single_ports("22,ABC,80")
    assert result == [22,80]

def test_minimal_valid():
    result = get_single_ports("1")
    assert result == [1]

def test_maximal_valid():
    result = get_single_ports("65535")
    assert result == [65535]

def test_below_minimum():
    result = get_single_ports("0")
    assert result == []

def test_above_maximum():
    result = get_single_ports("65536")
    assert result == []
