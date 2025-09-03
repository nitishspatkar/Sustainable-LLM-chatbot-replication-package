"""
Styling utilities for survey analyzer charts
Centralized styling configuration to eliminate code duplication
"""

import yaml
import matplotlib.pyplot as plt
import os

class ChartStyler:
    """Centralized chart styling management"""
    
    def __init__(self, config_path="config/chart_styles.yaml"):
        """Initialize with styling configuration"""
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        """Load styling configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Warning: Config file {self.config_path} not found. Using defaults.")
            return self._get_default_config()
    
    def _get_default_config(self):
        """Fallback default configuration"""
        return {
            'font': {
                'family': 'Times New Roman',
                'sizes': {
                    'title': 56, 'xlabel': 52, 'ylabel': 52, 'legend': 36,
                    'tick_labels': 35, 'y_axis_labels': 70, 'bar_labels': 34
                }
            },
            'colors': {
                'light_blue': ['#E3F2FD', '#BBDEFB', '#90CAF9', '#64B5F6', '#42A5F5'],
                'scientific': ['#1f77b4', '#ff7f0e', '#2ca02c'],
                'fallback': '#1f77b4'
            },
            'dimensions': {
                'base_width': 32, 'base_height': 24,
                'single_question_height': 8, 'two_question_height': 12, 'three_question_height': 16,
                'bar_height': {'single': 0.2, 'multi': 0.6, 'individual_in_multi': 0.3}
            },
            'layout': {
                'subplot_adjust': {
                    'left': 0.001, 'right': 0.999, 'bottom': 0.1, 'top': 0.95,
                    'bottom_with_legend': 0.2, 'top_with_legend': 0.85
                },
                'legend': {
                    'position': 'upper center', 'bbox_anchor': [0.5, -0.15], 'ncol': 5,
                    'frameon': True, 'fancybox': True, 'shadow': True
                }
            },
            'output': {'dpi': 300, 'facecolor': 'white', 'bbox_inches': 'tight'}
        }
    
    def setup_font(self):
        """Set up matplotlib font configuration"""
        plt.rcParams['font.family'] = self.config['font']['family']
    
    def get_font_size(self, element):
        """Get font size for specific chart element"""
        return self.config['font']['sizes'].get(element, 35)
    
    def get_colors(self, scheme='light_blue'):
        """Get color scheme"""
        return self.config['colors'].get(scheme, self.config['colors']['light_blue'])
    
    def get_figure_size(self, width_type='base', height_type='base'):
        """Get figure dimensions"""
        width = self.config['dimensions'].get(f'{width_type}_width', self.config['dimensions']['base_width'])
        height = self.config['dimensions'].get(f'{height_type}_height', self.config['dimensions']['base_height'])
        return width, height
    
    def get_bar_height(self, chart_type='single'):
        """Get bar height for different chart types"""
        return self.config['dimensions']['bar_height'].get(chart_type, 0.3)
    
    def apply_subplot_adjust(self, has_legend=False, legend_position='bottom'):
        """Apply subplot adjustments for maximum stretching"""
        adjust_config = self.config['layout']['subplot_adjust']
        
        if has_legend:
            if legend_position == 'bottom':
                plt.subplots_adjust(
                    left=adjust_config['left'],
                    right=adjust_config['right'],
                    bottom=adjust_config['bottom_with_legend'],
                    top=adjust_config['top']
                )
            else:  # top legend
                plt.subplots_adjust(
                    left=adjust_config['left'],
                    right=adjust_config['right'],
                    bottom=adjust_config['bottom'],
                    top=adjust_config['top_with_legend']
                )
        else:
            plt.subplots_adjust(
                left=adjust_config['left'],
                right=adjust_config['right'],
                bottom=adjust_config['bottom'],
                top=adjust_config['top']
            )
    
    def setup_legend(self, labels, position='upper center', ncol=None):
        """Set up legend with consistent styling"""
        legend_config = self.config['layout']['legend']
        
        if ncol is None:
            ncol = legend_config['ncol']
        
        plt.legend(
            labels,
            loc=position,
            bbox_to_anchor=legend_config['bbox_anchor'],
            ncol=ncol,
            fontsize=self.get_font_size('legend'),
            frameon=legend_config['frameon'],
            fancybox=legend_config['fancybox'],
            shadow=legend_config['shadow']
        )
    
    def save_chart(self, output_path):
        """Save chart with consistent output settings"""
        output_config = self.config['output']
        plt.savefig(
            output_path,
            dpi=output_config['dpi'],
            bbox_inches=output_config['bbox_inches'],
            facecolor=output_config['facecolor']
        )
        plt.close()
    
    def get_likert_labels(self, scale_type):
        """Get Likert scale labels for different question types"""
        likert_config = self.config.get('likert_scales', {})
        return likert_config.get(scale_type, likert_config.get('normalized', [
            '1 - Low', '2 - Below Average', '3 - Average', '4 - Above Average', '5 - High'
        ]))
    
    def create_figure(self, width_type='base', height_type='base'):
        """Create figure with consistent sizing"""
        width, height = self.get_figure_size(width_type, height_type)
        return plt.figure(figsize=(width, height))

# Global styler instance
styler = ChartStyler()
