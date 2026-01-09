"""
Data Module

This module provides functions for loading and managing emergency call data.
"""

from typing import List, Dict, Any


def get_dummy_calls() -> List[Dict[str, Any]]:
    """
    Get dummy emergency call data for testing.
    
    Returns:
        list: List of dictionaries containing call information
    """
    return [
        {
            "call_id": "A317",
            "transcript": "There has been a crash near highway 6 underpass. Two cars. One driver not moving. I smell gas.",
            "asr_conf": 0.92,      # STT confidence was good
            "llm_conf": 0.81,      # LLM thought its summary is good
            "bg_noise": "siren",
            "timestamp": "2024-10-15 14:32:15",
        },
        {
            "call_id": "B204",
            "transcript": "I was in a small accident, we are on the side of the road, everyone is talking, I think people are okay.",
            "asr_conf": 0.78,
            "llm_conf": 0.70,
            "bg_noise": "crowd",
            "timestamp": "2024-10-15 14:35:42",
        },
        {
            "call_id": "C118",
            "transcript": "My mom fell and she is not answering me properly. We are at 411 Parkside. Please come fast.",
            "asr_conf": 0.85,
            "llm_conf": 0.73,
            "bg_noise": "quiet",
            "timestamp": "2024-10-15 14:38:01",
        },
        {
            "call_id": "D456",
            "transcript": "Oh my god, there's blood everywhere! The car flipped over and I can't get to my friend! Please help!",
            "asr_conf": 0.88,
            "llm_conf": 0.82,
            "bg_noise": "traffic",
            "timestamp": "2024-10-15 14:40:23",
        },
        {
            "call_id": "E789",
            "transcript": "Hi, I just need to report a minor fender bender. No one is hurt, just some damage to the bumper.",
            "asr_conf": 0.95,
            "llm_conf": 0.88,
            "bg_noise": "quiet",
            "timestamp": "2024-10-15 14:42:10",
        },
    ]


def load_calls_from_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Load calls from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        list: List of call dictionaries
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    import json
    
    with open(file_path, 'r') as f:
        calls = json.load(f)
    
    return calls


def save_calls_to_file(calls: List[Dict[str, Any]], file_path: str) -> None:
    """
    Save calls to a JSON file.
    
    Args:
        calls: List of call dictionaries
        file_path: Path to save the JSON file
    """
    import json
    
    with open(file_path, 'w') as f:
        json.dump(calls, f, indent=2)


def validate_call(call: Dict[str, Any]) -> bool:
    """
    Validate that a call dictionary has all required fields.
    
    Args:
        call: Call dictionary to validate
        
    Returns:
        bool: True if call is valid, False otherwise
    """
    required_fields = ["call_id", "transcript", "asr_conf", "llm_conf"]
    return all(field in call for field in required_fields)

