
def STRING_TO_BINARY(char: str) -> str:
    """Converts input character into it's 8-bit binary value."""
    if len(char) > 1:
        raise ValueError
    binary = bin(ord(char))[2:]
    if len(binary) < 8:
        binary = "0"*(8-len(binary))+binary
    return binary


def BINARY_TO_STRING(str: str) -> str:
    str = str.strip()
    char = chr(int(str, 2))
    return char


def BINARY_TO_HEXA(str: str) -> str:
    """Converts the inputted binary string to hexadecimal value"""
    hexa = hex(int(str, 2))[2:]
    return hexa


def HEXA_TO_BINARY(str: str) -> str:
    """Converts the Hexa decimal value of the given input to binary"""
    binary = ""
    binary = bin(int(str, 16))[2:]
    if len(binary) < 8:
        binary = "0"*(8-len(binary))+binary
    return binary


def XNOR(binary1: str, binary2: str) -> str:
    """XNOR two inputted binary string..Returns the XNOR value"""

    if type(binary1) is not str and type(binary2) is not str:
        raise TypeError
    if len(binary1) != len(binary2):
        raise ValueError
        # print(binary1, binary2)
    xnor_values = {"00": '1', "01": '0', "10": '0', "11": '1'}
    new_binary = ""
    for i in range(0, len(binary1)):
        new_binary += xnor_values[binary1[i]+binary2[i]]
    return new_binary


def SHIFT(encrypted_String: str) -> list:
    """Shifts the input value..."""
    encrypted_values = encrypted_String.split(" ")
    shift_index = 1
    var = 0
    temp = 0
    for item in range(0, len(encrypted_values)-2):
        if (item+1) % 4 == 0:
            if shift_index == 4:
                shift_index = 1
                temp = 0
                continue
            shift_index += 1
            var = 0
            continue
        if shift_index == 1:
            encrypted_values[item], encrypted_values[item +
                                                     shift_index] = encrypted_values[item+shift_index], encrypted_values[item]
        elif shift_index == 2:
            if var != 2:
                encrypted_values[item], encrypted_values[item +
                                                         shift_index] = encrypted_values[item+shift_index], encrypted_values[item]
                var += 1
        elif shift_index == 3:
            encrypted_values[item+shift_index -
                             temp], encrypted_values[item] = encrypted_values[item], encrypted_values[item+shift_index-temp]
            temp += 1

        elif shift_index == 4:
            continue

    return encrypted_values


def REVERSE_SHIFT(encrypted_String: str) -> list:
    """Reverse The shifting algorithm"""
    encrypted_values = encrypted_String.split(" ")
    shift_index = 3
    var = 0
    temp = 0
    for item in range(0, len(encrypted_values)-2):
        if (item+1) % 4 == 0:
            if shift_index == 4:
                shift_index = 1
                temp = 0
                continue
            shift_index -= 1
            var = 0
            continue
        if shift_index == 1:
            encrypted_values[item], encrypted_values[item +
                                                     shift_index] = encrypted_values[item+shift_index], encrypted_values[item]
        elif shift_index == 2:
            if var != 2:
                encrypted_values[item], encrypted_values[item +
                                                         shift_index] = encrypted_values[item+shift_index], encrypted_values[item]
                var += 1
        elif shift_index == 3:
            encrypted_values[item+shift_index -
                             temp], encrypted_values[item] = encrypted_values[item], encrypted_values[item+shift_index-temp]
            temp += 1

        elif shift_index == 4:
            continue

    return encrypted_values


def encrypt(password: str, private_key: str = "") -> str:
    """Encrypts the value passed as agrument. Returns a String format of the encrypted data"""
    from sls import SLS_BOX, PRIVATE_KEY
    hexa = ""
    if private_key == "":
        private_key = PRIVATE_KEY
    for i in password:
        hexa = hexa+" "+BINARY_TO_HEXA(XNOR(STRING_TO_BINARY(i), private_key))
    hexa = hexa.strip()
    encrypt_level1 = SHIFT(hexa)
    for i in range(0, len(encrypt_level1)):
        encrypt_level1[i] = SLS_BOX[encrypt_level1[i]]
    return ''.join(encrypt_level1)


def decrypt(encypted_data, private_key: str = ""):
    """Decrypts the given input to original form"""
    from sls import SLS_BOX, PRIVATE_KEY
    if len(encypted_data) % 2 != 0:
        return ValueError
    if private_key == "":
        private_key = PRIVATE_KEY
    encypted_value = []
    for i in range(0, len(encypted_data), 2):
        for key, value in SLS_BOX.items():
            if encypted_data[i:i+2] == value:
                encypted_value.append(key)
    encypted_value = REVERSE_SHIFT(" ".join(encypted_value))
    original_text = ""
    for i in encypted_value:
        original_text += BINARY_TO_STRING(XNOR(HEXA_TO_BINARY(i), private_key))

    return original_text


def generate_key(name: str) -> str:
    """Generates unique Key for current session"""
    import random
    key = 0
    for i in name:
        key += ord(i)
    key = STRING_TO_BINARY(chr(key))
    unique_key = ""
    dataSet = ["0", "1"]
    for i in range(0, len(key)):
        unique_key += random.choice(dataSet)
    key = XNOR(key, unique_key)
    if len(key) > 8:
        sub_key1, sub_key2 = key[:len(key)//2], key[len(key)//2:]
        if len(sub_key1) < 8:
            sub_key1 = "0"*(8-len(sub_key1))+sub_key1
        if len(sub_key2) < 8:
            sub_key2 = "0"*(8-len(sub_key2))+sub_key2
        key = XNOR(sub_key1, sub_key2)
    return key
