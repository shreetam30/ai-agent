"""
Mathematical Calculation Tools for Langchain Agent
Handles various mathematical operations and calculations
"""

import math
from typing import Union, List, Dict, Any
from langchain.tools import tool
import logging
import numpy as np

logger = logging.getLogger(__name__)


class MathCalculations:
    """Mathematical calculations utility class"""
    
    @staticmethod
    def add(a: Union[float, int], b: Union[float, int]) -> Union[float, int]:
        """Add two numbers"""
        result = a + b
        logger.debug(f"Addition: {a} + {b} = {result}")
        return result
    
    @staticmethod
    def subtract(a: Union[float, int], b: Union[float, int]) -> Union[float, int]:
        """Subtract two numbers"""
        result = a - b
        logger.debug(f"Subtraction: {a} - {b} = {result}")
        return result
    
    @staticmethod
    def multiply(a: Union[float, int], b: Union[float, int]) -> Union[float, int]:
        """Multiply two numbers"""
        result = a * b
        logger.debug(f"Multiplication: {a} * {b} = {result}")
        return result
    
    @staticmethod
    def divide(a: Union[float, int], b: Union[float, int]) -> Union[float, int]:
        """Divide two numbers"""
        if b == 0:
            logger.error("Division by zero attempted")
            raise ValueError("Cannot divide by zero")
        result = a / b
        logger.debug(f"Division: {a} / {b} = {result}")
        return result
    
    @staticmethod
    def power(base: Union[float, int], exponent: Union[float, int]) -> Union[float, int]:
        """Calculate base raised to the power of exponent"""
        result = base ** exponent
        logger.debug(f"Power: {base}^{exponent} = {result}")
        return result
    
    @staticmethod
    def square_root(value: Union[float, int]) -> float:
        """Calculate the square root of a number"""
        if value < 0:
            logger.error("Square root of negative number attempted")
            raise ValueError("Cannot calculate square root of negative number")
        result = math.sqrt(value)
        logger.debug(f"Square root: sqrt({value}) = {result}")
        return result
    
    @staticmethod
    def absolute(value: Union[float, int]) -> Union[float, int]:
        """Get the absolute value of a number"""
        result = abs(value)
        logger.debug(f"Absolute: |{value}| = {result}")
        return result
    
    @staticmethod
    def average(numbers: List[Union[float, int]]) -> float:
        """Calculate the average of a list of numbers"""
        if not numbers:
            raise ValueError("Cannot calculate average of empty list")
        result = sum(numbers) / len(numbers)
        logger.debug(f"Average of {len(numbers)} numbers = {result}")
        return result
    
    @staticmethod
    def sum_numbers(numbers: List[Union[float, int]]) -> Union[float, int]:
        """Sum a list of numbers"""
        result = sum(numbers)
        logger.debug(f"Sum of {len(numbers)} numbers = {result}")
        return result
    
    @staticmethod
    def min_number(numbers: List[Union[float, int]]) -> Union[float, int]:
        """Find the minimum number in a list"""
        if not numbers:
            raise ValueError("Cannot find minimum of empty list")
        result = min(numbers)
        logger.debug(f"Minimum of {len(numbers)} numbers = {result}")
        return result
    
    @staticmethod
    def max_number(numbers: List[Union[float, int]]) -> Union[float, int]:
        """Find the maximum number in a list"""
        if not numbers:
            raise ValueError("Cannot find maximum of empty list")
        result = max(numbers)
        logger.debug(f"Maximum of {len(numbers)} numbers = {result}")
        return result
    
    @staticmethod
    def factorial(n: int) -> int:
        """Calculate factorial of n"""
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        if not isinstance(n, int):
            raise ValueError("Factorial requires an integer")
        result = math.factorial(n)
        logger.debug(f"Factorial: {n}! = {result}")
        return result
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Calculate the greatest common divisor of two numbers"""
        result = math.gcd(a, b)
        logger.debug(f"GCD: gcd({a}, {b}) = {result}")
        return result
    
    @staticmethod
    def lcm(a: int, b: int) -> int:
        """Calculate the least common multiple of two numbers"""
        result = abs(a * b) // math.gcd(a, b)
        logger.debug(f"LCM: lcm({a}, {b}) = {result}")
        return result
    
    @staticmethod
    def percentage(part: Union[float, int], total: Union[float, int]) -> float:
        """Calculate percentage"""
        if total == 0:
            raise ValueError("Cannot calculate percentage with zero total")
        result = (part / total) * 100
        logger.debug(f"Percentage: {part}/{total} * 100 = {result}%")
        return result
    
    @staticmethod
    def mean(numbers: List[Union[float, int]]) -> float:
        """Calculate mean (average) of a list"""
        return MathCalculations.average(numbers)
    
    @staticmethod
    def median(numbers: List[Union[float, int]]) -> Union[float, int]:
        """Calculate median of a list"""
        if not numbers:
            raise ValueError("Cannot calculate median of empty list")
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        if n % 2 == 0:
            result = (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
        else:
            result = sorted_numbers[n//2]
        logger.debug(f"Median of {n} numbers = {result}")
        return result
    
    @staticmethod
    def standard_deviation(numbers: List[Union[float, int]]) -> float:
        """Calculate standard deviation of a list"""
        if not numbers or len(numbers) < 2:
            raise ValueError("Need at least 2 numbers to calculate standard deviation")
        mean_val = MathCalculations.average(numbers)
        variance = sum((x - mean_val) ** 2 for x in numbers) / len(numbers)
        result = math.sqrt(variance)
        logger.debug(f"Standard deviation of {len(numbers)} numbers = {result}")
        return result
    
    @staticmethod
    def variance(numbers: List[Union[float, int]]) -> float:
        """Calculate variance of a list"""
        if not numbers or len(numbers) < 2:
            raise ValueError("Need at least 2 numbers to calculate variance")
        mean_val = MathCalculations.average(numbers)
        result = sum((x - mean_val) ** 2 for x in numbers) / len(numbers)
        logger.debug(f"Variance of {len(numbers)} numbers = {result}")
        return result
    
    @staticmethod
    def round_number(value: Union[float, int], decimals: int = 0) -> Union[float, int]:
        """Round a number to specified decimal places"""
        result = round(value, decimals)
        logger.debug(f"Round: {value} to {decimals} decimals = {result}")
        return result


# Langchain tool definitions
@tool
def add_tool(a: float, b: float) -> float:
    """Add two numbers together."""
    return MathCalculations.add(a, b)


@tool
def subtract_tool(a: float, b: float) -> float:
    """Subtract b from a."""
    return MathCalculations.subtract(a, b)


@tool
def multiply_tool(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return MathCalculations.multiply(a, b)


@tool
def divide_tool(a: float, b: float) -> float:
    """Divide a by b."""
    return MathCalculations.divide(a, b)


@tool
def power_tool(base: float, exponent: float) -> float:
    """Raise base to the power of exponent."""
    return MathCalculations.power(base, exponent)


@tool
def square_root_tool(value: float) -> float:
    """Calculate the square root of a value."""
    return MathCalculations.square_root(value)


@tool
def absolute_tool(value: float) -> float:
    """Get the absolute value of a number."""
    return MathCalculations.absolute(value)


@tool
def average_tool(numbers: List[float]) -> float:
    """Calculate the average of a list of numbers."""
    return MathCalculations.average(numbers)


@tool
def sum_tool(numbers: List[float]) -> float:
    """Sum a list of numbers."""
    return MathCalculations.sum_numbers(numbers)


@tool
def min_tool(numbers: List[float]) -> float:
    """Find the minimum value in a list of numbers."""
    return MathCalculations.min_number(numbers)


@tool
def max_tool(numbers: List[float]) -> float:
    """Find the maximum value in a list of numbers."""
    return MathCalculations.max_number(numbers)


@tool
def factorial_tool(n: int) -> int:
    """Calculate the factorial of n."""
    return MathCalculations.factorial(n)


@tool
def gcd_tool(a: int, b: int) -> int:
    """Calculate the greatest common divisor of two numbers."""
    return MathCalculations.gcd(a, b)


@tool
def lcm_tool(a: int, b: int) -> int:
    """Calculate the least common multiple of two numbers."""
    return MathCalculations.lcm(a, b)


@tool
def percentage_tool(part: float, total: float) -> float:
    """Calculate what percentage part is of total."""
    return MathCalculations.percentage(part, total)


@tool
def median_tool(numbers: List[float]) -> float:
    """Calculate the median of a list of numbers."""
    return MathCalculations.median(numbers)


@tool
def standard_deviation_tool(numbers: List[float]) -> float:
    """Calculate the standard deviation of a list of numbers."""
    return MathCalculations.standard_deviation(numbers)


@tool
def variance_tool(numbers: List[float]) -> float:
    """Calculate the variance of a list of numbers."""
    return MathCalculations.variance(numbers)


@tool
def round_tool(value: float, decimals: int = 0) -> float:
    """Round a number to a specified number of decimal places."""
    return MathCalculations.round_number(value, decimals)
