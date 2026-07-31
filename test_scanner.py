from cgi import valid_boundary

from scanner import validate_ip

#happyPath
def test_valid_prefix_3_parts():
    assert validate_ip("192.168.2", 3) == True

def test_valid_full_ip_4_parts():
    assert validate_ip("192.168.2.1", 4) == True

#unhappyPath

def test_valid_ip_too_few_parts():
    assert validate_ip("192.168", 3) == False

def test_valid_ip_too_many_parts():
    assert validate_ip("192.168.2.1.1", 4) == False
