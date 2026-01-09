"""
Fact Extraction Module

This module provides functions for extracting structured facts from emergency call transcripts.
It identifies location, hazards, people status, vehicle information, and urgency indicators.
"""

from typing import Dict, Any


def extract_facts(transcript: str) -> Dict[str, Any]:
    """
    Extract structured facts from transcript.
    
    In production, this would use NLP/NER models or LLM-based extraction.
    Currently uses keyword-based pattern matching.
    
    Args:
        transcript: The emergency call transcript text
        
    Returns:
        dict: Dictionary containing extracted facts:
            - location_found: bool
            - location_text: str or None
            - has_fuel_leak: bool
            - has_fire: bool
            -is_trapped:bool
            - people_unresponsive: bool
            - people_injured: bool
            - people_okay: bool
            - num_vehicles: int
            - vehicle_flipped: bool
            - explicit_urgency: bool
    """
    t = transcript.lower()
    
    facts = {
        # Location information
        "location_found": any([
            "highway" in t, "at " in t, "near " in t, 
            "street" in t, "road" in t, "avenue" in t,
            "parkside" in t, "underpass" in t
        ]),
        "location_text": None,
        
        # Hazards
        "has_fuel_leak": any(["smell gas" in t, "fuel" in t, "gas leak" in t]),
        "has_fire": any(["there is a fire" in t, "flames" in t, "burning" in t, "fire" in t]),

        "is_trapped": any(["i'm trapped" in t,"they're trapped" in t, "someone's trapped" in t, "they are trapped" in t, "trapped" in t]),
        
        # People status
        "people_unresponsive": any([
            "not moving" in t, "not answering" in t, 
            "unconscious" in t, "passed out" in t
        ]),
        "people_injured": any([
            " im hurt" in t,"someone is hurt" in t, "injured" in t, "bleeding" in t,
            "blood" in t, "wound" in t, "injuries" in t,
        ]),
        "people_okay": any([
            "everyone is okay" in t, "people are okay" in t,
            "no one is hurt" in t, "no one hurt" in t
        ]),
        
        # Vehicle information
        "num_vehicles": 1,
        "vehicle_flipped": any(["flipped" in t, "overturned" in t, "upside down" in t]),
        
        # Urgency indicators
        "explicit_urgency": any([
            "please come fast" in t, "hurry" in t, "emergency" in t,
            "please help" in t, "oh my god" in t, "immediately" in t
        ]),
    }
    
    # Count vehicles
    if "two car" in t or "two cars" in t or "two other cars" in t:
        facts["num_vehicles"] = 2
    elif "three" in t and ("car" in t or "vehicle" in t):
        facts["num_vehicles"] = 3
    elif "four car" in t or "four cars" in t or "four other cars" in t:
        facts["num_vehicles"] = 4
    elif "five car" in t or "five cars" in t or "five other cars" in t:
        facts["num_vehicles"] = 5
    
    # Extract location text if present
    if "at " in t:
        idx = t.find("at ")
        location_snippet = t[idx:idx+30]
        facts["location_text"] = location_snippet.strip()
    
    return facts


def has_critical_hazards(facts: Dict[str, Any]) -> bool:
    """
    Check if the call has critical hazards (fire or fuel leak).
    
    Args:
        facts: Dictionary of extracted facts
        
    Returns:
        bool: True if critical hazards are present
    """
    return facts.get("has_fire", False) or facts.get("has_fuel_leak", False)


def has_life_threatening_injuries(facts: Dict[str, Any]) -> bool:
    """
    Check if the call involves life-threatening injuries.
    
    Args:
        facts: Dictionary of extracted facts
        
    Returns:
        bool: True if life-threatening injuries are present
    """
    return facts.get("people_unresponsive", False) or (
        facts.get("people_injured", False) and not facts.get("people_okay", False)
    )


def get_vehicle_count(facts: Dict[str, Any]) -> int:
    """
    Get the number of vehicles involved.
    
    Args:
        facts: Dictionary of extracted facts
        
    Returns:
        int: Number of vehicles
    """
    return facts.get("num_vehicles", 1)

