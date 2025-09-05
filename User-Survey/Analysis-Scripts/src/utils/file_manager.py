"""
File management utilities for survey analyzer
Handles output organization, versioning, and metadata tracking
"""

import os
import json
from datetime import datetime
from pathlib import Path

class OutputManager:
    """Manages output file organization and metadata"""
    
    def __init__(self, base_path="output", version=None):
        """Initialize output manager"""
        self.base_path = Path(base_path)
        self.version = version or self._generate_version()
        self.metadata = {
            'generated_at': datetime.now().isoformat(),
            'version': self.version,
            'files_created': []
        }
    
    def _generate_version(self):
        """Generate version string based on timestamp"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def create_plot_path(self, category, subcategory=None, filename=None):
        """Create organized path for plot files"""
        path_parts = [self.base_path, 'plots', category]
        
        if subcategory:
            path_parts.append(subcategory)
        
        plot_dir = Path(*path_parts)
        plot_dir.mkdir(parents=True, exist_ok=True)
        
        if filename:
            return plot_dir / filename
        else:
            return plot_dir
    
    def create_data_path(self, subcategory=None, filename=None):
        """Create organized path for data files"""
        path_parts = [self.base_path, 'data']
        
        if subcategory:
            path_parts.append(subcategory)
        
        data_dir = Path(*path_parts)
        data_dir.mkdir(parents=True, exist_ok=True)
        
        if filename:
            return data_dir / filename
        else:
            return data_dir
    
    def create_report_path(self, filename=None):
        """Create organized path for report files"""
        report_dir = self.base_path / 'reports'
        report_dir.mkdir(parents=True, exist_ok=True)
        
        if filename:
            return report_dir / filename
        else:
            return report_dir
    
    def add_timestamp_to_filename(self, filename):
        """Add timestamp to filename for versioning"""
        name, ext = os.path.splitext(filename)
        return f"{name}_{self.version}{ext}"
    
    def track_file_creation(self, file_path, file_type, description=None):
        """Track file creation in metadata"""
        self.metadata['files_created'].append({
            'path': str(file_path),
            'type': file_type,
            'description': description,
            'created_at': datetime.now().isoformat()
        })
    
    def save_metadata(self):
        """Save generation metadata to file"""
        metadata_path = self.create_report_path('generation_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)
        
        print(f"Metadata saved to: {metadata_path}")
        return metadata_path
    
    def get_summary(self):
        """Get summary of created files"""
        summary = {
            'version': self.version,
            'generated_at': self.metadata['generated_at'],
            'total_files': len(self.metadata['files_created']),
            'files_by_type': {}
        }
        
        for file_info in self.metadata['files_created']:
            file_type = file_info['type']
            if file_type not in summary['files_by_type']:
                summary['files_by_type'][file_type] = 0
            summary['files_by_type'][file_type] += 1
        
        return summary
    
    def print_summary(self):
        """Print generation summary"""
        summary = self.get_summary()
        print(f"\n{'='*50}")
        print(f"GENERATION SUMMARY")
        print(f"{'='*50}")
        print(f"Version: {summary['version']}")
        print(f"Generated: {summary['generated_at']}")
        print(f"Total files: {summary['total_files']}")
        print(f"\nFiles by type:")
        for file_type, count in summary['files_by_type'].items():
            print(f"  {file_type}: {count}")
        print(f"{'='*50}")

# Global output manager instance
output_manager = OutputManager()
