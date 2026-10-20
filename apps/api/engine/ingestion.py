import asyncio
import httpx
import redis.asyncio as aioredis
import time

class GitHubIngestionEngine:
    def __init__(self, github_token: str, redis_url: str):
        self.github_token = github_token
        self.graphql_url = "https://github.com"
        self.redis = aioredis.from_url(redis_url)
        self.headers = {
            "Authorization": f"Bearer {github_token}",
            "Content-Type": "application/json"
        }

    async def _enforce_rate_limit(self, weight: int = 1):
        """
        Leaky Bucket mechanism over Redis to survive intense GitHub GraphQL Rate Limits.
        """
        rate_limit_key = "github:rate_limit:tokens"
        max_tokens = 5000
        leak_rate_per_sec = 1.38  # Matches GitHub's default restoration rate
        
        while True:
            pipe = self.redis.pipeline()
            await pipe.get("github:rate_limit:last_leak")
            await pipe.get(rate_limit_key)
            last_leak, tokens = await pipe.execute()
            
            now = time.time()
            tokens = float(tokens) if tokens else float(max_tokens)
            last_leak = float(last_leak) if last_leak else now
            
            # Leak tokens (restore quota based on time elapsed)
            delta = now - last_leak
            tokens = min(max_tokens, tokens + (delta * leak_rate_per_sec))
            
            if tokens >= weight:
                # Consume tokens
                tokens -= weight
                pipe = self.redis.pipeline()
                await pipe.set("github:rate_limit:last_leak", now)
                await pipe.set(rate_limit_key, tokens)
                await pipe.execute()
                return True
            
            # Backoff dynamically based on token depletion deficit
            await asyncio.sleep(0.5)

    async def fetch_user_contributions(self, username: str, cursor: str = None) -> dict:
        """
        Executes highly dense GraphQL query targeted at deep commit and PR extraction.
        """
        await self._enforce_rate_limit(weight=5) # Deep queries cost higher weight
        
        query = """
        query($username: String!, $cursor: String) {
          user(login: $username) {
            pullRequests(first: 20, after: $cursor, states: MERGED, orderBy: {field: CREATED_AT, direction: DESC}) {
              pageInfo { hasNextPage, endCursor }
              nodes {
                id
                title
                repository { name, owner { login } }
                commits(first: 50) {
                  nodes {
                    commit {
                      oid
                      message
                      additions
                      deletions
                      changedFiles
                    }
                  }
                }
              }
            }
          }
        }
        """
        
        variables = {"username": username, "cursor": cursor}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.graphql_url, 
                json={"query": query, "variables": variables}, 
                headers=self.headers,
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json().get("data", {})
            else:
                raise Exception(f"GitHub GraphQL execution failed: {response.text}")
