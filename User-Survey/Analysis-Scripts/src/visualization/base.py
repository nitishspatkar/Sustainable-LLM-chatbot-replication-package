"""
Base chart class for survey analyzer
Provides common functionality for all chart types
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.styling import styler
from utils.file_manager import output_manager

class BaseChart:
    """Base class for all chart types"""
    
    def __init__(self, config=None):
        """Initialize base chart"""
        self.config = config or {}
        self.styler = styler
        self.output_manager = output_manager
    
    def setup_figure(self, width_type='base', height_type='base'):
        """Set up figure with consistent styling"""
        self.styler.setup_font()
        fig = self.styler.create_figure(width_type, height_type)
        return fig
    
    def apply_common_styling(self, xlabel=None, ylabel=None, title=None, 
                           xlim=None, ylim=None, has_legend=False, legend_position='bottom'):
        """Apply common styling elements"""
        
        # Set labels
        if xlabel:
            plt.xlabel(xlabel, fontsize=self.styler.get_font_size('xlabel'), fontweight='bold')
        if ylabel:
            plt.ylabel(ylabel, fontsize=self.styler.get_font_size('ylabel'), fontweight='bold')
        if title:
            plt.title(title, fontsize=self.styler.get_font_size('title'), fontweight='bold', pad=20)
        
        # Set limits
        if xlim:
            plt.xlim(xlim)
        if ylim:
            plt.ylim(ylim)
        
        # Set tick font sizes
        plt.xticks(fontsize=self.styler.get_font_size('tick_labels'))
        plt.yticks(fontsize=self.styler.get_font_size('tick_labels'))
        
        # Apply subplot adjustments
        self.styler.apply_subplot_adjust(has_legend, legend_position)
    
    def add_percentage_labels(self, bars, values, min_threshold=3):
        """Add percentage labels to bars"""
        for bar, value in zip(bars, values):
            if value > min_threshold:
                plt.text(
                    bar.get_x() + bar.get_width()/2,
                    bar.get_y() + bar.get_height()/2,
                    f'{value:.1f}%',
                    ha='center', va='center',
                    fontsize=self.styler.get_font_size('bar_labels'),
                    fontweight='bold',
                    color='black'
                )
    
    def save_chart(self, output_path):
        """Save chart with consistent settings"""
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save chart
        self.styler.save_chart(output_path)
        
        # Track file creation
        self.output_manager.track_file_creation(
            output_path, 
            'chart', 
            f"Chart saved to {output_path}"
        )
        
        print(f"Created visualization: {output_path}")
    
    def get_colors(self, scheme='light_blue', n_colors=None):
        """Get color scheme"""
        colors = self.styler.get_colors(scheme)
        if n_colors and len(colors) > n_colors:
            return colors[:n_colors]
        return colors
    
    def get_likert_labels(self, scale_type):
        """Get Likert scale labels"""
        return self.styler.get_likert_labels(scale_type)
    
    def create(self, data, title, output_path, **kwargs):
        """Create chart - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement create method")

class HorizontalBarChart(BaseChart):
    """Horizontal bar chart implementation"""
    
    def create(self, data, title, output_path, **kwargs):
        """Create horizontal bar chart"""
        self.setup_figure()
        
        # Sort data in ascending order (longest bar on top)
        data_sorted = data.sort_values(ascending=True)
        
        # Create horizontal bar chart
        colors = self.get_colors('light_blue', len(data_sorted))
        bars = plt.barh(range(len(data_sorted)), data_sorted.values, color=colors)
        
        # Add percentage labels
        self.add_percentage_labels(bars, data_sorted.values)
        
        # Apply styling
        self.apply_common_styling(
            xlabel='Count',
            ylabel='Response Options',
            title=title
        )
        
        # Set y-axis labels
        plt.yticks(range(len(data_sorted)), data_sorted.index, 
                  fontsize=self.styler.get_font_size('y_axis_labels'))
        
        # Save chart
        self.save_chart(output_path)

class LikertScaleChart(BaseChart):
    """Likert scale chart implementation"""
    
    def create(self, data, title, output_path, scale_type='normalized', **kwargs):
        """Create Likert scale chart"""
        self.setup_figure()
        
        # Get Likert labels
        likert_labels = self.get_likert_labels(scale_type)
        
        # Create horizontal bar chart
        colors = self.get_colors('light_blue', len(data))
        bars = plt.barh(range(len(data)), data.values, color=colors)
        
        # Add percentage labels
        self.add_percentage_labels(bars, data.values)
        
        # Apply styling
        self.apply_common_styling(
            xlabel='Count',
            ylabel='Response Options',
            title=title
        )
        
        # Set y-axis labels
        plt.yticks(range(len(data)), data.index, 
                  fontsize=self.styler.get_font_size('y_axis_labels'))
        
        # Save chart
        self.save_chart(output_path)
