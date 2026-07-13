import os
import ast

import lemonade as l


def press_enter():
    input("\nPress [Enter] to continue...")


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def read_bytes(prompt):
    value = input(prompt)

    try:
        result = ast.literal_eval(value)

        if not isinstance(result, bytes):
            raise ValueError

        return result

    except Exception:
        print("\nInvalid bytes format.")
        return None


def main():
    option = ""

    while option != "0":
        clear()

        print("🍋 Lemonade Cryptography - Made by Vlinho")
        print()
        print("    0 - Quit")
        print()
        print(" MESSAGE")
        print("    1 - Encrypt message")
        print("    2 - Encrypt message with key")
        print("    3 - Decrypt message")
        print()
        print(" FILES")
        print("    4 - Encrypt file")
        print("    5 - Encrypt file with .sourkey")
        print("    6 - Decrypt .lemon file")
        print()
        print(" KEY")
        print("    7 - Generate .sourkey")

        option = input("\n>>> ")

        match option:
            case "0":
                clear()

            case "1":
                print("\nENCRYPT MESSAGE =================")

                message = input("\nMessage: ").encode("utf-8")

                crypt, key = l.encrypt(message)

                print("\nEncrypted:", end="")
                print(crypt)

                print("\nKey:", end="")
                print(key)

                press_enter()

            case "2":
                print("\nENCRYPT WITH KEY ================")

                message = input("\nMessage: ").encode("utf-8")
                key = read_bytes("\nKey bytes: ")

                crypt = l.encrypt_with_key(message, key)

                print("\nEncrypted:", end="")
                print(crypt)

                press_enter()

            case "3":
                print("\nDECRYPT MESSAGE =================")

                crypt = read_bytes("\nEncrypted bytes: ")
                key = read_bytes("\nKey bytes: ")

                message = l.decrypt(crypt, key)

                print("\nMessage: ", end="")
                print(message.decode("utf-8"))

                press_enter()

            case "4":
                print("\nENCRYPT FILE ====================")

                file_path = input("\nFile path: ")
                output = input("\nOutput directory: ")

                l.encrypt_to_file(file_path, output)

                print("\nFile encrypted successfully.")

                press_enter()

            case "5":
                print("\nENCRYPT FILE WITH SOURKEY =======")

                file_path = input("\nFile path: ")
                output = input("\nOutput directory: ")
                sourkey = input("\n.sourkey path: ")

                l.encrypt_with_sourkey_to_file(file_path, output, sourkey)

                print("\nFile encrypted with sourkey.")

                press_enter()

            case "6":
                print("\nDECRYPT .LEMON FILE =============")

                lemon = input("\n.lemon path: ")
                sourkey = input("\n.sourkey path: ")
                output = input("\nOutput directory: ")

                l.decrypt_from_file(lemon, sourkey, output)

                print("\nFile restored successfully.")
                
                press_enter()

            case "7":
                print("\nGENERATE SOURKEY ================")

                path = input("\nOutput .sourkey path: ")
                length = int(input("\nKey length (bytes): "))

                l.generate_sourkey_file(path, length)

                print("\n.sourkey generated.")

                press_enter()

            case _:
                pass


if __name__ == "__main__":
    main()