from typing import Optional
from src.models.token_nft import TokenNFT
from datetime import datetime
from src.db.neo4j import driver

class NFTRepository:
    def save(self, token: TokenNFT) -> None:
        with driver.session() as session:
            session.run(
                """
                MERGE (t:TokenNFT {token_id: $token_id})
                SET t.owner = $owner,
                    t.poll_id = $poll_id,
                    t.option = $option,
                    t.issued_at = $issued_at
                """,
                token_id=token.token_id,
                owner=token.owner,
                poll_id=token.poll_id,
                option=token.option,
                issued_at=token.issued_at.isoformat()
            )

    def find_by_id(self, token_id: str) -> Optional[TokenNFT]:
        with driver.session() as session:
            result = session.run(
                "MATCH (t:TokenNFT {token_id: $token_id}) RETURN t",
                token_id=token_id
            )
            record = result.single()
            if record:
                t = record["t"]
                issued_at = datetime.fromisoformat(t["issued_at"])
                return TokenNFT(
                    token_id=t["token_id"],
                    owner=t["owner"],
                    poll_id=t["poll_id"],
                    option=t["option"],
                    issued_at=issued_at
                )
            return None