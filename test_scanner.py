from scanner import validate_ip

#HappyPath
def test_validate_ip_3():
    result3 = validate_ip("192.168.2", 3)
    assert result3 == True

def test_validate_ip_4():
    result4 = validate_ip("192.168.2.1", 4)
    assert result4 == True
