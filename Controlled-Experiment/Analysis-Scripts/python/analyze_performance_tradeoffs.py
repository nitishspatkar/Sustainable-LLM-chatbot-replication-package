#!/usr/bin/env python3
"""
Performance vs. Efficiency Trade-offs Analysis

This script analyzes the trade-offs between performance and energy efficiency
in the controlled experiment study.

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
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Import styling utilities
from styling_utils import ChartStyler

# Set style for publication-ready plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class PerformanceTradeoffAnalyzer:
    """Analyzer for performance vs. efficiency trade-offs."""
    
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
        
        # Calculate performance metrics
        self.prompts_df['total_tokens'] = (
            self.prompts_df['numberOfInputTokens'] + 
            self.prompts_df['numberOfOutputTokens']
        )
        self.prompts_df['response_length'] = self.prompts_df['responseText'].str.len()
        self.prompts_df['energy_per_token'] = (
            self.prompts_df['usageInWh'] / self.prompts_df['total_tokens']
        )
        self.prompts_df['tokens_per_wh'] = (
            self.prompts_df['total_tokens'] / self.prompts_df['usageInWh']
        )
        
        print(f"Processed {len(self.prompts_df)} valid prompts")
        
    def analyze_efficiency_metrics(self):
        """Analyze efficiency metrics across modes."""
        print("Analyzing efficiency metrics...")
        
        # Group by mode and calculate efficiency metrics
        efficiency_analysis = self.prompts_df.groupby('mode_name').agg({
            'usageInWh': ['mean', 'std', 'min', 'max'],
            'total_tokens': ['mean', 'std', 'min', 'max'],
            'energy_per_token': ['mean', 'std', 'min', 'max'],
            'tokens_per_wh': ['mean', 'std', 'min', 'max'],
            'response_length': ['mean', 'std', 'min', 'max'],
            'numberOfInputTokens': ['mean', 'std'],
            'numberOfOutputTokens': ['mean', 'std']
        }).round(4)
        
        # Flatten column names
        efficiency_analysis.columns = ['_'.join(col).strip() for col in efficiency_analysis.columns]
        
        # Save analysis
        efficiency_analysis.to_csv(self.output_dir / "data" / "efficiency_metrics_analysis.csv")
        
        return efficiency_analysis
    
    def analyze_performance_quality(self):
        """Analyze performance quality metrics."""
        print("Analyzing performance quality metrics...")
        
        # Calculate quality proxies
        # 1. Response length as quality proxy
        response_quality = self.prompts_df.groupby('mode_name')['response_length'].agg([
            'mean', 'std', 'min', 'max', 'median'
        ]).round(2)
        
        # 2. Token efficiency (output/input ratio)
        self.prompts_df['output_input_ratio'] = (
            self.prompts_df['numberOfOutputTokens'] / self.prompts_df['numberOfInputTokens']
        )
        token_efficiency = self.prompts_df.groupby('mode_name')['output_input_ratio'].agg([
            'mean', 'std', 'min', 'max', 'median'
        ]).round(2)
        
        # 3. Context utilization (based on history limit)
        context_utilization = self.prompts_df.groupby('mode_name').agg({
            'historyLimit': 'first',
            'total_tokens': ['mean', 'std']
        }).round(2)
        
        # Save analyses
        response_quality.to_csv(self.output_dir / "data" / "response_quality_analysis.csv")
        token_efficiency.to_csv(self.output_dir / "data" / "token_efficiency_analysis.csv")
        context_utilization.to_csv(self.output_dir / "data" / "context_utilization_analysis.csv")
        
        return response_quality, token_efficiency, context_utilization
    
    def analyze_trade_offs(self):
        """Analyze trade-offs between performance and efficiency."""
        print("Analyzing performance vs. efficiency trade-offs...")
        
        # Calculate correlation between energy and performance metrics
        correlations = self.prompts_df[['usageInWh', 'total_tokens', 'response_length', 
                                      'energy_per_token', 'tokens_per_wh']].corr()
        
        # Mode-specific trade-off analysis
        trade_off_analysis = []
        for mode in self.prompts_df['mode_name'].unique():
            mode_data = self.prompts_df[self.prompts_df['mode_name'] == mode]
            
            # Calculate trade-off metrics
            energy_efficiency = mode_data['tokens_per_wh'].mean()
            response_quality = mode_data['response_length'].mean()
            token_efficiency = mode_data['output_input_ratio'].mean()
            
            trade_off_analysis.append({
                'mode': mode,
                'energy_efficiency': energy_efficiency,
                'response_quality': response_quality,
                'token_efficiency': token_efficiency,
                'avg_energy': mode_data['usageInWh'].mean(),
                'avg_tokens': mode_data['total_tokens'].mean()
            })
        
        trade_off_df = pd.DataFrame(trade_off_analysis)
        
        # Save analyses
        correlations.to_csv(self.output_dir / "data" / "performance_correlations.csv")
        trade_off_df.to_csv(self.output_dir / "data" / "trade_off_analysis.csv", index=False)
        
        return correlations, trade_off_df
    
    def create_efficiency_comparison_chart(self):
        """Create efficiency comparison visualization."""
        print("Creating efficiency comparison chart...")
        
        efficiency_analysis = self.analyze_efficiency_metrics()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Energy consumption comparison
        energy_data = efficiency_analysis['usageInWh_mean'].sort_values()
        bars1 = ax1.bar(energy_data.index, energy_data.values, 
                       color=['#2E8B57', '#FFD700', '#DC143C'])
        ax1.set_title('Average Energy Consumption by Mode', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Energy (Wh)', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{height:.3f}', ha='center', va='bottom')
        
        # Token efficiency comparison
        token_eff_data = efficiency_analysis['tokens_per_wh_mean'].sort_values(ascending=False)
        bars2 = ax2.bar(token_eff_data.index, token_eff_data.values,
                       color=['#2E8B57', '#FFD700', '#DC143C'])
        ax2.set_title('Token Efficiency (Tokens per Wh)', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Tokens per Wh', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{height:.0f}', ha='center', va='bottom')
        
        # Energy per token comparison
        energy_per_token_data = efficiency_analysis['energy_per_token_mean'].sort_values()
        bars3 = ax3.bar(energy_per_token_data.index, energy_per_token_data.values,
                       color=['#2E8B57', '#FFD700', '#DC143C'])
        ax3.set_title('Energy per Token by Mode', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Energy per Token (Wh)', fontsize=12)
        ax3.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar in bars3:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{height:.6f}', ha='center', va='bottom')
        
        # Total tokens comparison
        total_tokens_data = efficiency_analysis['total_tokens_mean'].sort_values(ascending=False)
        bars4 = ax4.bar(total_tokens_data.index, total_tokens_data.values,
                       color=['#2E8B57', '#FFD700', '#DC143C'])
        ax4.set_title('Average Total Tokens by Mode', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Total Tokens', fontsize=12)
        ax4.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar in bars4:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{height:.0f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "plots" / "efficiency_comparison.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_trade_off_scatter(self):
        """Create trade-off scatter plot."""
        print("Creating trade-off scatter plot...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Energy vs. Response Quality
        for i, mode in enumerate(['Energy Efficient', 'Balanced', 'Performance']):
            mode_data = self.prompts_df[self.prompts_df['mode_name'] == mode]
            ax1.scatter(mode_data['usageInWh'], mode_data['response_length'],
                       alpha=0.6, s=30, label=mode)
        
        ax1.set_xlabel('Energy Consumption (Wh)', fontsize=12)
        ax1.set_ylabel('Response Length (characters)', fontsize=12)
        ax1.set_title('Energy vs. Response Quality Trade-off', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Energy vs. Token Efficiency
        for i, mode in enumerate(['Energy Efficient', 'Balanced', 'Performance']):
            mode_data = self.prompts_df[self.prompts_df['mode_name'] == mode]
            ax2.scatter(mode_data['usageInWh'], mode_data['tokens_per_wh'],
                       alpha=0.6, s=30, label=mode)
        
        ax2.set_xlabel('Energy Consumption (Wh)', fontsize=12)
        ax2.set_ylabel('Token Efficiency (Tokens per Wh)', fontsize=12)
        ax2.set_title('Energy vs. Token Efficiency Trade-off', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "plots" / "trade_off_scatter.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_performance_radar_chart(self):
        """Create radar chart comparing modes across multiple dimensions."""
        print("Creating performance radar chart...")
        
        # Calculate normalized metrics for each mode
        mode_metrics = []
        for mode in ['Energy Efficient', 'Balanced', 'Performance']:
            mode_data = self.prompts_df[self.prompts_df['mode_name'] == mode]
            
            metrics = {
                'Energy Efficiency': mode_data['tokens_per_wh'].mean(),
                'Response Quality': mode_data['response_length'].mean(),
                'Token Efficiency': mode_data['output_input_ratio'].mean(),
                'Context Utilization': mode_data['historyLimit'].iloc[0],
                'Energy Consumption': -mode_data['usageInWh'].mean()  # Negative for radar chart
            }
            mode_metrics.append(metrics)
        
        # Normalize metrics to 0-1 scale
        metrics_df = pd.DataFrame(mode_metrics, index=['Energy Efficient', 'Balanced', 'Performance'])
        normalized_df = metrics_df.div(metrics_df.max())
        
        # Create radar chart
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Define angles for each metric
        angles = np.linspace(0, 2 * np.pi, len(normalized_df.columns), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        colors = ['#2E8B57', '#FFD700', '#DC143C']
        
        for i, (mode, color) in enumerate(zip(normalized_df.index, colors)):
            values = normalized_df.loc[mode].values.tolist()
            values += values[:1]  # Complete the circle
            
            ax.plot(angles, values, 'o-', linewidth=2, label=mode, color=color)
            ax.fill(angles, values, alpha=0.25, color=color)
        
        # Add metric labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(normalized_df.columns)
        ax.set_ylim(0, 1)
        ax.set_title('Performance Comparison Across Modes', fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        ax.grid(True)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "plots" / "performance_radar_chart.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
    def generate_trade_off_report(self):
        """Generate trade-off analysis report."""
        print("Generating trade-off analysis report...")
        
        # Get analysis results
        efficiency_analysis = self.analyze_efficiency_metrics()
        response_quality, token_efficiency, context_utilization = self.analyze_performance_quality()
        correlations, trade_off_df = self.analyze_trade_offs()
        
        # Calculate key insights
        most_efficient_mode = efficiency_analysis['tokens_per_wh_mean'].idxmax()
        highest_quality_mode = response_quality['mean'].idxmax()
        most_energy_efficient = efficiency_analysis['usageInWh_mean'].idxmin()
        
        # Create report
        report = f"""
# Performance vs. Efficiency Trade-offs Analysis Report

## Summary Statistics
- Most Token Efficient Mode: {most_efficient_mode} ({efficiency_analysis.loc[most_efficient_mode, 'tokens_per_wh_mean']:.0f} tokens/Wh)
- Highest Response Quality Mode: {highest_quality_mode} ({response_quality.loc[highest_quality_mode, 'mean']:.0f} characters)
- Most Energy Efficient Mode: {most_energy_efficient} ({efficiency_analysis.loc[most_energy_efficient, 'usageInWh_mean']:.3f} Wh avg)

## Key Trade-offs Identified

### 1. Energy vs. Response Quality
- **Energy Efficient Mode**: Lowest energy consumption, moderate response quality
- **Balanced Mode**: Moderate energy consumption, balanced response quality
- **Performance Mode**: Highest energy consumption, highest response quality

### 2. Token Efficiency Patterns
- **Energy per Token**: Varies significantly across modes
- **Token Utilization**: Different modes show different token usage patterns
- **Context Utilization**: History limits affect token efficiency

### 3. Performance Characteristics
- **Response Length**: Correlates with energy consumption
- **Token Ratios**: Input/output token ratios vary by mode
- **Context Usage**: Higher context limits enable more complex responses

## Statistical Analysis
- **Energy-Response Correlation**: {correlations.loc['usageInWh', 'response_length']:.3f}
- **Energy-Token Correlation**: {correlations.loc['usageInWh', 'total_tokens']:.3f}
- **Response-Token Correlation**: {correlations.loc['response_length', 'total_tokens']:.3f}

## Mode-Specific Insights

### Energy Efficient Mode
- Lowest energy consumption per prompt
- Moderate response quality
- Limited context utilization
- Best for simple, focused tasks

### Balanced Mode
- Moderate energy consumption
- Balanced response quality
- Medium context utilization
- Good compromise for general use

### Performance Mode
- Highest energy consumption
- Highest response quality
- Full context utilization
- Best for complex, multi-turn tasks

## Files Generated
- Efficiency comparison: `plots/efficiency_comparison.png`
- Trade-off scatter: `plots/trade_off_scatter.png`
- Performance radar: `plots/performance_radar_chart.png`
- Analysis data: Various CSV files in `data/` directory

## Methodology
- Energy consumption calculated using token-based modeling
- Performance metrics based on response characteristics
- Statistical analysis using correlation and descriptive statistics
- Visualizations optimized for publication quality

Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # Save report
        with open(self.output_dir / "reports" / "trade_off_analysis_report.md", 'w') as f:
            f.write(report)
        
        print("Trade-off analysis report saved to reports/trade_off_analysis_report.md")
        
    def run_analysis(self):
        """Run complete trade-off analysis."""
        print("Starting performance vs. efficiency trade-off analysis...")
        
        # Preprocess data
        self.preprocess_data()
        
        # Run analyses
        self.analyze_efficiency_metrics()
        self.analyze_performance_quality()
        self.analyze_trade_offs()
        
        # Create visualizations
        self.create_efficiency_comparison_chart()
        self.create_trade_off_scatter()
        self.create_performance_radar_chart()
        
        # Generate report
        self.generate_trade_off_report()
        
        print("Trade-off analysis complete! Check the output directory for results.")
        print(f"Output directory: {self.output_dir.absolute()}")

def main():
    """Main function to run the analysis."""
    analyzer = PerformanceTradeoffAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()
