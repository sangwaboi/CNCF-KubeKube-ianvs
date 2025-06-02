"""
Industrial Locomotion Metrics for Ianvs Benchmarking
Specialized metrics for evaluating autonomous navigation in industrial environments
"""

import numpy as np
import time
from typing import List, Dict, Any, Tuple

def navigation_success_rate(y_true: List, y_pred: List, **kwargs) -> float:
    """
    Calculate navigation success rate - primary metric for locomotion
    
    Args:
        y_true: Ground truth navigation outcomes (1 for success, 0 for failure)
        y_pred: Predicted navigation outcomes  
        
    Returns:
        Success rate as float between 0 and 1
    """
    if len(y_true) == 0:
        return 0.0
    
    # Convert to numpy arrays
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    # Calculate success rate
    successes = np.sum(y_true == 1)
    total_attempts = len(y_true)
    
    success_rate = successes / total_attempts if total_attempts > 0 else 0.0
    
    print(f"Navigation Success Rate: {success_rate:.3f} ({successes}/{total_attempts})")
    return success_rate

def path_efficiency(y_true: List, y_pred: List, **kwargs) -> float:
    """
    Calculate path efficiency - ratio of optimal path length to actual path length
    
    Args:
        y_true: Ground truth optimal path lengths
        y_pred: Actual path lengths taken
        
    Returns:
        Average path efficiency as float between 0 and 1
    """
    if len(y_true) == 0:
        return 0.0
        
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    # Avoid division by zero
    y_pred = np.where(y_pred == 0, 1e-6, y_pred)
    
    # Calculate efficiency for each path
    efficiencies = y_true / y_pred
    # Cap efficiency at 1.0 (can't be more efficient than optimal)
    efficiencies = np.minimum(efficiencies, 1.0)
    
    avg_efficiency = np.mean(efficiencies)
    
    print(f"Path Efficiency: {avg_efficiency:.3f}")
    return float(avg_efficiency)

def collision_avoidance(y_true: List, y_pred: List, **kwargs) -> float:
    """
    Calculate collision avoidance rate - safety metric
    
    Args:
        y_true: Ground truth collision events (1 for collision, 0 for no collision)
        y_pred: Predicted collision events
        
    Returns:
        Collision avoidance rate as float between 0 and 1
    """
    if len(y_true) == 0:
        return 1.0  # Perfect avoidance if no data
        
    y_true = np.array(y_true)
    
    # Calculate collision avoidance rate
    no_collisions = np.sum(y_true == 0)
    total_scenarios = len(y_true)
    
    avoidance_rate = no_collisions / total_scenarios if total_scenarios > 0 else 1.0
    
    print(f"Collision Avoidance: {avoidance_rate:.3f} ({no_collisions}/{total_scenarios})")
    return avoidance_rate

def execution_time(y_true: List, y_pred: List, **kwargs) -> float:
    """
    Calculate average execution time for navigation tasks
    
    Args:
        y_true: Ground truth execution times (not used, for compatibility)
        y_pred: Actual execution times in seconds
        
    Returns:
        Average execution time in seconds
    """
    if len(y_pred) == 0:
        return 0.0
        
    y_pred = np.array(y_pred)
    avg_time = np.mean(y_pred)
    
    print(f"Average Execution Time: {avg_time:.3f} seconds")
    return float(avg_time)

def accuracy(y_true: List, y_pred: List, **kwargs) -> float:
    """
    Legacy accuracy function for compatibility with Ianvs framework
    Maps to navigation success rate for locomotion tasks
    """
    return navigation_success_rate(y_true, y_pred, **kwargs)

# Metrics registry for easy access
LOCOMOTION_METRICS = {
    'navigation_success_rate': navigation_success_rate,
    'path_efficiency': path_efficiency, 
    'collision_avoidance': collision_avoidance,
    'execution_time': execution_time,
    'accuracy': accuracy  # For compatibility
} 