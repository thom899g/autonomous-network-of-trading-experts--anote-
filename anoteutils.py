"""
Utility functions for ANOTE system.
Handles common operations, error handling, and data transformations.
"""

import logging
import time
import json
import hashlib
from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from dataclasses import asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('anote.log')
    ]
)

class ANOTEError(Exception):
    """Base exception for ANOTE system."""
    pass

class MarketDataError(ANOTEError):
    """Market data related errors."""
    pass

class TradeExecutionError(ANOTEError):
    """Trade execution related errors."""
    pass

class NetworkError(ANOTEError):
    """Network communication errors."""
    pass

def setup_logger(name: str,