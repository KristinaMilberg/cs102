def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    list = []
    for i in range(len(plaintext)):
        if 65 <= ord(plaintext[i]) <= 90:
            shift = ord(keyword[i % len(keyword)]) - 65
            new = chr((ord(plaintext[i]) - 65 + shift) % 26 + 65)
            list.append(new)
        else:
            list.append(plaintext[i])
        ciphertext = "".join(list)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    list = []
    for i in range(len(ciphertext)):
        if 65 <= ord(ciphertext[i]) <= 90:
            shift = ord(keyword[i % len(keyword)]) + 65
            new = chr((ord(ciphertext[i]) - 65 - shift) % 26 + 65)
            list.append(new)
        else:
            list.append(ciphertext[i])
        plaintext = "".join(list)
    return plaintext
