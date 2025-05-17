from datetime import datetime
class NFTService:
    def __init__(self, repo):
        self.repo = repo

    def mint_token(self, username, poll_id, option):
        token_id = "token_" + str(datetime.now().timestamp())
        token_data = {
            "_id": token_id,
            "owner": username,
            "poll_id": poll_id,
            "option": option,
            "issued_at": datetime.now().isoformat()
        }
        self.repo.save("nfts", token_id, token_data)
        return {"token_id": token_id}