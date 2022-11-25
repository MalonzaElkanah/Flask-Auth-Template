import os
import secrets
import string


def generate_secret_key(length):
    """ Generate secret keys """

    characters = string.ascii_letters + string.digits + "!#$&*)_+[]}:>?"

    return "".join(secrets.choice(characters) for _ in range(int(length)))


def help():
    """ List Available Commands """

    scripts = {
        f"{help.__name__}": help, 
        f"{generate_secret_key.__name__}": generate_secret_key,
    }
    print("\n\tAvailable commands:")
    for script in scripts.values():
        print(f"\n\t\t* {script.__name__}: {script.__doc__}")


if __name__ == "__main__":
    scripts = {
        f"{help.__name__}": help, 
        f"{generate_secret_key.__name__}": generate_secret_key,
    }
    
    if len(os.sys.argv) > 1:
        if os.sys.argv[1] == generate_secret_key.__name__:
            if len(os.sys.argv) > 2:
                secret_key = generate_secret_key(os.sys.argv[2])
            else:
                secret_key = generate_secret_key(50)
            print(f"\n\t{secret_key}")
        elif scripts.get(os.sys.argv[1], None):
            print("\033[32m\t", scripts.get(os.sys.argv[1])(), "\033[00m")
        else:
            print("\033[31m\tScript not found\033[00m")
            help()
    else:
        print("\033[31m\tPlease specify a script after `scripts.py`\033[00m")
        help()

    print("\n") 
