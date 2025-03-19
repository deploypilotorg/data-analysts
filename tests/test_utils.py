"""
Tests for the utility functions in miguellib.utils.
"""

import os
import json
import yaml
import tempfile
import unittest
from miguellib.utils import load_config, save_config, merge_configs


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_load_config_yaml(self):
        """Test loading a YAML configuration file."""
        with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as temp:
            temp.write(b"""
app:
  name: test-app
  version: 1.0.0
environment: development
""")
            temp_path = temp.name
        
        try:
            config = load_config(temp_path)
            self.assertEqual(config['app']['name'], 'test-app')
            self.assertEqual(config['app']['version'], '1.0.0')
            self.assertEqual(config['environment'], 'development')
        finally:
            os.unlink(temp_path)
    
    def test_load_config_json(self):
        """Test loading a JSON configuration file."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp:
            temp.write(b"""
{
  "app": {
    "name": "test-app",
    "version": "1.0.0"
  },
  "environment": "development"
}
""")
            temp_path = temp.name
        
        try:
            config = load_config(temp_path)
            self.assertEqual(config['app']['name'], 'test-app')
            self.assertEqual(config['app']['version'], '1.0.0')
            self.assertEqual(config['environment'], 'development')
        finally:
            os.unlink(temp_path)
    
    def test_save_config_yaml(self):
        """Test saving a configuration to a YAML file."""
        config = {
            'app': {
                'name': 'test-app',
                'version': '1.0.0'
            },
            'environment': 'development'
        }
        
        with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as temp:
            temp_path = temp.name
        
        try:
            save_config(config, temp_path)
            
            with open(temp_path, 'r') as f:
                loaded_config = yaml.safe_load(f)
            
            self.assertEqual(loaded_config['app']['name'], 'test-app')
            self.assertEqual(loaded_config['app']['version'], '1.0.0')
            self.assertEqual(loaded_config['environment'], 'development')
        finally:
            os.unlink(temp_path)
    
    def test_merge_configs(self):
        """Test merging two configuration dictionaries."""
        base_config = {
            'app': {
                'name': 'base-app',
                'version': '1.0.0',
                'settings': {
                    'debug': False,
                    'log_level': 'info'
                }
            },
            'environment': 'development'
        }
        
        override_config = {
            'app': {
                'name': 'override-app',
                'settings': {
                    'debug': True
                }
            },
            'resources': {
                'cpu': '1',
                'memory': '512Mi'
            }
        }
        
        merged = merge_configs(base_config, override_config)
        
        self.assertEqual(merged['app']['name'], 'override-app')
        self.assertEqual(merged['app']['version'], '1.0.0')
        self.assertEqual(merged['app']['settings']['debug'], True)
        self.assertEqual(merged['app']['settings']['log_level'], 'info')
        self.assertEqual(merged['environment'], 'development')
        self.assertEqual(merged['resources']['cpu'], '1')
        self.assertEqual(merged['resources']['memory'], '512Mi')


if __name__ == '__main__':
    unittest.main() 