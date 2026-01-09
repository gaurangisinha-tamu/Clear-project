"""
Main Script

This is the main entry point for the emergency dispatch system.
It processes emergency calls and generates reports.
"""

import pandas as pd
from typing import List, Dict, Any

# Import modules
import data
import process_call
import evaluation
import visualization
import dispatcher_assistance


def process_all_calls(calls: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Process all emergency calls and return results as a DataFrame.
    
    Args:
        calls: List of call dictionaries
        
    Returns:
        pd.DataFrame: DataFrame containing processed results
    """
    records = []
    
    for call in calls:
        result = process_call.process_call(call)
        # Extract only the fields we want in the DataFrame
        records.append({
            "call_id": result["call_id"],
            "timestamp": result.get("timestamp", ""),
            "transcript": result["transcript"],
            "asr_conf": result["asr_conf"],
            "llm_conf": result["llm_conf"],
            "emotion_score": result["emotion_score"],
            "emotion_class": result["emotion_class"],
            "severity_band": result["severity_band"],
            "triage_score": result["triage_score"],
            "triage_label": result["triage_label"],
            "gate_ok": result["gate_ok"],
            "num_ai_suggestions": result["num_ai_suggestions"],
            "has_calm_strategies": result["has_calm_strategies"],
            "dispatch_time_s": result["dispatch_time_s"],
        })
    
    df = pd.DataFrame(records)
    return df


def get_dispatch_queue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get dispatch priority queue sorted by triage score.
    
    Args:
        df: DataFrame containing processed results
        
    Returns:
        pd.DataFrame: DataFrame sorted by triage score (highest first)
    """
    df_sorted = df.sort_values("triage_score", ascending=False).reset_index(drop=True)
    return df_sorted


def main():
    """
    Main function to run the emergency dispatch system.
    """
    print("=" * 80)
    print("EMERGENCY DISPATCH SYSTEM")
    print("=" * 80)
    
    # Load calls
    print("\nLoading emergency calls...")
    calls = data.get_dummy_calls()
    print(f"Loaded {len(calls)} calls")
    
    # Process all calls
    print("\nProcessing calls...")
    df = process_all_calls(calls)
    
    # Display summary
    print("\n" + "=" * 80)
    print("PROCESSED CALLS SUMMARY")
    print("=" * 80)
    print(df.to_string())
    
    # Get dispatch queue
    df_queue = get_dispatch_queue(df)
    print("\n" + "=" * 80)
    print("DISPATCH PRIORITY QUEUE (Sorted by Triage Score)")
    print("=" * 80)
    display_cols = ["call_id", "triage_score", "triage_label", "emotion_class", 
                    "severity_band", "gate_ok", "dispatch_time_s"]
    print(df_queue[display_cols].to_string())
    
    # Show detailed analysis for each call
    print("\n" + "=" * 80)
    print("DETAILED CALL ANALYSIS")
    print("=" * 80)
    processed_results = [process_call.process_call(call) for call in calls]
    for call, result in zip(calls, processed_results):
        process_call.print_call_details(call, result)
    
    # Calculate and display metrics
    metrics = evaluation.calculate_metrics(df)
    evaluation.print_metrics(metrics)
    
    # Generate visualizations
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)
    try:
        visualization.plot_all_visualizations(df)
    except Exception as e:
        print(f"Could not generate visualizations: {e}")
        print("This is optional and requires matplotlib.")
    
    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()

