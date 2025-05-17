class UserService:
    def __init__(self, repo):
        self.repo = repo

    def get_tokens(self, username):
        user_data = self.repo.find_by_id("users", username)
        return user_data.get("token_ids", []) if user_data else []