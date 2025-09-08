#!/usr/bin/env python3
"""
User Behavior Analysis for Controlled Experiment

This script analyzes user behavior patterns, mode switching, and temporal usage
patterns in the controlled experiment study.

Author: Research Team
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import styling utilities
from styling_utils import ChartStyler

# Set style for publication-ready plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class UserBehaviorAnalyzer:
    """Analyzer for user behavior patterns in controlled experiment."""
    
    def __init__(self, data_dir="../../Raw-Data"):
        """Initialize analyzer with data directory."""
        self.data_dir = Path(data_dir)
        self.output_dir = Path("../output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Create output subdirectories
        (self.output_dir / "plots").mkdir(exist_ok=True)
        (self.output_dir / "data").mkdir(exist_ok=True)
        (self.output_dir / "reports").mkdir(exist_ok=True)
        
        # Initialize chart styler
        self.styler = ChartStyler()
        
        # Load data
        self.load_data()
        
    def load_data(self):
        """Load all experiment data from JSON files."""
        print("Loading experiment data...")
        
        # Load main data files
        self.users = self._load_json("Users.json")
        self.modes = self._load_json("Modes.json")
        self.prompts = self._load_json("Prompts.json")
        self.conversations = self._load_json("Conversations.json")
        
        # Convert to DataFrames
        self.users_df = pd.DataFrame(self.users)
        self.prompts_df = pd.DataFrame(self.prompts)
        self.conversations_df = pd.DataFrame(self.conversations)
        
        print(f"Loaded {len(self.users_df)} users, {len(self.prompts_df)} prompts, {len(self.conversations_df)} conversations")
        
    def _load_json(self, filename):
        """Load JSON file and return data."""
        filepath = self.data_dir / filename
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
        else:
            print(f"Warning: {filename} not found")
            return []
    
    def preprocess_data(self):
        """Preprocess and clean the data."""
        print("Preprocessing data...")
        
        # Convert timestamps
        self.prompts_df['createdAt'] = pd.to_datetime(self.prompts_df['createdAt'])
        self.prompts_df['sentAt'] = pd.to_datetime(self.prompts_df['sentAt'])
        
        # Extract usage data from nested dictionary
        if 'usage' in self.prompts_df.columns:
            usage_df = pd.json_normalize(self.prompts_df['usage'])
            self.prompts_df = pd.concat([self.prompts_df, usage_df], axis=1)
        
        # Convert numeric columns
        numeric_cols = ['numberOfInputTokens', 'numberOfOutputTokens', 'usageInWh']
        for col in numeric_cols:
            if col in self.prompts_df.columns:
                self.prompts_df[col] = pd.to_numeric(self.prompts_df[col], errors='coerce')
        
        # Filter valid prompts (isSent = True)
        if 'isSent' in self.prompts_df.columns:
            self.prompts_df = self.prompts_df[self.prompts_df['isSent'] == True]
        
        # Add mode names
        mode_mapping = {0: 'Energy Efficient', 1: 'Balanced', 2: 'Performance'}
        if 'chatMode' in self.prompts_df.columns:
            self.prompts_df['mode_name'] = self.prompts_df['chatMode'].map(mode_mapping)
        
        # Add time features
        self.prompts_df['hour'] = self.prompts_df['createdAt'].dt.hour
        self.prompts_df['day_of_week'] = self.prompts_df['createdAt'].dt.day_name()
        self.prompts_df['date'] = self.prompts_df['createdAt'].dt.date
        
        print(f"Processed {len(self.prompts_df)} valid prompts")
        
    def analyze_mode_switching(self):
        """Analyze user mode switching patterns."""
        print("Analyzing mode switching patterns...")
        
        # Group by user and analyze mode usage
        user_mode_analysis = self.prompts_df.groupby('userId').agg({
            'chatMode': ['count', 'nunique', lambda x: list(x)],
            'mode_name': lambda x: list(x)
        }).round(4)
        
        # Flatten column names
        user_mode_analysis.columns = ['total_prompts', 'modes_used', 'mode_sequence', 'mode_names']
        
        # Calculate mode switching frequency
        user_mode_analysis['mode_switches'] = user_mode_analysis['mode_sequence'].apply(
            lambda x: sum(1 for i in range(1, len(x)) if x[i] != x[i-1])
        )
        
        # Calculate mode diversity (entropy)
        def calculate_entropy(sequence):
            from collections import Counter
            counts = Counter(sequence)
            total = len(sequence)
            entropy = -sum((count/total) * np.log2(count/total) for count in counts.values())
            return entropy
        
        user_mode_analysis['mode_entropy'] = user_mode_analysis['mode_sequence'].apply(calculate_entropy)
        
        # Save analysis
        user_mode_analysis.to_csv(self.output_dir / "data" / "user_mode_switching_analysis.csv")
        
        return user_mode_analysis
    
    def analyze_temporal_patterns(self):
        """Analyze temporal usage patterns."""
        print("Analyzing temporal patterns...")
        
        # Daily usage patterns
        daily_usage = self.prompts_df.groupby('date').agg({
            'id': 'count',
            'usageInWh': 'sum',
            'numberOfInputTokens': 'sum',
            'numberOfOutputTokens': 'sum'
        }).reset_index()
        daily_usage.columns = ['date', 'prompts_count', 'total_energy', 'total_input_tokens', 'total_output_tokens']
        
        # Hourly usage patterns
        hourly_usage = self.prompts_df.groupby('hour').agg({
            'id': 'count',
            'usageInWh': 'mean',
            'chatMode': lambda x: x.mode().iloc[0] if len(x) > 0 else None
        }).reset_index()
        hourly_usage.columns = ['hour', 'prompts_count', 'avg_energy', 'most_common_mode']
        
        # Day of week patterns
        dow_usage = self.prompts_df.groupby('day_of_week').agg({
            'id': 'count',
            'usageInWh': 'mean',
            'chatMode': lambda x: x.mode().iloc[0] if len(x) > 0 else None
        }).reset_index()
        dow_usage.columns = ['day_of_week', 'prompts_count', 'avg_energy', 'most_common_mode']
        
        # Save analyses
        daily_usage.to_csv(self.output_dir / "data" / "daily_usage_patterns.csv", index=False)
        hourly_usage.to_csv(self.output_dir / "data" / "hourly_usage_patterns.csv", index=False)
        dow_usage.to_csv(self.output_dir / "data" / "day_of_week_patterns.csv", index=False)
        
        return daily_usage, hourly_usage, dow_usage
    
    def analyze_conversation_patterns(self):
        """Analyze conversation patterns and characteristics."""
        print("Analyzing conversation patterns...")
        
        # Group by conversation
        conversation_analysis = self.prompts_df.groupby('conversationId').agg({
            'id': 'count',
            'userId': 'first',
            'chatMode': 'first',
            'mode_name': 'first',
            'usageInWh': 'sum',
            'numberOfInputTokens': 'sum',
            'numberOfOutputTokens': 'sum',
            'createdAt': ['min', 'max']
        }).round(4)
        
        # Flatten column names
        conversation_analysis.columns = ['prompt_count', 'user_id', 'mode', 'mode_name', 
                                       'total_energy', 'total_input_tokens', 'total_output_tokens',
                                       'start_time', 'end_time']
        
        # Calculate conversation duration
        conversation_analysis['duration_minutes'] = (
            conversation_analysis['end_time'] - conversation_analysis['start_time']
        ).dt.total_seconds() / 60
        
        # Calculate conversation efficiency
        conversation_analysis['energy_per_prompt'] = (
            conversation_analysis['total_energy'] / conversation_analysis['prompt_count']
        )
        conversation_analysis['tokens_per_prompt'] = (
            (conversation_analysis['total_input_tokens'] + conversation_analysis['total_output_tokens']) 
            / conversation_analysis['prompt_count']
        )
        
        # Save analysis
        conversation_analysis.to_csv(self.output_dir / "data" / "conversation_patterns_analysis.csv")
        
        return conversation_analysis
    
    def create_mode_switching_chart(self):
        """Create mode switching visualization."""
        print("Creating mode switching chart...")
        
        # Get mode switching data
        user_mode_analysis = self.analyze_mode_switching()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Mode switches per user
        ax1.bar(range(len(user_mode_analysis)), user_mode_analysis['mode_switches'])
        ax1.set_title('Mode Switches per User', fontsize=14, fontweight='bold')
        ax1.set_xlabel('User Index', fontsize=12)
        ax1.set_ylabel('Number of Mode Switches', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # Mode entropy per user
        ax2.bar(range(len(user_mode_analysis)), user_mode_analysis['mode_entropy'])
        ax2.set_title('Mode Diversity (Entropy) per User', fontsize=14, fontweight='bold')
        ax2.set_xlabel('User Index', fontsize=12)
        ax2.set_ylabel('Mode Entropy', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "plots" / "mode_switching_patterns.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_temporal_charts(self):
        """Create temporal usage pattern charts."""
        print("Creating temporal pattern charts...")
        
        daily_usage, hourly_usage, dow_usage = self.analyze_temporal_patterns()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Daily usage over time
        ax1.plot(daily_usage['date'], daily_usage['prompts_count'], marker='o')
        ax1.set_title('Daily Prompt Count Over Time', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Date', fontsize=12)
        ax1.set_ylabel('Number of Prompts', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)
        
        # Hourly usage patterns
        ax2.bar(hourly_usage['hour'], hourly_usage['prompts_count'])
        ax2.set_title('Hourly Usage Patterns', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Hour of Day', fontsize=12)
        ax2.set_ylabel('Number of Prompts', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # Day of week patterns
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_usage_ordered = dow_usage.set_index('day_of_week').reindex(day_order).reset_index()
        ax3.bar(dow_usage_ordered['day_of_week'], dow_usage_ordered['prompts_count'])
        ax3.set_title('Day of Week Usage Patterns', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Day of Week', fontsize=12)
        ax3.set_ylabel('Number of Prompts', fontsize=12)
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
        
        # Energy consumption over time
        ax4.plot(daily_usage['date'], daily_usage['total_energy'], marker='o', color='red')
        ax4.set_title('Daily Energy Consumption Over Time', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Date', fontsize=12)
        ax4.set_ylabel('Total Energy (Wh)', fontsize=12)
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "plots" / "temporal_usage_patterns.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_conversation_analysis_chart(self):
        """Create conversation analysis visualization."""
        print("Creating conversation analysis chart...")
        
        conversation_analysis = self.analyze_conversation_patterns()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Conversation length distribution
        ax1.hist(conversation_analysis['prompt_count'], bins=20, alpha=0.7)
        ax1.set_title('Conversation Length Distribution', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Number of Prompts per Conversation', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # Conversation duration distribution
        ax2.hist(conversation_analysis['duration_minutes'], bins=20, alpha=0.7, color='orange')
        ax2.set_title('Conversation Duration Distribution', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Duration (minutes)', fontsize=12)
        ax2.set_ylabel('Frequency', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # Energy per prompt by mode
        mode_energy = conversation_analysis.groupby('mode_name')['energy_per_prompt'].mean()
        ax3.bar(mode_energy.index, mode_energy.values, color=['#2E8B57', '#FFD700', '#DC143C'])
        ax3.set_title('Average Energy per Prompt by Mode', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Chat Mode', fontsize=12)
        ax3.set_ylabel('Energy per Prompt (Wh)', fontsize=12)
        ax3.grid(True, alpha=0.3)
        
        # Tokens per prompt by mode
        mode_tokens = conversation_analysis.groupby('mode_name')['tokens_per_prompt'].mean()
        ax4.bar(mode_tokens.index, mode_tokens.values, color=['#2E8B57', '#FFD700', '#DC143C'])
        ax4.set_title('Average Tokens per Prompt by Mode', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Chat Mode', fontsize=12)
        ax4.set_ylabel('Tokens per Prompt', fontsize=12)
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "plots" / "conversation_analysis.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
    def generate_behavior_report(self):
        """Generate user behavior analysis report."""
        print("Generating behavior analysis report...")
        
        # Get analysis results
        user_mode_analysis = self.analyze_mode_switching()
        daily_usage, hourly_usage, dow_usage = self.analyze_temporal_patterns()
        conversation_analysis = self.analyze_conversation_patterns()
        
        # Calculate key metrics
        total_users = len(user_mode_analysis)
        avg_mode_switches = user_mode_analysis['mode_switches'].mean()
        avg_mode_entropy = user_mode_analysis['mode_entropy'].mean()
        total_conversations = len(conversation_analysis)
        avg_conversation_length = conversation_analysis['prompt_count'].mean()
        
        # Create report
        report = f"""
# User Behavior Analysis Report

## Summary Statistics
- Total Users: {total_users}
- Total Conversations: {total_conversations}
- Average Mode Switches per User: {avg_mode_switches:.2f}
- Average Mode Diversity (Entropy): {avg_mode_entropy:.3f}
- Average Conversation Length: {avg_conversation_length:.1f} prompts

## Mode Switching Analysis
- Users with multiple modes: {len(user_mode_analysis[user_mode_analysis['modes_used'] > 1])}
- Most active mode switcher: {user_mode_analysis['mode_switches'].max()} switches
- Average modes used per user: {user_mode_analysis['modes_used'].mean():.1f}

## Temporal Patterns
- Peak usage hour: {hourly_usage.loc[hourly_usage['prompts_count'].idxmax(), 'hour']}:00
- Most active day: {dow_usage.loc[dow_usage['prompts_count'].idxmax(), 'day_of_week']}
- Total experiment duration: {(self.prompts_df['createdAt'].max() - self.prompts_df['createdAt'].min()).days} days

## Conversation Characteristics
- Average conversation duration: {conversation_analysis['duration_minutes'].mean():.1f} minutes
- Longest conversation: {conversation_analysis['prompt_count'].max()} prompts
- Shortest conversation: {conversation_analysis['prompt_count'].min()} prompts

## Key Insights
1. **Mode Adaptation**: Users show varying levels of mode switching behavior
2. **Temporal Patterns**: Clear usage patterns emerge based on time of day and day of week
3. **Conversation Dynamics**: Conversation length and duration vary significantly
4. **User Engagement**: Different users show different engagement patterns

## Files Generated
- Mode switching analysis: `plots/mode_switching_patterns.png`
- Temporal patterns: `plots/temporal_usage_patterns.png`
- Conversation analysis: `plots/conversation_analysis.png`
- Data files: Various CSV files in `data/` directory

Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # Save report
        with open(self.output_dir / "reports" / "user_behavior_report.md", 'w') as f:
            f.write(report)
        
        print("Behavior analysis report saved to reports/user_behavior_report.md")
        
    def run_analysis(self):
        """Run complete user behavior analysis."""
        print("Starting user behavior analysis...")
        
        # Preprocess data
        self.preprocess_data()
        
        # Run analyses
        self.analyze_mode_switching()
        self.analyze_temporal_patterns()
        self.analyze_conversation_patterns()
        
        # Create visualizations
        self.create_mode_switching_chart()
        self.create_temporal_charts()
        self.create_conversation_analysis_chart()
        
        # Generate report
        self.generate_behavior_report()
        
        print("User behavior analysis complete! Check the output directory for results.")
        print(f"Output directory: {self.output_dir.absolute()}")

def main():
    """Main function to run the analysis."""
    analyzer = UserBehaviorAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()
