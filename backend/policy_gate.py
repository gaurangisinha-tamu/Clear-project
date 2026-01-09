"""
Policy Gate Module

This module provides functions for determining if AI suggestions should be shown
based on confidence thresholds for ASR (Automatic Speech Recognition) and LLM.
"""

from typing import Dict

# Default thresholds
ASR_THRESHOLD = 0.80
LLM_THRESHOLD = 0.75


def policy_gate(asr_conf: float, llm_conf: float, 
                asr_threshold: float = None, 
                llm_threshold: float = None) -> bool:
    """
    Policy gate: determines if AI suggestions should be shown.
    
    Only show AI assistance when confidence is high enough to ensure
    reliable suggestions.
    
    Args:
        asr_conf: ASR (Automatic Speech Recognition) confidence score (0.0-1.0)
        llm_conf: LLM (Large Language Model) confidence score (0.0-1.0)
        asr_threshold: Optional custom ASR threshold (default: 0.80)
        llm_threshold: Optional custom LLM threshold (default: 0.75)
        
    Returns:
        bool: True if gate passes (both thresholds met), False otherwise
    """
    asr_thresh = asr_threshold if asr_threshold is not None else ASR_THRESHOLD
    llm_thresh = llm_threshold if llm_threshold is not None else LLM_THRESHOLD
    
    return (asr_conf >= asr_thresh) and (llm_conf >= llm_thresh)


def get_default_thresholds() -> Dict[str, float]:
    """
    Get the default confidence thresholds.
    
    Returns:
        dict: Dictionary with 'asr_threshold' and 'llm_threshold'
    """
    return {
        "asr_threshold": ASR_THRESHOLD,
        "llm_threshold": LLM_THRESHOLD
    }

