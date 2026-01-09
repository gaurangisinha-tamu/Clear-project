"""
Evaluation Module

This module provides functions for calculating evaluation metrics
for the emotion detection and triage system.
"""

import pandas as pd
from typing import Dict, Any


def calculate_metrics(df_results: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate evaluation metrics for the emotion detection and triage system.
    
    Args:
        df_results: DataFrame containing processed call results
        
    Returns:
        dict: Dictionary containing various evaluation metrics
    """
    metrics = {
        "total_calls": len(df_results),
        "avg_emotion_score": df_results["emotion_score"].mean(),
        "avg_triage_score": df_results["triage_score"].mean(),
        "gate_pass_rate": df_results["gate_ok"].sum() / len(df_results),
        "critical_calls": (df_results["triage_label"] == "CRITICAL").sum(),
        "high_priority_calls": (df_results["triage_label"].isin(["CRITICAL", "HIGH"])).sum(),
        "calls_with_ai_suggestions": (df_results["num_ai_suggestions"] > 0).sum(),
        "calls_with_calm_strategies": df_results["has_calm_strategies"].sum(),
    }
    
    # Distribution by emotion class
    emotion_dist = df_results["emotion_class"].value_counts().to_dict()
    metrics["emotion_distribution"] = emotion_dist
    
    # Distribution by severity band
    severity_dist = df_results["severity_band"].value_counts().to_dict()
    metrics["severity_distribution"] = severity_dist
    
    # Distribution by triage label
    triage_dist = df_results["triage_label"].value_counts().to_dict()
    metrics["triage_distribution"] = triage_dist
    
    return metrics


def print_metrics(metrics: Dict[str, Any]) -> None:
    """
    Print evaluation metrics in a formatted way.
    
    Args:
        metrics: Dictionary containing evaluation metrics
    """
    print("=" * 80)
    print("EVALUATION METRICS")
    print("=" * 80)
    print(f"\nTotal Calls Processed: {metrics['total_calls']}")
    print(f"\nAverage Emotion Score: {metrics['avg_emotion_score']:.2f}/5.0")
    print(f"Average Triage Score: {metrics['avg_triage_score']:.2f}/5.0")
    print(f"Policy Gate Pass Rate: {metrics['gate_pass_rate']:.1%}")
    print(f"\nCritical Calls: {metrics['critical_calls']}")
    print(f"High Priority Calls (Critical + High): {metrics['high_priority_calls']}")
    print(f"Calls with AI Suggestions: {metrics['calls_with_ai_suggestions']}")
    print(f"Calls Requiring Calm-Down Strategies: {metrics['calls_with_calm_strategies']}")
    print(f"\nEmotion Class Distribution:")
    for emotion, count in metrics['emotion_distribution'].items():
        print(f"  {emotion.capitalize()}: {count}")
    print(f"\nSeverity Band Distribution:")
    for band, count in metrics['severity_distribution'].items():
        print(f"  {band.capitalize()}: {count}")
    print(f"\nTriage Label Distribution:")
    for label, count in sorted(metrics['triage_distribution'].items(), 
                              key=lambda x: ["LOW", "MEDIUM", "HIGH", "CRITICAL"].index(x[0])):
        print(f"  {label}: {count}")
    print("=" * 80)


def get_accuracy_metrics(df_results: pd.DataFrame, 
                         ground_truth: pd.DataFrame = None) -> Dict[str, float]:
    """
    Calculate accuracy metrics if ground truth is available.
    
    Args:
        df_results: DataFrame containing predicted results
        ground_truth: Optional DataFrame containing ground truth labels
        
    Returns:
        dict: Dictionary containing accuracy metrics
    """
    if ground_truth is None:
        return {"note": "Ground truth not provided"}
    
    # Merge results with ground truth
    merged = df_results.merge(ground_truth, on="call_id", suffixes=("_pred", "_true"))
    
    metrics = {
        "emotion_accuracy": (merged["emotion_class_pred"] == merged["emotion_class_true"]).mean(),
        "triage_accuracy": (merged["triage_label_pred"] == merged["triage_label_true"]).mean(),
        "emotion_mae": (merged["emotion_score_pred"] - merged["emotion_score_true"]).abs().mean(),
        "triage_mae": (merged["triage_score_pred"] - merged["triage_score_true"]).abs().mean(),
    }
    
    return metrics

