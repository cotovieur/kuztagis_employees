from werkzeug.security import generate_password_hash

password = "user_password"
hashed_password = generate_password_hash(password)
print(hashed_password)
