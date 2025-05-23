from typing import Optional
from src.models.encuesta import Poll
from datetime import datetime
from src.db.neo4j import driver

class PollRepository:
    def save(self, poll: Poll) -> None:
        with driver.session() as session:
            session.run(
                """
                MERGE (p:Poll {id: $id})
                SET p.question = $question,
                    p.options = $options,
                    p.votes = $votes,
                    p.status = $status,
                    p.created_at = $created_at,
                    p.duration_seconds = $duration_seconds
                """,
                id=poll.id,
                question=poll.question,
                options=poll.options,
                votes=poll.votes,
                status=poll.status,
                created_at=poll.created_at.isoformat(),
                duration_seconds=poll.duration_seconds
            )

    def find_by_id(self, poll_id: str) -> Optional[Poll]:
        with driver.session() as session:
            result = session.run(
                "MATCH (p:Poll {id: $id}) RETURN p",
                id=poll_id
            )
            record = result.single()
            if record:
                p = record["p"]
                # Neo4j stores everything as string, so we need to convert types
                created_at = datetime.fromisoformat(p["created_at"])
                return Poll(
                    id=p["id"],
                    question=p["question"],
                    options=p["options"],
                    votes=p.get("votes", {}),
                    status=p["status"],
                    created_at=created_at,
                    duration_seconds=int(p["duration_seconds"])
                )
            return None