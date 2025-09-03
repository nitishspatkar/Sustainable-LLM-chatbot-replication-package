"""
Configuration loading utilities for survey analyzer
Handles loading and validation of YAML configuration files
"""

import yaml
import os
from pathlib import Path

class ConfigLoader:
    """Loads and manages configuration files"""
    
    def __init__(self, config_dir="config"):
        """Initialize config loader"""
        self.config_dir = Path(config_dir)
        self._cache = {}
    
    def load_config(self, config_name):
        """Load configuration file with caching"""
        if config_name in self._cache:
            return self._cache[config_name]
        
        config_path = self.config_dir / f"{config_name}.yaml"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
                self._cache[config_name] = config
                return config
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file {config_path}: {e}")
    
    def get_questions_config(self):
        """Get questions configuration"""
        return self.load_config('questions')
    
    def get_styles_config(self):
        """Get chart styles configuration"""
        return self.load_config('chart_styles')
    
    def get_question_by_id(self, question_id, category=None):
        """Get specific question configuration by ID"""
        questions_config = self.get_questions_config()
        
        if category:
            category_config = questions_config.get(category, {})
            return category_config.get(question_id)
        else:
            # Search across all categories
            for category_name, category_config in questions_config.items():
                if isinstance(category_config, dict) and question_id in category_config:
                    return category_config[question_id]
        
        return None
    
    def get_all_questions(self, category=None):
        """Get all questions from a category or all categories"""
        questions_config = self.get_questions_config()
        
        if category:
            return questions_config.get(category, {})
        else:
            return questions_config
    
    def validate_config(self, config_name):
        """Validate configuration file structure"""
        try:
            config = self.load_config(config_name)
            
            if config_name == 'questions':
                return self._validate_questions_config(config)
            elif config_name == 'chart_styles':
                return self._validate_styles_config(config)
            else:
                return True, "Unknown config type"
                
        except Exception as e:
            return False, str(e)
    
    def _validate_questions_config(self, config):
        """Validate questions configuration structure"""
        required_categories = ['demographics', 'usage_patterns', 'environmental_impact', 'environmental_preferences']
        
        for category in required_categories:
            if category not in config:
                return False, f"Missing required category: {category}"
            
            category_config = config[category]
            if not isinstance(category_config, dict):
                return False, f"Category {category} must be a dictionary"
            
            for question_id, question_config in category_config.items():
                if not isinstance(question_config, dict):
                    return False, f"Question {question_id} must be a dictionary"
                
                required_fields = ['column', 'title', 'chart_type', 'output']
                for field in required_fields:
                    if field not in question_config:
                        return False, f"Question {question_id} missing required field: {field}"
        
        return True, "Questions configuration is valid"
    
    def _validate_styles_config(self, config):
        """Validate styles configuration structure"""
        required_sections = ['font', 'colors', 'dimensions', 'layout', 'output']
        
        for section in required_sections:
            if section not in config:
                return False, f"Missing required section: {section}"
        
        return True, "Styles configuration is valid"

# Global config loader instance
config_loader = ConfigLoader()
