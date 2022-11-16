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
    for c in plaintext:
        if c.isupper():  # проверка, является ли символ прописным
            c_index = ord(c) - ord('A')
            c_shifted = (c_index + shift) % 26 + ord('A')  # сдвиг текущего символа на shift
            c_new = chr(c_shifted)
            ciphertext += c_new
        elif c.islower():  # проверка наличия символа в нижнем регистре
            c_index = ord(c) - ord('a')  # вычесть юникод 'a', чтобы получить индекс в диапазоне [0-25)
            c_shifted = (c_index + shift) % 26 + ord('a')
            c_new = chr(c_shifted)
            ciphertext += c_new
        else:  # если нет алфавита оставить все как есть
            ciphertext += c
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
    for c in ciphertext:
        if c.isupper():
            c_index = ord(c) - ord('A')
            c_og_pos = (c_index - shift) % 26 + ord('A')  # сдвинуть текущий символ влево на позицию shift, чтобы получить его исходное положение
            c_og = chr(c_og_pos)
            plaintext += c_og
        elif c.islower():
            c_index = ord(c) - ord('a')
            c_og_pos = (c_index - shift) % 26 + ord('a')
            c_og = chr(c_og_pos)
            plaintext += c_og
        else:
            plaintext += c
    return plaintext
