"""
Process Call Module

This module provides functions for processing individual emergency calls
through the complete pipeline: emotion detection, fact extraction, triage scoring,
and UI suggestions.
"""

from typing import Dict, Any
import emotion_detection
import fact_extraction
import triage_scoring
import dispatcher_assistance


def process_call(call: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a single emergency call through the complete pipeline.
    
    Args:
        call: Dictionary containing call information with keys:
            - call_id: str
            - transcript: str
            - asr_conf: float
            - llm_conf: float
            - timestamp: str (optional)
            - bg_noise: str (optional)
        
    Returns:
        dict: Dictionary containing processed results:
            - call_id: str
            - transcript: str (truncated)
            - asr_conf: float
            - llm_conf: float
            - emotion_score: float
            - emotion_class: str
            - severity_band: str
            - triage_score: float
            - triage_label: str
            - gate_ok: bool
            - num_ai_suggestions: int
            - has_calm_strategies: bool
            - facts: dict
            - ui_suggestions: dict
    """
    # Run emotion detection
    emo_score = emotion_detection.detect_emotion(call["transcript"])
    emotion_class = emotion_detection.classify_emotion_class(emo_score)
    severity_band = emotion_detection.get_severity_band(emo_score)
    
    # Extract facts
    facts = fact_extraction.extract_facts(call["transcript"])
    
    # Get UI suggestions
    ui = dispatcher_assistance.get_ui_suggestions(call, facts, emo_score)
    
    # Calculate triage score
    triage_score = triage_scoring.final_triage(emo_score, facts)
    triage_label = triage_scoring.get_triage_label(triage_score)
    
    # Calculate dispatch time
    dispatch_time = dispatcher_assistance.calculate_dispatch_time(triage_label, ui["gate_ok"])
    
    return {
        "call_id": call["call_id"],
        "timestamp": call.get("timestamp", ""),
        "transcript": call["transcript"][:50] + "..." if len(call["transcript"]) > 50 else call["transcript"],
        "asr_conf": call["asr_conf"],
        "llm_conf": call["llm_conf"],
        "emotion_score": emo_score,
        "emotion_class": emotion_class,
        "severity_band": severity_band,
        "triage_score": triage_score,
        "triage_label": triage_label,
        "gate_ok": ui["gate_ok"],
        "num_ai_suggestions": len(ui["ai_suggestions"]),
        "has_calm_strategies": len(ui["calm_down_strategies"]) > 0,
        "dispatch_time_s": dispatch_time,
        "facts": facts,
        "ui_suggestions": ui,
    }


def get_call_details(call: Dict[str, Any], processed_result: Dict[str, Any] = None) -> str:
    """
    Get detailed analysis string for a call.
    
    Args:
        call: Dictionary containing call information
        processed_result: Optional pre-processed result (if None, will process call)
        
    Returns:
        str: Formatted string with call details
    """
    if processed_result is None:
        processed_result = process_call(call)
    
    emo_score = processed_result["emotion_score"]
    emotion_class = processed_result["emotion_class"]
    severity_band = processed_result["severity_band"]
    facts = processed_result["facts"]
    ui = processed_result["ui_suggestions"]
    triage_score = processed_result["triage_score"]
    triage_label = processed_result["triage_label"]
    
    details = []
    details.append(f"\n{'='*80}")
    details.append(f"CALL DETAILS: {call['call_id']}")
    details.append(f"{'='*80}")
    details.append(f"\n📞 TRANSCRIPT:")
    details.append(f"   {call['transcript']}")
    details.append(f"\n🎭 EMOTION ANALYSIS:")
    details.append(f"   Score: {emo_score:.2f}/5.0")
    details.append(f"   Class: {emotion_class.upper()}")
    details.append(f"   Severity Band: {severity_band.upper()}")
    details.append(f"\n📋 EXTRACTED FACTS:")
    for key, value in facts.items():
        if value and key != "location_text":
            details.append(f"   ✓ {key.replace('_', ' ').title()}")
    details.append(f"\n🏥 TRIAGE ASSESSMENT:")
    details.append(f"   Score: {triage_score}/5.0")
    details.append(f"   Label: {triage_label}")
    details.append(f"\n✅ POLICY GATE:")
    details.append(f"   ASR Confidence: {call['asr_conf']:.2f}")
    details.append(f"   LLM Confidence: {call['llm_conf']:.2f}")
    details.append(f"   Gate Status: {'PASSED ✓' if ui['gate_ok'] else 'FAILED ✗'}")
    details.append(f"\n💡 AI SUGGESTIONS:")
    if ui['ai_suggestions']:
        for i, suggestion in enumerate(ui['ai_suggestions'], 1):
            details.append(f"   {i}. {suggestion}")
    else:
        details.append(f"   (No suggestions - gate failed or all info collected)")
    details.append(f"\n🧘 CALM-DOWN STRATEGIES:")
    if ui['calm_down_strategies']:
        for strategy in ui['calm_down_strategies']:
            details.append(f"   • {strategy}")
    else:
        details.append(f"   (No calm-down strategies needed - caller is relatively calm)")
    details.append(f"\n{'='*80}\n")
    
    return "\n".join(details)


def print_call_details(call: Dict[str, Any], processed_result: Dict[str, Any] = None) -> None:
    """
    Print detailed analysis for a call.
    
    Args:
        call: Dictionary containing call information
        processed_result: Optional pre-processed result (if None, will process call)
    """
    print(get_call_details(call, processed_result))

