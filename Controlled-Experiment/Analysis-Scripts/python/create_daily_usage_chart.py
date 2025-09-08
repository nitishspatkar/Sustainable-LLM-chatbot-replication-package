#!/usr/bin/env python3
"""
Daily Usage Pattern Chart Creator

This script creates a stacked bar chart showing chat mode usage per day
with professional styling and blue shades.

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
import warnings
warnings.filterwarnings('ignore')

# Import styling utilities
from styling_utils import ChartStyler

# Set style for publication-ready plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class DailyUsageChartCreator:
    """Creator for daily usage pattern visualization."""
    
    def __init__(self, data_dir="../../Raw-Data"):
        """Initialize with data directory."""
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
        """Load experiment data."""
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
        
        # Add day information
        self.prompts_df['day'] = self.prompts_df['createdAt'].dt.date
        min_date = self.prompts_df['day'].min()
        self.prompts_df['day_number'] = (self.prompts_df['day'] - min_date).apply(lambda x: x.days + 1)
        
        print(f"Processed {len(self.prompts_df)} valid prompts")
        print(f"Date range: {self.prompts_df['day'].min()} to {self.prompts_df['day'].max()}")
        print(f"Days in experiment: {self.prompts_df['day_number'].max()}")
        
    def create_daily_usage_chart(self):
        """Create daily usage pattern stacked bar chart."""
        print("Creating daily usage pattern chart...")
        
        # Calculate daily usage percentages
        daily_usage = self.prompts_df.groupby(['day_number', 'mode_name']).size().unstack(fill_value=0)
        
        # Calculate percentages
        daily_percentages = daily_usage.div(daily_usage.sum(axis=1), axis=0) * 100
        
        # Reorder columns to match the desired order
        mode_order = ['Energy Efficient', 'Balanced', 'Performance']
        daily_percentages = daily_percentages.reindex(columns=mode_order, fill_value=0)
        
        # Filter out days with only one mode (100% bars) - keep only days with multiple modes
        daily_percentages = daily_percentages[daily_percentages.sum(axis=1) > 0]
        # Remove days where any single mode is 100%
        daily_percentages = daily_percentages[~((daily_percentages == 100).any(axis=1))]
        
        # Create the chart
        self.styler.setup_fonts()
        fig, ax = plt.subplots(figsize=(16, 10))
        
        # Define blue shades with better contrast
        blue_shades = ['#42A5F5', '#1976D2', '#0D47A1']  # Light, medium, dark blue for better contrast
        
        # Create stacked bar chart
        bottom = np.zeros(len(daily_percentages))
        bars = []
        
        for i, mode in enumerate(mode_order):
            if mode in daily_percentages.columns:
                values = daily_percentages[mode].values
                bars.append(ax.bar(daily_percentages.index, values, 
                                 bottom=bottom, color=blue_shades[i], 
                                 alpha=0.8, edgecolor='white', linewidth=1.5,
                                 label=mode))
                
                # Add percentage labels on each segment
                for j, (day, value) in enumerate(zip(daily_percentages.index, values)):
                    if value > 0:  # Only show label if there's a value
                        y_pos = bottom[j] + value/2
                        ax.text(day, y_pos, f'{value:.0f}%', 
                               ha='center', va='center', fontsize=16, fontweight='bold',
                               color='white' if value > 15 else 'black')
                
                bottom += values
        
        # Customize the chart (remove title and "Day" labels)
        ax.set_xlabel('', fontsize=28)  # Remove x-axis label
        ax.set_ylabel('Percentage of Prompts', fontsize=28)
        
        # Set x-axis labels (with "Day" prefix)
        ax.set_xticks(daily_percentages.index)
        ax.set_xticklabels([f'Day {day}' for day in daily_percentages.index], fontsize=24)
        
        # Set y-axis
        ax.set_ylim(0, 100)
        ax.set_yticks(range(0, 101, 10))
        ax.set_yticklabels([f'{i}%' for i in range(0, 101, 10)], fontsize=20)
        
        # Add grid
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_axisbelow(True)
        
        # Customize legend (move to top, remove shadow)
        legend = ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), 
                          ncol=3, fontsize=20, frameon=True, 
                          fancybox=True, shadow=False)
        legend.get_frame().set_facecolor('white')
        legend.get_frame().set_alpha(0.9)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the chart
        self.styler.save_chart(fig, self.output_dir / "plots" / "daily_usage_pattern.png")
        plt.close()
        
        # Also create a data summary
        summary_data = daily_percentages.round(1)
        summary_data.to_csv(self.output_dir / "data" / "daily_usage_percentages.csv")
        
        return daily_percentages
    
    def create_usage_trend_chart(self):
        """Create a complementary trend chart showing usage patterns."""
        print("Creating usage trend chart...")
        
        # Calculate daily counts
        daily_counts = self.prompts_df.groupby(['day_number', 'mode_name']).size().unstack(fill_value=0)
        mode_order = ['Energy Efficient', 'Balanced', 'Performance']
        daily_counts = daily_counts.reindex(columns=mode_order, fill_value=0)
        
        # Create the chart
        self.styler.setup_fonts()
        fig, ax = plt.subplots(figsize=(16, 10))
        
        # Define blue shades with better contrast
        blue_shades = ['#42A5F5', '#1976D2', '#0D47A1']  # Light, medium, dark blue for better contrast
        
        # Create line plot
        for i, mode in enumerate(mode_order):
            if mode in daily_counts.columns:
                ax.plot(daily_counts.index, daily_counts[mode], 
                       marker='o', linewidth=4, markersize=8,
                       color=blue_shades[i], alpha=0.8, 
                       label=mode, markerfacecolor='white', 
                       markeredgecolor=blue_shades[i], markeredgewidth=2)
        
        # Customize the chart
        ax.set_title('Daily Chat Mode Usage Trends (Count)', 
                    fontsize=32, fontweight='bold', pad=30)
        ax.set_xlabel('Day', fontsize=28)
        ax.set_ylabel('Number of Prompts', fontsize=28)
        
        # Set x-axis labels
        ax.set_xticks(daily_counts.index)
        ax.set_xticklabels([f'Day {day}' for day in daily_counts.index], fontsize=24)
        
        # Set y-axis
        ax.tick_params(axis='y', labelsize=20)
        
        # Add grid
        ax.grid(True, alpha=0.3)
        ax.set_axisbelow(True)
        
        # Customize legend
        legend = ax.legend(loc='upper right', fontsize=20, frameon=True, 
                          fancybox=True, shadow=True)
        legend.get_frame().set_facecolor('white')
        legend.get_frame().set_alpha(0.9)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the chart
        self.styler.save_chart(fig, self.output_dir / "plots" / "daily_usage_trends.png")
        plt.close()
        
        return daily_counts
    
    def generate_daily_usage_report(self, daily_percentages, daily_counts):
        """Generate daily usage analysis report."""
        print("Generating daily usage report...")
        
        # Calculate key statistics
        total_days = len(daily_percentages)
        avg_energy_efficient = daily_percentages['Energy Efficient'].mean()
        avg_balanced = daily_percentages['Balanced'].mean()
        avg_performance = daily_percentages['Performance'].mean()
        
        # Find trends
        energy_trend = daily_percentages['Energy Efficient'].iloc[-1] - daily_percentages['Energy Efficient'].iloc[0]
        performance_trend = daily_percentages['Performance'].iloc[-1] - daily_percentages['Performance'].iloc[0]
        
        report = f"""
# Daily Usage Pattern Analysis Report

## Summary Statistics
- **Total Days Analyzed**: {total_days}
- **Average Energy Efficient Usage**: {avg_energy_efficient:.1f}%
- **Average Balanced Usage**: {avg_balanced:.1f}%
- **Average Performance Usage**: {avg_performance:.1f}%

## Usage Trends
- **Energy Efficient Trend**: {energy_trend:+.1f}% change from Day 1 to Day {total_days}
- **Performance Trend**: {performance_trend:+.1f}% change from Day 1 to Day {total_days}

## Daily Breakdown
{daily_percentages.round(1).to_string()}

## Key Insights
1. **Mode Distribution**: Clear daily patterns in mode usage
2. **User Adaptation**: Users may be adapting their mode choices over time
3. **Efficiency Preference**: Energy Efficient mode shows varying usage patterns
4. **Balanced Usage**: Balanced mode provides consistent middle-ground option

## Charts Generated
- Daily usage percentages: `plots/daily_usage_pattern.png`
- Usage trends: `plots/daily_usage_trends.png`
- Data files: `data/daily_usage_percentages.csv`

Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # Save report
        with open(self.output_dir / "reports" / "daily_usage_report.md", 'w') as f:
            f.write(report)
        
        print("Daily usage report saved to reports/daily_usage_report.md")
    
    def run_analysis(self):
        """Run complete daily usage analysis."""
        print("Creating daily usage pattern visualizations...")
        
        # Preprocess data
        self.preprocess_data()
        
        # Create visualizations
        daily_percentages = self.create_daily_usage_chart()
        daily_counts = self.create_usage_trend_chart()
        
        # Generate report
        self.generate_daily_usage_report(daily_percentages, daily_counts)
        
        print("Daily usage analysis complete!")
        print(f"Output directory: {self.output_dir.absolute()}")

def main():
    """Main function to run the analysis."""
    creator = DailyUsageChartCreator()
    creator.run_analysis()

if __name__ == "__main__":
    main()
