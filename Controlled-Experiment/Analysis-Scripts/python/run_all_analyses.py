#!/usr/bin/env python3
"""
Complete Analysis Pipeline for Controlled Experiment

This script runs all analysis modules for the controlled experiment study.

Author: Research Team
Date: 2024
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from analyze_energy_consumption import EnergyConsumptionAnalyzer
from analyze_user_behavior import UserBehaviorAnalyzer
from analyze_performance_tradeoffs import PerformanceTradeoffAnalyzer

def main():
    """Run all analyses for the controlled experiment."""
    print("=" * 60)
    print("CONTROLLED EXPERIMENT - COMPLETE ANALYSIS PIPELINE")
    print("=" * 60)
    
    # Run energy consumption analysis
    print("\n1. Running Energy Consumption Analysis...")
    print("-" * 40)
    energy_analyzer = EnergyConsumptionAnalyzer()
    energy_analyzer.run_analysis()
    
    # Run user behavior analysis
    print("\n2. Running User Behavior Analysis...")
    print("-" * 40)
    behavior_analyzer = UserBehaviorAnalyzer()
    behavior_analyzer.run_analysis()
    
    # Run performance trade-offs analysis
    print("\n3. Running Performance Trade-offs Analysis...")
    print("-" * 40)
    tradeoff_analyzer = PerformanceTradeoffAnalyzer()
    tradeoff_analyzer.run_analysis()
    
    print("\n" + "=" * 60)
    print("ALL ANALYSES COMPLETE!")
    print("=" * 60)
    print("\nGenerated outputs:")
    print("- Energy consumption charts and analysis")
    print("- User behavior patterns and temporal analysis")
    print("- Performance vs. efficiency trade-offs")
    print("- Statistical reports and data files")
    print("\nCheck the output directory for all results.")

if __name__ == "__main__":
    main()
