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
    for i, letter in enumerate(plaintext):
        if "A" <= letter <= "Z":
            ciphertext += chr(ord("A") + (ord(letter) + ord(keyword[i % len(keyword)]) - 2 * ord("A")) % 26)
        elif "a" <= letter <= "z":
            ciphertext += chr(ord("a") + (ord(letter) + ord(keyword[i % len(keyword)]) - 2 * ord("a")) % 26)
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
    for i, letter in enumerate(ciphertext):
        if "A" <= letter <= "Z":
            plaintext += chr(ord("A") + (ord(letter) - ord(keyword[i % len(keyword)])) % 26)
        elif "a" <= letter <= "z":
            plaintext += chr(ord("a") + (ord(letter) - ord(keyword[i % len(keyword)])) % 26)
        else:
            plaintext += ciphertext[i]
    return plaintext
