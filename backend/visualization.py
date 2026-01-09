"""
Visualization Module

This module provides functions for visualizing emotion detection and triage results.
"""

import pandas as pd
from typing import Optional


def plot_emotion_distribution(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """
    Plot emotion score distribution.
    
    Args:
        df: DataFrame containing emotion scores
        save_path: Optional path to save the plot
    """
    try:
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        plt.hist(df["emotion_score"], bins=10, color='skyblue', edgecolor='black')
        plt.xlabel('Emotion Score')
        plt.ylabel('Number of Calls')
        plt.title('Emotion Score Distribution')
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
    except ImportError:
        print("Matplotlib not available. Skipping visualization.")


def plot_triage_distribution(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """
    Plot triage score distribution.
    
    Args:
        df: DataFrame containing triage scores
        save_path: Optional path to save the plot
    """
    try:
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        plt.hist(df["triage_score"], bins=10, color='coral', edgecolor='black')
        plt.xlabel('Triage Score')
        plt.ylabel('Number of Calls')
        plt.title('Triage Score Distribution')
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
    except ImportError:
        print("Matplotlib not available. Skipping visualization.")


def plot_emotion_vs_triage(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """
    Plot emotion score vs triage score scatter plot.
    
    Args:
        df: DataFrame containing emotion and triage scores
        save_path: Optional path to save the plot
    """
    try:
        import matplotlib.pyplot as plt
        
        colors_map = {'CRITICAL': 'red', 'HIGH': 'orange', 'MEDIUM': 'yellow', 'LOW': 'green'}
        
        plt.figure(figsize=(10, 6))
        for label in df["triage_label"].unique():
            mask = df["triage_label"] == label
            plt.scatter(df[mask]["emotion_score"], df[mask]["triage_score"], 
                       label=label, color=colors_map.get(label, 'gray'), s=100, alpha=0.7)
        
        plt.xlabel('Emotion Score')
        plt.ylabel('Triage Score')
        plt.title('Emotion Score vs Triage Score')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
    except ImportError:
        print("Matplotlib not available. Skipping visualization.")


def plot_triage_labels(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """
    Plot bar chart of calls by triage label.
    
    Args:
        df: DataFrame containing triage labels
        save_path: Optional path to save the plot
    """
    try:
        import matplotlib.pyplot as plt
        
        triage_counts = df["triage_label"].value_counts()
        labels_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
        counts = [triage_counts.get(label, 0) for label in labels_order]
        colors = ['red', 'orange', 'yellow', 'green']
        
        plt.figure(figsize=(10, 6))
        plt.bar(labels_order, counts, color=colors, edgecolor='black')
        plt.ylabel('Number of Calls')
        plt.title('Calls by Triage Label')
        plt.grid(True, alpha=0.3, axis='y')
        
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
    except ImportError:
        print("Matplotlib not available. Skipping visualization.")


def plot_all_visualizations(df: pd.DataFrame, save_dir: Optional[str] = None) -> None:
    """
    Plot all visualizations in a 2x2 grid.
    
    Args:
        df: DataFrame containing all results
        save_dir: Optional directory to save plots
    """
    try:
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. Emotion Score Distribution
        axes[0, 0].hist(df["emotion_score"], bins=10, color='skyblue', edgecolor='black')
        axes[0, 0].set_xlabel('Emotion Score')
        axes[0, 0].set_ylabel('Number of Calls')
        axes[0, 0].set_title('Emotion Score Distribution')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Triage Score Distribution
        axes[0, 1].hist(df["triage_score"], bins=10, color='coral', edgecolor='black')
        axes[0, 1].set_xlabel('Triage Score')
        axes[0, 1].set_ylabel('Number of Calls')
        axes[0, 1].set_title('Triage Score Distribution')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Emotion vs Triage Score Scatter
        colors_map = {'CRITICAL': 'red', 'HIGH': 'orange', 'MEDIUM': 'yellow', 'LOW': 'green'}
        for label in df["triage_label"].unique():
            mask = df["triage_label"] == label
            axes[1, 0].scatter(df[mask]["emotion_score"], df[mask]["triage_score"], 
                              label=label, color=colors_map.get(label, 'gray'), s=100, alpha=0.7)
        axes[1, 0].set_xlabel('Emotion Score')
        axes[1, 0].set_ylabel('Triage Score')
        axes[1, 0].set_title('Emotion Score vs Triage Score')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Triage Label Count
        triage_counts = df["triage_label"].value_counts()
        labels_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
        counts = [triage_counts.get(label, 0) for label in labels_order]
        axes[1, 1].bar(labels_order, counts, color=['red', 'orange', 'yellow', 'green'], edgecolor='black')
        axes[1, 1].set_ylabel('Number of Calls')
        axes[1, 1].set_title('Calls by Triage Label')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_dir:
            plt.savefig(f"{save_dir}/all_visualizations.png")
        else:
            plt.show()
            
    except ImportError:
        print("Matplotlib not available. Skipping visualizations.")
        print("To install: pip install matplotlib")

