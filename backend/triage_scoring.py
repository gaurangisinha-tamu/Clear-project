"""
Triage Scoring Module

This module provides functions for calculating triage scores based on emotion
and extracted facts. Uses policy-aligned rules for interpretability.
"""

from typing import Dict


def triage_from_facts(facts: Dict) -> float:
    """
    Calculate triage score based on extracted facts.
    
    Uses policy-aligned rules (not ML) for interpretability.
    Higher scores indicate more urgent situations.
    
    Args:
        facts: Dictionary of extracted facts from transcript
        
    Returns:
        float: Triage score between 1.0 and 5.0
    """
    score = 1.0  # Base score
    
    # Critical factors (highest priority)
    if facts.get("people_unresponsive", False):
        score = max(score, 4.8)  # Unresponsive = critical
    if facts.get("has_fire", False):
        score = max(score, 4.9)  # Fire = extreme critical
    if facts.get("vehicle_flipped", False):
        score = max(score, 4.5)  # Flipped vehicle = high critical
    
    # High priority factors
    if facts.get("has_fuel_leak", False):
        score = max(score, 4.3)  # Fuel leak = high risk
    if facts.get("people_injured", False) and not facts.get("people_okay", False):
        score = max(score, 4.2)  # Injuries present = high priority
    
    # Medium priority factors
    if facts.get("num_vehicles", 1) > 1:
        score = max(score, 3.5)  # Multiple vehicles = medium-high
    if facts.get("explicit_urgency", False):
        score = max(score, 3.8)  # Explicit urgency call = medium-high
    
    # Low priority factors
    if facts.get("people_okay", False) and facts.get("num_vehicles", 1) == 1:
        score = min(score, 2.5)  # Single vehicle, people okay = lower priority
    
    return score


def final_triage(emotion_score: float, facts: Dict) -> float:
    """
    Final triage score combining emotion and facts.
    
    Policy: Take the maximum of emotion and fact-based scores,
    as either can indicate urgency.
    
    Args:
        emotion_score: Emotion severity score (1.0-5.0)
        facts: Dictionary of extracted facts
        
    Returns:
        float: Final triage score between 1.0 and 5.0 (rounded to 1 decimal)
    """
    fact_score = triage_from_facts(facts)
    
    # Combine: take max (emotion or facts can indicate urgency)
    triage = max(emotion_score, fact_score)
    
    # Round to 1 decimal place, clip to 1-5
    return round(max(1.0, min(5.0, triage)), 1)


def get_triage_label(triage_score: float) -> str:
    """
    Get human-readable triage label from score.
    
    Args:
        triage_score: Triage score (1.0-5.0)
        
    Returns:
        str: Triage label (LOW, MEDIUM, HIGH, CRITICAL)
    """
    if triage_score >= 4.5:
        return "CRITICAL"
    elif triage_score >= 3.5:
        return "HIGH"
    elif triage_score >= 2.5:
        return "MEDIUM"
    else:
        return "LOW"


def get_triage_label_info(triage_label: str) -> Dict:
    """
    Get information about a triage label.
    
    Args:
        triage_label: Triage label (LOW, MEDIUM, HIGH, CRITICAL)
        
    Returns:
        dict: Information about the triage label
    """
    triage_info = {
        "LOW": {
            "score_range": (1.0, 2.5),
            "description": "Non-life-threatening situation, minimal urgency",
            "dispatch_priority": "Low",
            "response_time": "Standard (15+ seconds)"
        },
        "MEDIUM": {
            "score_range": (2.5, 3.5),
            "description": "Moderate urgency, requires attention but not immediately life-threatening",
            "dispatch_priority": "Medium",
            "response_time": "Moderate (10-15 seconds)"
        },
        "HIGH": {
            "score_range": (3.5, 4.5),
            "description": "High urgency, potential for serious harm",
            "dispatch_priority": "High",
            "response_time": "Fast (5-10 seconds)"
        },
        "CRITICAL": {
            "score_range": (4.5, 5.0),
            "description": "Immediate life-threatening situation",
            "dispatch_priority": "Critical",
            "response_time": "Immediate (1-5 seconds)"
        }
    }
    return triage_info.get(triage_label, {})

