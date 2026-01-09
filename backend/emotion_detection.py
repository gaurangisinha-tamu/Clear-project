"""
Emotion Detection Module

This module provides functions for detecting emotion severity from emergency call transcripts.
It includes emotion classification and severity band assignment.
"""

from typing import Dict, Tuple

# Emotion classification schema
EMOTION_CLASSES = {
    "calm": {"severity_range": (1.0, 2.0), "color": "green"},
    "concerned": {"severity_range": (2.0, 3.0), "color": "yellow"},
    "distressed": {"severity_range": (3.0, 4.0), "color": "orange"},
    "panicked": {"severity_range": (4.0, 5.0), "color": "red"},
}

# Emotion severity bands (for triage classification)
SEVERITY_BANDS = {
    "low": (1.0, 2.5),
    "medium": (2.5, 3.5),
    "high": (3.5, 4.5),
    "critical": (4.5, 5.0),
}

# Keyword-based emotion detection (simulating ML model output)
EMOTION_KEYWORDS = {
    # Critical urgency indicators
    "not moving": 4.8,
    "not answering": 4.5,
    "unconscious": 4.9,
    "blood everywhere": 4.9,
    "oh my god": 4.3,
    "please help": 4.6,
    "can't get to": 4.4,
    
    # High urgency
    "smell gas": 4.7,
  
    "flames": 4.8,
    "crash": 4.2,
    "please come fast": 4.4,
    "flipped over": 4.6,
    
    # Medium urgency
    "accident": 3.5,
    "fell": 3.8,
    "hurt": 3.6,
    "bleeding": 4.1,
    
    # Low urgency
    "small accident": 2.2,
    "minor": 2.0,
    "fender bender": 1.8,
    "everyone is okay": 2.0,
    "people are okay": 2.1,
}

DEFAULT_EMOTION = 2.5  # neutral/calm baseline


def detect_emotion(transcript: str) -> float:
    """
    Detect emotion severity score from transcript (1-5 scale).
    
    In production, this would use audio analysis (pitch, tone, pace) + NLP.
    Currently uses keyword-based detection with intensity boosters.
    
    Args:
        transcript: The emergency call transcript text
        
    Returns:
        float: Emotion severity score between 1.0 and 5.0
    """
    t = transcript.lower()
    score = DEFAULT_EMOTION
    
    # Check for urgency keywords
    for keyword, urgency_score in EMOTION_KEYWORDS.items():
        if keyword in t:
            score = max(score, urgency_score)
    
    # Add intensity boosters (exclamation marks, repetition)
    exclamations = t.count('!')
    if exclamations > 0:
        score += min(exclamations * 0.2, 0.6)
    
    # Repetition of urgent words
    urgent_words = ["help", "please", "hurry", "fast", "emergency"]
    for word in urgent_words:
        count = t.count(word)
        if count > 1:
            score += min(count * 0.15, 0.5)
    
    return max(1.0, min(5.0, score))


def classify_emotion_class(emotion_score: float) -> str:
    """
    Classify emotion into one of the emotion classes.
    
    Args:
        emotion_score: Emotion severity score (1.0-5.0)
        
    Returns:
        str: Emotion class name (calm, concerned, distressed, panicked)
    """
    for emotion, info in EMOTION_CLASSES.items():
        low, high = info["severity_range"]
        if low <= emotion_score < high:
            return emotion
    return "panicked"  # default for scores >= 5.0


def get_severity_band(emotion_score: float) -> str:
    """
    Get severity band for the emotion score.
    
    Args:
        emotion_score: Emotion severity score (1.0-5.0)
        
    Returns:
        str: Severity band name (low, medium, high, critical)
    """
    for band, (low, high) in SEVERITY_BANDS.items():
        if low <= emotion_score < high:
            return band
    return "critical"  # default for scores >= 5.0


def get_emotion_class_info(emotion_class: str) -> Dict:
    """
    Get information about an emotion class.
    
    Args:
        emotion_class: Emotion class name
        
    Returns:
        dict: Information about the emotion class including severity range and color
    """
    return EMOTION_CLASSES.get(emotion_class, {})


def get_severity_band_info(severity_band: str) -> Tuple[float, float]:
    """
    Get the severity range for a severity band.
    
    Args:
        severity_band: Severity band name
        
    Returns:
        tuple: (low, high) range for the severity band
    """
    return SEVERITY_BANDS.get(severity_band, (1.0, 5.0))

