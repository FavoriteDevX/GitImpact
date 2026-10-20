import os
from openai import OpenAI
import psycopg2
from psycopg2.extras import execute_values

class SemanticImpactVectorEngine:
    def __init__(self, db_connection_string: str):
        self.conn_str = db_connection_string
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def _generate_embedding(self, text: str) -> list:
        """
        Converts text summaries and structural code codeblocks into dense vector representations.
        """
        response = self.client.embeddings.create(
            input=[text],
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    def store_vectorized_highlight(self, highlight_id: str, structured_text: str):
        """
        Saves embedding coordinates straight into PostgreSQL using pgvector.
        """
        embedding = self._generate_embedding(structured_text)
        
        conn = psycopg2.connect(self.conn_str)
        cursor = conn.cursor()
        
        query = """
            INSERT INTO "CodeHighlightVector" (highlight_id, embedding)
            VALUES (%s, %s)
            ON CONFLICT (highlight_id) DO UPDATE SET embedding = EXCLUDED.embedding;
        """
        
        cursor.execute(query, (highlight_id, embedding))
        conn.commit()
        cursor.close()
        conn.close()

    def query_developer_impact_by_intent(self, user_portfolio_id: str, natural_language_intent: str, limit: int = 3):
        """
        Searches a developer's real achievements semantically.
        Example query: 'Find code where this candidate fixed performance degradation or memory leaks'
        """
        query_embedding = self._generate_embedding(natural_language_intent)
        
        conn = psycopg2.connect(self.conn_str)
        cursor = conn.cursor()
        
        # Uses cosine distance (<=> operator in pgvector) to rank best technical feats
        semantic_search_query = """
            SELECT ch.id, ch.repository_name, ch.summary_title, ch.detailed_impact,
                   (chv.embedding <=> %s::vector) as distance
            FROM "CodeHighlight" ch
            JOIN "CodeHighlightVector" chv ON ch.id = chv.highlight_id
            WHERE ch.portfolio_id = %s
            ORDER BY distance ASC
            LIMIT %s;
        """
        
        cursor.execute(semantic_search_query, (query_embedding, user_portfolio_id, limit))
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        mapped_feats = []
        for row in results:
            mapped_feats.append({
                "id": row[0],
                "repo": row[1],
                "title": row[2],
                "impact": row[3],
                "confidence_match": round(1 - row[4], 4)
            })
            
        return mapped_feats
