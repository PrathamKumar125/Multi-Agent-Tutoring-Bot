from typing import Union
import re
import math

class Calculator:
    """A simple calculator tool for basic arithmetic operations."""
    
    @staticmethod
    def add(a: float, b: float) -> float:
        """Add two numbers."""
        return a + b
    
    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Subtract second number from first."""
        return a - b
    
    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b
    
    @staticmethod
    def divide(a: float, b: float) -> float:
        """Divide first number by second."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    @staticmethod
    def power(a: float, b: float) -> float:
        """Raise first number to the power of second."""
        return a ** b
    
    @staticmethod
    def sqrt(a: float) -> float:
        """Calculate square root."""
        if a < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(a)
    
    @staticmethod
    def evaluate_expression(expression: str) -> float:
        """Safely evaluate a mathematical expression."""
        # Remove spaces and validate expression
        expression = expression.replace(" ", "")
        
        # Only allow digits, operators, parentheses, and decimal points
        if not re.match(r'^[0-9+\-*/().^√]+$', expression):
            raise ValueError("Invalid characters in expression")
        
        # Replace ^ with ** for power operations
        expression = expression.replace("^", "**")
        
        # Handle square root symbol
        expression = re.sub(r'√(\d+(?:\.\d+)?)', r'math.sqrt(\1)', expression)
        
        try:
            # Use eval with restricted globals for safety
            allowed_names = {
                "__builtins__": {},
                "math": math,
            }
            return eval(expression, allowed_names)
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {str(e)}")
