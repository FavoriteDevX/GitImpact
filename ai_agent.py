import os
from openai import OpenAI
from pydantic import BaseModel
from typing import List

# Enforce structured output from the LLM
class ImpactAnalysis(BaseModel):
    category: str
    impact_summary: str
    estimated_time_saved_hours: float
    security_vulnerabilities_patched: List[str]
    confidence_score: float

def analyze_commit_impact(diff_content: str, commit_message: str) -> ImpactAnalysis:
    """
    Leverages LLM with structured outputs to convert raw Git code changes 
    into measurable recruitment and engineering metrics.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    system_prompt = (
        "You are an elite Staff Engineer auditing code contributions. "
        "Analyze the provided Git diff and message. Extract real-world business "
        "and runtime optimization value. Be hyper-critical. Ignore formatting or trivial changes."
    )
    
    user_prompt = f"Commit Message: {commit_message}\n\nGit Diff:\n{diff_content}"
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format=ImpactAnalysis,
    )
    
    return completion.choices[0].message.parsed

# Example execution layout
if __name__ == "__main__":
    sample_diff = "@@ -12,4 +12,2 @@\ -    for i in range(len(data)):\n-        if data[i] in lookup_set:\n+    # Optimization: Replaced O(N) lookup loop with direct O(1) set checking\n+    return [x for x in data if x in lookup_set]"
    sample_msg = "perf: optimize array filtering speed overhead"
    
    analysis = analyze_commit_impact(sample_diff, sample_msg)
    print(analysis.model_dump_json(indent=2))
