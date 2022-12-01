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
    for i in range(len(plaintext)):
        if "A" <= plaintext[i] <= "Z":
            ciphertext += chr(ord("A") + (ord(plaintext[i]) + ord(keyword[i % len(keyword)]) - 2 * ord("A")) % 26)
        elif "a" <= plaintext[i] <= "z":
            ciphertext += chr(ord("a") + (ord(plaintext[i]) + ord(keyword[i % len(keyword)]) - 2 * ord("a")) % 26)
        else:
            ciphertext += plaintext[i]
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
    for i in range(len(ciphertext)):
        if "A" <= ciphertext[i] <= "Z":
            plaintext += chr(ord("A") + (ord(ciphertext[i]) - ord(keyword[i % len(keyword)])) % 26)
        elif "a" <= ciphertext[i] <= "z":
            plaintext += chr(ord("a") + (ord(ciphertext[i]) - ord(keyword[i % len(keyword)])) % 26)
        else:
            plaintext += ciphertext[i]
    return plaintext


print(encrypt_vigenere("introduction to python", "lsci"))
