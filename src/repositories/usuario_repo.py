from typing import Optional
from src.models.usuario import User
from src.db.neo4j import driver

class UserRepository:
    def save(self, user: User) -> None:
        with driver.session() as session:
            session.run(
                "MERGE (u:User {username: $username}) "
                "SET u.password_hash = $password_hash, u.token_ids = $token_ids",
                username=user.username,
                password_hash=user.password_hash,
                token_ids=user.token_ids
            )

    def find_by_username(self, username: str) -> Optional[User]:
        with driver.session() as session:
            result = session.run(
                "MATCH (u:User {username: $username}) RETURN u",
                username=username
            )
            record = result.single()
            if record:
                u = record["u"]
                return User(
                    username=u["username"],
                    password_hash=u["password_hash"],
                    token_ids=u.get("token_ids", [])
                )
            return None