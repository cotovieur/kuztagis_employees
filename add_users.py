import json
import os
from werkzeug.security import generate_password_hash

def load_users():
    try:
        if os.path.exists('users.json'):
            with open('users.json', 'r') as file:
                return json.load(file)
    except json.JSONDecodeError:
        pass
    return {"users": []}  # Ensure the dictionary has a 'users' key

def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

def add_user(users):
    username = input("Enter username (or type 'exit' to finish): ")
    if username.lower() == 'exit':
        return False

    password = input("Enter password: ")
    hashed_password = generate_password_hash(password)

    # Ensure the 'users' key exists in the dictionary
    if 'users' not in users:
        users['users'] = []

    # Check if the username already exists
    user_exists = False
    for user in users['users']:
        if user['username'] == username:
            user['password'] = hashed_password  # Update the password
            user_exists = True
            break

    if not user_exists:
        users['users'].append({
            "username": username,
            "password": hashed_password
        })

    return True

def main():
    users = load_users()

    while True:
        if not add_user(users):
            break

    save_users(users)
    print("Users saved to users.json")

if __name__ == "__main__":
    main()
