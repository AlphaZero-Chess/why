from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/search", tags=["search"])

# Emergent LLM key from environment
EMERGENT_API_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

class SuggestionsResponse(BaseModel):
    suggestions: List[str]
    query: str

async def get_ai_suggestions(query: str, limit: int = 5) -> List[str]:
    """Get AI suggestions using emergentintegrations"""
    from emergentintegrations.llm.chat import chat, Message, LLMConfig
    
    try:
        config = LLMConfig(
            model_name="gpt-4o-mini",
            api_key=EMERGENT_API_KEY,
            temperature=0.7,
            max_output_tokens=200
        )
        
        messages = [
            Message(
                role="system",
                content="You are a search suggestion assistant. Given a partial search query, provide relevant autocomplete suggestions. Return ONLY a JSON array of strings with suggested completions. No explanations, just the array."
            ),
            Message(
                role="user", 
                content=f"Provide {limit} search suggestions for: \"{query}\""
            )
        ]
        
        response = await chat(config=config, messages=messages)
        content = response.message.strip()
        
        # Parse JSON array from response
        if content.startswith('['):
            suggestions = json.loads(content)
        else:
            start = content.find('[')
            end = content.rfind(']') + 1
            if start >= 0 and end > start:
                suggestions = json.loads(content[start:end])
            else:
                suggestions = [query]
        
        return suggestions[:limit]
        
    except Exception as e:
        logger.error(f"AI suggestions error: {e}")
        raise

@router.get("/suggestions", response_model=SuggestionsResponse)
async def get_search_suggestions(q: str, limit: int = 5):
    """Get AI-powered search suggestions"""
    if not q or len(q.strip()) < 2:
        return SuggestionsResponse(suggestions=[], query=q)
    
    try:
        suggestions = await get_ai_suggestions(q, limit)
        return SuggestionsResponse(
            suggestions=suggestions,
            query=q
        )
        
    except Exception as e:
        logger.error(f"AI suggestions failed: {e}")
        # Fallback suggestions based on common patterns
        fallback = [
            f"{q} tutorial",
            f"{q} example",
            f"{q} documentation",
            f"how to {q}",
            f"{q} guide"
        ]
        return SuggestionsResponse(
            suggestions=fallback[:limit],
            query=q
        )
