import os

import lemonade as l


def press_enter():
    input("\nPress [Enter] to continue...")


def main():
    debug_mode = False
    app = "2026"

    while app != "0":
        os.system("cls")

        print("Lemonade Cryptography - Made by Vlinho")
        print("\n    0 - Quit")
        print("    1 - Encrypt message")
        print("    2 - Decrypt message")
        print("    3 - Encrypt file")
        print("    4 - Encrypt file with .sourkey")
        print("    5 - Decrypt .lemon file")
        print("    6 - Generate .sourkey")
        print(
            "debug - Debug mode"
            if not debug_mode
            else "debug - Normal mode"
        )

        app = input("\n>>> ")

        match app:

            case "0":
                os.system("cls")

            case "1":
                print("\nENCRYPT MESSAGE =================")

                message = input(
                    "\nMessage: "
                ).encode("utf-8")

                crypt, key = l.encrypt(message)

                print("\nEncrypted bytes:")
                print(crypt)

                print("\nKey:")
                print(key)

                press_enter()


            case "2":
                print("\nDECRYPT MESSAGE =================")

                crypt = eval(
                    input("\nEncrypted bytes: ")
                )

                key = eval(
                    input("\nKey bytes: ")
                )

                result = l.decrypt(
                    crypt,
                    key
                )

                print("\nMessage:")
                print(result.decode("utf-8"))

                press_enter()


            case "3":
                print("\nENCRYPT FILE ====================")

                file_path = input(
                    "\nFile path: "
                )

                output_directory = input(
                    "\nOutput directory: "
                )

                with open(file_path, "rb") as file:
                    data = file.read()

                l.encrypt_to_file(
                    data,
                    output_directory
                )

                print("\nFile encrypted.")

                press_enter()


            case "4":
                print("\nENCRYPT WITH SOURKEY ============")

                file_path = input(
                    "\nFile path: "
                )

                output_directory = input(
                    "\nOutput directory: "
                )

                sourkey_path = input(
                    "\n.sourkey path: "
                )

                with open(file_path, "rb") as file:
                    data = file.read()

                l.encrypt_with_sourkey_to_file(
                    data,
                    output_directory,
                    sourkey_path
                )

                print("\nFile encrypted with sourkey.")

                press_enter()


            case "5":
                print("\nDECRYPT .LEMON FILE =============")

                lemon_path = input(
                    "\n.lemon path: "
                )

                sourkey_path = input(
                    "\n.sourkey path: "
                )

                output_path = input(
                    "\nOutput file path: "
                )

                data = l.decrypt_from_file(
                    lemon_path,
                    sourkey_path
                )

                with open(output_path, "wb") as file:
                    file.write(data)

                print("\nFile decrypted.")

                press_enter()


            case "6":
                print("\nGENERATE SOURKEY ================")

                path = input(
                    "\nOutput .sourkey path: "
                )

                length = int(
                    input("\nKey length (bytes): ")
                )

                l.generate_sourkey_file(
                    path,
                    length
                )

                print("\nSourkey generated.")

                press_enter()


            case "debug":
                debug_mode = not debug_mode

            case _:
                pass


if __name__ == "__main__":
    main()