import os
import lemonade as l

def press_enter():
    input("\nPress [Enter] to continue...")

def main():
    debugMode = False
    app = '2026'
    while app != '0':
        os.system("cls")
        print("Lemonade Cryptography - Made by Vlinho")
        print(l.encrypt("Lemonade Cryptography")[0])
        print("\n    0 - Quit")
        print("    1 - Encrypt")
        print("    2 - Decrypt")
        print("    3 - Decrypt from a .lemon file")
        print("debug - Debug mode") if not debugMode else print("debug - Normal mode")
        
        app = input("\n>>> ")
        
        match app:
            case "0":
                os.system("cls")
                
            case "1":
                print("\ ENCRYPT ==========================")
                msg = input("\nMessage: ")
                
                values = l.encrypt(msg)
                print("\nEncrypted message: " + values[0])
                print("\nKey: " + values[1])
                
                if debugMode:
                    print("\nrepr(values): " + repr(values))
                    print("\nlen(values): " + str(len(values)) + "\n")
                
                n = 1

                while os.path.exists(f"lemonade_{n}.lemon"):
                    print(f"lemonade_{n}.lemon exists.") if debugMode else None
                    n += 1
                
                print("...") if n == 1 and debugMode else None

                file_name = f"lemonade_{n}.lemon"
                print(f"\nfile_name: {file_name}.") if debugMode else None

                with open(file_name, "w", encoding="utf-8") as file:
                    file.write(f"CRYPTOGRAPHY:{values[0]}\n")
                    file.write(f"\nKEY:{values[1]}\n")

                press_enter()
                
            case "2":
                print("\nDECRYPT ==========================")
                crypt = input("\nCryptography: ")
                key = input("\nKey: ")
                
                print("\nMessage: " + l.decrypt(crypt, key))
                
                press_enter()
                
            case "3":
                print("\nDECRYPT FROM A .LEMON FILE =======")
                filePath = input("\nFile path: ")
                
                if not os.path.exists(filePath):
                    print(f"\n{filePath} doesn't exist.")
                else:
                    crypt = ""
                    key = ""
                    lemonadeFile = True
                    
                    with open(filePath, "r", encoding="utf-8") as file:
                        content = file.read()
                        
                        print("\nrepr(content): ", repr(content)) if debugMode else None
                        
                        values = content.split("\n\n")
                        print(f"\nvalues: {values}") if debugMode else None
                        
                        if values[0].startswith("CRYPTOGRAPHY:") and values[1].startswith("KEY:"):
                            crypt = values[0].removeprefix("CRYPTOGRAPHY:")
                            key = values[1].removeprefix("KEY:").strip()
                        else:
                            lemonadeFile = False
                    
                    if lemonadeFile:
                        print("\nCryptography: " + crypt)
                        print("\nKey: " + key)
                        print("\nMessage: " + l.decrypt(crypt, key))
                    else:
                        print("\nThe file path is not a lemonade file.")
                    
                press_enter()
                
            case "debug":
                if debugMode:
                    debugMode = False
                else:
                    debugMode = True
                
            case _:
                ...
    
if __name__ == '__main__':
    main()