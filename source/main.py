import json
import hashlib


def finish():
    print('FINISH')


def login_input():
    """
    Check if user want to log in or sign up.
    login_input() -> None
    """
    login_check = input('S or L: ').replace(' ', '')
    if login_check == 'L':
        log_in()
    elif login_check == 'S':
        sign_up()


def log_in():
    """
    Called when user wants to log in
    log_in() -> None
    """
    print('LOGGING IN')
    login = input('login: ')

    # Check if user wants quit to sign up
    if login == 'q':
        sign_up()
        return
    password = input('password: ')

    # Check if users login isn't already registered, then returns to log in
    if not presence_check(login):
        print('insert q into login to sign up')
        log_in()
        return
    else:
        # Open users.json file
        f = open('users.json')
        users = json.load(f)

        # Itarates through all users already registeres
        for user in users['users']:
            # Finds user with matching login
            if user['login'] == login:
                # Checks if passwords are matching, then finish. Else returns to log in
                if decrypt(password, user['password']):
                    finish()
                    return
                else:
                    print('Something went worng')
                    log_in()
                    return


def sign_up():
    """
    Called when user wants to log in
    sign_up() -> None
    """
    print('SIGNING UP')
    login = input('login: ')
    password = input('password: ')
    password1 = input('password: ')

    # Check if accounts with such login already exists, then returns to log in
    if presence_check(login):
        print('Something went worng')
        sign_up()
        return

    # Check if password is follow the rules, else returns to sign up
    if password != password1 or len(login) < 4 or len(password) < 4 or ' ' in password or login == 'q':
        print('Something went worng')
        sign_up()
        return

    # If all requirements are met, add a new user
    add_user(login, password)
    finish()


def encrypt(s):
    """
    Encrypts passwords by ms5 protocol
    encrypt(str) -> str
    """
    password = hashlib.md5(s.encode('ASCII'))
    return password.hexdigest()


def decrypt(s, password):
    """
    Check if password in database is matching given
    decrypt(str, str) -> bool
    """
    decrypted_s = hashlib.md5(s.encode('ASCII'))
    return password == decrypted_s.hexdigest()


def add_user(login, password):
    """
    Add user to db
    add_user(str, str) -> None
    """
    # Open users.json file
    f = open('users.json')
    users = json.load(f)

    # Adds dict with user data to db
    users['users'].append({'login': login, 'password': encrypt(password)})
    f = open('users.json', 'w')
    json.dump(users, f, indent=2)


def presence_check(login):
    """
    Check if given login is already in db
    presence_check(str) -> bool
    """
    # Open users.json file
    f = open('users.json')
    users = json.load(f)

    # Check if login is already in db
    for user in users['users']:
        if login == user['login']:
            return True
    return False


if__name__ == '__main__':
    login_input()
