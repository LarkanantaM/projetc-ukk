

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def check_password(self, password):
        return self.password == password

    def __repr__(self):
        return f"User(username={self.username}, role={self.role})"