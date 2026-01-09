"""
Dispatcher Assistance Module

This module provides functions for generating UI suggestions, checklists,
and calm-down strategies for dispatchers handling emergency calls.
"""

from typing import Dict, Any, List
from policy_gate import policy_gate

# Checklist items
CHECKLIST_SPINE = ["Location", "Threats", "Hazards", "Injuries", "People_Status"]

# Context-aware prompts based on what's missing
PROMPT_TEMPLATES = {
    "location": "Confirm nearest cross-street / landmark.",
    "hazards": "Is there any fuel leak or flames?",
    "injuries": "Is anyone unconscious or bleeding heavily?",
    "people_status": "Can you confirm everyone's status?",
    "urgency": "Stay calm. Can you tell me exactly what happened?",
}

# Calm-down strategies
CALM_DOWN_STRATEGIES_HIGH = [
    "Take a deep breath. I'm here to help.",
    "We're getting help to you. Can you tell me exactly what happened?",
    "Stay calm. Help is on the way."
]

CALM_DOWN_STRATEGIES_MEDIUM = [
    "I understand this is stressful. Let's get through this together."
]


def get_ui_suggestions(call: Dict[str, Any], facts: Dict[str, Any], 
                       emotion_score: float) -> Dict[str, Any]:
    """
    Return what to show on the dispatcher screen for this call.
    
    Includes checklist, AI suggestions, and calm-down strategies.
    
    Args:
        call: Dictionary containing call information (must have 'asr_conf' and 'llm_conf')
        facts: Dictionary of extracted facts from transcript
        emotion_score: Emotion severity score (1.0-5.0)
        
    Returns:
        dict: Dictionary containing:
            - checklist: dict of checklist items and their completion status
            - ai_suggestions: list of AI-generated prompts
            - calm_down_strategies: list of calm-down strategies
            - gate_ok: bool indicating if policy gate passed
    """
    gate_ok = policy_gate(call["asr_conf"], call["llm_conf"])
    
    ui = {
        "checklist": {item: False for item in CHECKLIST_SPINE},
        "ai_suggestions": [],
        "calm_down_strategies": [],
        "gate_ok": gate_ok,
    }

    # Auto-check what we already know from facts
    if facts.get("location_found", False):
        ui["checklist"]["Location"] = True
    if facts.get("has_fuel_leak", False) or facts.get("has_fire", False):
        ui["checklist"]["Hazards"] = True
        ui["checklist"]["Threats"] = True
    if facts.get("people_unresponsive", False) or facts.get("people_injured", False):
        ui["checklist"]["Injuries"] = True
        ui["checklist"]["People_Status"] = True
    elif facts.get("people_okay", False):
        ui["checklist"]["People_Status"] = True

    # If gate passes → show AI suggestions
    if gate_ok:
        # Suggest prompts for missing information
        if not facts.get("location_found", False):
            ui["ai_suggestions"].append(PROMPT_TEMPLATES["location"])
        if not (facts.get("has_fuel_leak", False) or facts.get("has_fire", False)):
            ui["ai_suggestions"].append(PROMPT_TEMPLATES["hazards"])
        if not (facts.get("people_unresponsive", False) or 
                facts.get("people_injured", False) or 
                facts.get("people_okay", False)):
            ui["ai_suggestions"].append(PROMPT_TEMPLATES["people_status"])
    
    # Calm-down strategies for high emotion calls
    if emotion_score >= 4.0:
        ui["calm_down_strategies"] = CALM_DOWN_STRATEGIES_HIGH.copy()
    elif emotion_score >= 3.0:
        ui["calm_down_strategies"] = CALM_DOWN_STRATEGIES_MEDIUM.copy()

    return ui


def get_checklist_items() -> List[str]:
    """
    Get the list of checklist items.
    
    Returns:
        list: List of checklist item names
    """
    return CHECKLIST_SPINE.copy()


def get_prompt_templates() -> Dict[str, str]:
    """
    Get the prompt templates for AI suggestions.
    
    Returns:
        dict: Dictionary of prompt templates
    """
    return PROMPT_TEMPLATES.copy()


def calculate_dispatch_time(triage_label: str, gate_ok: bool) -> int:
    """
    Calculate dispatch time based on triage label and gate status.
    
    Higher triage = faster response. Gate OK = faster (better info).
    
    Args:
        triage_label: Triage label (LOW, MEDIUM, HIGH, CRITICAL)
        gate_ok: Whether policy gate passed
        
    Returns:
        int: Dispatch time in seconds
    """
    # Triage-based adjustments
    if triage_label == "CRITICAL":
        base_time = 3
    elif triage_label == "HIGH":
        base_time = 6
    elif triage_label == "MEDIUM":
        base_time = 10
    else:  # LOW
        base_time = 15
    
    # Gate OK (good info) → faster response
    if gate_ok:
        base_time = max(1, base_time - 2)
    
    return base_time

