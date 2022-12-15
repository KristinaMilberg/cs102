def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """

    ciphertext = ""
    for item in plaintext:
        if item.isupper():  # проверка, является ли символ прописным
            c_index = ord(item) - ord("A")
            c_shifted = (c_index + shift) % 26 + ord("A")  # сдвиг текущего символа на shift
            ciphertext += chr(c_shifted)
        elif item.islower():  # проверка наличия символа в нижнем регистре
            c_index = ord(item) - ord("a")  # вычесть юникод 'a', чтобы получить индекс в диапазоне [0-25)
            c_shifted = (c_index + shift) % 26 + ord("a")
            ciphertext += chr(c_shifted)
        else:  # если нет алфавита оставить все как есть
            ciphertext += item
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for item in ciphertext:
        if item.isupper():
            c_index = ord(item) - ord("A")
            c_og_pos = (c_index - shift) % 26 + ord(
                "A"
            )  # сдвинуть текущий символ влево на позицию shift, чтобы получить его исходное положение
            plaintext += chr(c_og_pos)
        elif item.islower():
            c_index = ord(item) - ord("a")
            c_og_pos = (c_index - shift) % 26 + ord("a")
            plaintext += chr(c_og_pos)
        else:
            plaintext += item
    return plaintext
