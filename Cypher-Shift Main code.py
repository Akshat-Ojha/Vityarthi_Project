def is_prime(number):
    if number < 2:
        return False
    d = 2
    while d * d <= number:
        if number % d == 0:
            return False
        d += 1
    return True


def next_prime(seed_pin):
    cand = seed_pin + 1
    while not is_prime(cand):
        cand += 1
    return cand


def lcg_pseudo_random(seed_pin):
    # Standard LCG parameters for 32-bit generation
    a, c, m = 1103515245, 12345, 2147483648
    return (a * seed_pin + c) % m


def generate_shift_key(seed_pin):
    prime = next_prime(seed_pin)
    rnd = lcg_pseudo_random(seed_pin)
    key = (prime + rnd) % 256
    if key == 0:
        key = prime % 255 + 1
    return key, prime, rnd


def manually_reverse_array(items):
    res = []
    for i in range(len(items) - 1, -1, -1):
        res.append(items[i])
    return res


def encrypt_message(message, shift_key):
    res = []
    for ch in message:
        val = ord(ch)
        shifted = val + shift_key
        b = bin(shifted)[2:]
        res.append(b)
    return manually_reverse_array(res)


def decrypt_message(encrypted_values, shift_key):
    ordered = manually_reverse_array(encrypted_values)
    chars = []
    for b in ordered:
        shifted = int(b, 2)
        val = shifted - shift_key
        if val < 0 or val > 1114111:
            raise ValueError("The encrypted data or PIN does not match.")
        chars.append(chr(val))
    return "".join(chars)


def get_pin():
    while True:
        try:
            pin = int(input("Enter a non-negative numeric PIN seed: "))
            if pin < 0:
                print("Please enter a PIN of 0 or greater.")
            else:
                return pin
        except ValueError:
            print("Invalid PIN. Please enter whole numbers only, for example 1234.")


def get_encrypted_array():
    while True:
        raw = input("Paste the encrypted binary values (comma-separated or full array): ").strip()
        if raw == "":
            print("The encrypted array cannot be empty.")
            continue

        if raw.startswith("[") and raw.endswith("]"):
            raw = raw[1:-1].strip()

        clean = []
        valid = True

        # Parse comma-separated list and strip optional quote wrappers
        for item in raw.split(","):
            b = item.strip()
            if len(b) >= 2:
                sq = b.startswith("'") and b.endswith("'")
                dq = b.startswith('"') and b.endswith('"')
                if sq or dq:
                    b = b[1:-1].strip()

            if b == "" or any(bit not in "01" for bit in b):
                valid = False
                break
            clean.append(b)

        if valid:
            return clean

        print("Invalid array. Use binary values only, such as 101001, 110010, or ['101001', '110010'].")


def display_key_details(shift_key, prime_number, random_number):
    print("\nKey generation details:")
    print("Next prime number:", prime_number)
    print("LCG pseudo-random number:", random_number)
    print("Generated shift key:", shift_key)


def encrypt_flow():
    print("\n--- Encrypt Message ---")
    msg = input("Enter the message to encrypt: ")
    if msg == "":
        print("Message cannot be empty.")
        return

    pin = get_pin()
    key, prime, rnd = generate_shift_key(pin)
    enc = encrypt_message(msg, key)

    display_key_details(key, prime, rnd)
    print("\nFinal encrypted binary values (reversed and ready to copy):")
    print(", ".join(enc))
    print("\nTo decrypt, choose option 2 and paste the entire line above.")
    print("The program also accepts the old format with [brackets] and 'quotes'.")
    print("Use the same PIN seed:", pin)


def decrypt_flow():
    print("\n--- Decrypt Message ---")
    enc = get_encrypted_array()
    pin = get_pin()
    key, prime, rnd = generate_shift_key(pin)

    try:
        dec = decrypt_message(enc, key)
        display_key_details(key, prime, rnd)
        print("\nDecrypted message:", dec)
    except ValueError as err:
        print("Could not decrypt the message:", err)


def main():
    print("========================================")
    print("   Cipher-Shift Cryptography Engine")
    print("========================================")
    print("Educational project: not for real secure data.\n")

    while True:
        print("1. Encrypt Message")
        print("2. Decrypt Message")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            encrypt_flow()
        elif choice == "2":
            decrypt_flow()
        elif choice == "3":
            print("Thank you for using Cipher-Shift. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.\n")


if __name__ == "__main__":
    main()