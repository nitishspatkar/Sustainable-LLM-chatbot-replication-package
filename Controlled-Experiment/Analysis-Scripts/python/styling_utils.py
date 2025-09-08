#!/usr/bin/env python3
"""
Styling utilities for Controlled Experiment charts
Consistent with User-Survey styling standards

Author: Research Team
Date: 2024
"""

import matplotlib.pyplot as plt
import yaml
from pathlib import Path

class ChartStyler:
    """Chart styling utility for consistent visualization formatting."""
    
    def __init__(self, config_path="chart_styles.yaml"):
        """Initialize with styling configuration."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self):
        """Load styling configuration from YAML file."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            # Fallback configuration
            return {
                'font': {'family': 'Times New Roman', 'sizes': {'title': 56, 'xlabel': 52, 'ylabel': 52, 'legend': 36, 'tick_labels': 35}},
                'colors': {'modes': ['#2E8B57', '#FFD700', '#DC143C'], 'fallback': '#1f77b4'},
                'output': {'dpi': 300, 'facecolor': 'white', 'bbox_inches': 'tight'}
            }
    
    def setup_fonts(self):
        """Configure matplotlib fonts."""
        plt.rcParams['font.family'] = self.config['font']['family']
        plt.rcParams['font.size'] = self.config['font']['sizes']['tick_labels']
        
    def get_font_size(self, element):
        """Get font size for specific chart element."""
        return self.config['font']['sizes'].get(element, 35)
    
    def get_colors(self, color_scheme='modes'):
        """Get color scheme for charts."""
        return self.config['colors'].get(color_scheme, [self.config['colors']['fallback']])
    
    def get_figure_size(self, chart_type='base'):
        """Get figure size for specific chart type."""
        if chart_type == 'single':
            return (self.config['dimensions']['base_width'], self.config['dimensions']['single_chart_height'])
        elif chart_type == 'dual':
            return (self.config['dimensions']['base_width'], self.config['dimensions']['dual_chart_height'])
        elif chart_type == 'quad':
            return (self.config['dimensions']['base_width'], self.config['dimensions']['quad_chart_height'])
        else:
            return (self.config['dimensions']['base_width'], self.config['dimensions']['base_height'])
    
    def configure_subplot(self, fig, ax, chart_type='base'):
        """Configure subplot layout for maximum stretching."""
        layout = self.config['layout']['subplot_adjust']
        
        if chart_type == 'with_legend':
            fig.subplots_adjust(
                left=layout['left'],
                right=layout['right'],
                bottom=layout['bottom_with_legend'],
                top=layout['top_with_legend']
            )
        else:
            fig.subplots_adjust(
                left=layout['left'],
                right=layout['right'],
                bottom=layout['bottom'],
                top=layout['top']
            )
    
    def style_axes(self, ax, title, xlabel, ylabel, chart_type='base'):
        """Apply consistent styling to axes."""
        # Set title
        ax.set_title(title, fontsize=self.get_font_size('title'), fontweight='bold', pad=20)
        
        # Set labels
        ax.set_xlabel(xlabel, fontsize=self.get_font_size('xlabel'))
        ax.set_ylabel(ylabel, fontsize=self.get_font_size('ylabel'))
        
        # Style tick labels
        ax.tick_params(axis='x', labelsize=self.get_font_size('tick_labels'))
        ax.tick_params(axis='y', labelsize=self.get_font_size('tick_labels'))
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    def style_legend(self, ax, chart_type='base'):
        """Apply consistent legend styling."""
        legend_config = self.config['layout']['legend']
        
        if chart_type == 'top':
            ax.legend(
                loc=legend_config['position'],
                bbox_to_anchor=legend_config['bbox_anchor'],
                ncol=legend_config['ncol'],
                frameon=legend_config['frameon'],
                fancybox=legend_config['fancybox'],
                shadow=legend_config['shadow'],
                fontsize=self.get_font_size('legend')
            )
        else:
            ax.legend(
                fontsize=self.get_font_size('legend'),
                frameon=True,
                fancybox=True,
                shadow=True
            )
    
    def save_chart(self, fig, output_path, chart_type='base'):
        """Save chart with consistent output settings."""
        output_config = self.config['output']
        
        fig.savefig(
            output_path,
            dpi=output_config['dpi'],
            facecolor=output_config['facecolor'],
            bbox_inches=output_config['bbox_inches']
        )
    
    def create_bar_chart(self, data, labels, title, xlabel, ylabel, output_path, 
                        color_scheme='modes', chart_type='single'):
        """Create a styled bar chart."""
        self.setup_fonts()
        
        fig, ax = plt.subplots(figsize=self.get_figure_size(chart_type))
        
        colors = self.get_colors(color_scheme)
        bars = ax.bar(labels, data, color=colors[:len(labels)])
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                   f'{height:.3f}', ha='center', va='bottom', 
                   fontsize=self.get_font_size('bar_labels'))
        
        self.style_axes(ax, title, xlabel, ylabel, chart_type)
        self.configure_subplot(fig, ax, chart_type)
        self.save_chart(fig, output_path, chart_type)
        plt.close()
    
    def create_scatter_plot(self, x_data, y_data, labels, title, xlabel, ylabel, 
                           output_path, color_scheme='modes', chart_type='single'):
        """Create a styled scatter plot."""
        self.setup_fonts()
        
        fig, ax = plt.subplots(figsize=self.get_figure_size(chart_type))
        
        colors = self.get_colors(color_scheme)
        
        for i, (x, y, label) in enumerate(zip(x_data, y_data, labels)):
            ax.scatter(x, y, alpha=0.6, s=30, color=colors[i % len(colors)], label=label)
        
        self.style_axes(ax, title, xlabel, ylabel, chart_type)
        self.style_legend(ax)
        self.configure_subplot(fig, ax, chart_type)
        self.save_chart(fig, output_path, chart_type)
        plt.close()
    
    def create_multi_subplot(self, data_dict, titles, xlabels, ylabels, output_path, 
                           color_scheme='modes', chart_type='quad'):
        """Create a styled multi-subplot chart."""
        self.setup_fonts()
        
        fig, axes = plt.subplots(2, 2, figsize=self.get_figure_size(chart_type))
        axes = axes.flatten()
        
        colors = self.get_colors(color_scheme)
        
        for i, (key, data) in enumerate(data_dict.items()):
            if i < len(axes):
                ax = axes[i]
                
                if isinstance(data, dict) and 'x' in data and 'y' in data:
                    # Scatter plot data
                    ax.scatter(data['x'], data['y'], alpha=0.6, s=30, color=colors[i % len(colors)])
                elif isinstance(data, (list, tuple)) and len(data) == 2:
                    # Bar chart data
                    labels, values = data
                    bars = ax.bar(labels, values, color=colors[:len(labels)])
                    
                    # Add value labels
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                               f'{height:.2f}', ha='center', va='bottom', 
                               fontsize=self.get_font_size('bar_labels'))
                
                self.style_axes(ax, titles[i], xlabels[i], ylabels[i], chart_type)
        
        self.configure_subplot(fig, axes[0], chart_type)
        self.save_chart(fig, output_path, chart_type)
        plt.close()
