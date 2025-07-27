from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import numpy as np
from datetime import datetime

app = FastAPI(title="ML Sentiment Analysis Service")

# Simple mock sentiment analyzer (replace with real model)
class SentimentAnalyzer:
    def __init__(self):
        self.positive_words = {"good", "great", "amazing", "excellent", "wonderful", "fantastic", "love"}
        self.negative_words = {"bad", "terrible", "awful", "horrible", "hate", "worst", "disappointing"}
    
    def analyze(self, text: str) -> Dict[str, float]:
        text_lower = text.lower()
        words = text_lower.split()
        
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            return {"positive": 0.5, "negative": 0.5, "neutral": 1.0}
        
        positive_score = positive_count / total_sentiment_words
        negative_score = negative_count / total_sentiment_words
        
        return {
            "positive": positive_score,
            "negative": negative_score,
            "neutral": 1 - max(positive_score, negative_score)
        }

analyzer = SentimentAnalyzer()

class TextInput(BaseModel):
    text: str

class BatchTextInput(BaseModel):
    texts: List[str]

class SentimentResponse(BaseModel):
    text: str
    sentiment: Dict[str, float]
    timestamp: datetime

class BatchSentimentResponse(BaseModel):
    results: List[SentimentResponse]
    processed_count: int

@app.get("/")
async def root():
    return {"service": "ML Sentiment Analysis", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": True}

@app.post("/analyze", response_model=SentimentResponse)
async def analyze_sentiment(input: TextInput):
    if not input.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    sentiment = analyzer.analyze(input.text)
    
    return SentimentResponse(
        text=input.text,
        sentiment=sentiment,
        timestamp=datetime.now()
    )

@app.post("/batch-analyze", response_model=BatchSentimentResponse)
async def batch_analyze_sentiment(input: BatchTextInput):
    if not input.texts:
        raise HTTPException(status_code=400, detail="No texts provided")
    
    results = []
    for text in input.texts:
        if text.strip():
            sentiment = analyzer.analyze(text)
            results.append(SentimentResponse(
                text=text,
                sentiment=sentiment,
                timestamp=datetime.now()
            ))
    
    return BatchSentimentResponse(
        results=results,
        processed_count=len(results)
    )

@app.get("/model/info")
async def model_info():
    return {
        "model_type": "rule-based",
        "version": "1.0.0",
        "features": ["sentiment_analysis"],
        "languages": ["en"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)