from typing import Dict, Any, Optional
from config import PHYSICS_CONSTANTS

class PhysicsConstantsLookup:
    """A tool for looking up physical constants."""
    
    def __init__(self):
        self.constants = PHYSICS_CONSTANTS
    
    def get_constant(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Look up a physical constant by name.
        
        Args:
            name: The name of the constant (case-insensitive)
            
        Returns:
            Dictionary with value, unit, and symbol, or None if not found
        """
        name_lower = name.lower().replace(" ", "_")
        return self.constants.get(name_lower)
    
    def search_constants(self, keyword: str) -> Dict[str, Dict[str, Any]]:
        """
        Search for constants containing a keyword.
        
        Args:
            keyword: The keyword to search for
            
        Returns:
            Dictionary of matching constants
        """
        keyword_lower = keyword.lower()
        matches = {}
        
        for const_name, const_data in self.constants.items():
            if (keyword_lower in const_name.lower() or 
                keyword_lower in const_data.get("symbol", "").lower()):
                matches[const_name] = const_data
                
        return matches
    
    def list_all_constants(self) -> Dict[str, Dict[str, Any]]:
        """Return all available constants."""
        return self.constants
    
    def format_constant(self, name: str, data: Dict[str, Any]) -> str:
        """Format a constant for display."""
        return f"{name.replace('_', ' ').title()}: {data['value']} {data['unit']} (Symbol: {data['symbol']})"
