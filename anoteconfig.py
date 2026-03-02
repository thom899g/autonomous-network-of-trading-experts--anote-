"""
Configuration and constants for ANOTE system.
Centralized configuration management with environment variables support.
"""

import os
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class TradingMode(Enum):
    """Trading operation modes."""
    BACKTEST = "backtest"
    PAPER = "paper"
    LIVE = "live"

class NodeRole(Enum):
    """Node specialization roles."""
    RESEARCHER = "researcher"
    EXECUTOR = "executor"
    ANALYZER = "analyzer"
    HYBRID = "hybrid"

@dataclass
class ANOTEConfig:
    """Main configuration dataclass for ANOTE system."""
    
    # Node Configuration
    node_id: str = field(default_factory=lambda: os.environ.get("NODE_ID", "anote_node_001"))
    node_role: NodeRole = field(default_factory=lambda: NodeRole(os.environ.get("NODE_ROLE", "HYBRID")))
    trading_mode: TradingMode = field(default_factory=lambda: TradingMode(os.environ.get("TRADING_MODE", "PAPER")))
    
    # Exchange Configuration
    exchange_id: str = field(default_factory=lambda: os.environ.get("EXCHANGE_ID", "binance"))
    api_key: Optional[str] = field(default_factory=lambda: os.environ.get("EXCHANGE_API_KEY"))
    api_secret: Optional[str] = field(default_factory=lambda: os.environ.get("EXCHANGE_API_SECRET"))
    
    # Firebase Configuration (CRITICAL: Ecosystem standard)
    firebase_project_id: str = field(default_factory=lambda: os.environ.get("FIREBASE_PROJECT_ID", "anote-network"))
    firestore_collection: str = field(default_factory=lambda: os.environ.get("FIRESTORE_COLLECTION", "anote_nodes"))
    realtime_db_url: str = field(default_factory=lambda: os.environ.get("FIREBASE_DB_URL", "https://anote-network.firebaseio.com"))
    
    # Trading Parameters
    initial_capital: float = field(default_factory=lambda: float(os.environ.get("INITIAL_CAPITAL", 10000.0)))
    max_position_size: float = field(default_factory=lambda: float(os.environ.get("MAX_POSITION_SIZE", 0.1)))  # 10% of capital
    max_daily_loss: float = field(default_factory=lambda: float(os.environ.get("MAX_DAILY_LOSS", 0.02)))  # 2% daily loss limit
    
    # Network Parameters
    knowledge_share_interval: int = field(default_factory=lambda: int(os.environ.get("KNOWLEDGE_SHARE_INTERVAL", 300)))  # 5 minutes
    strategy_update_frequency: int = field(default_factory=lambda: int(os.environ.get("STRATEGY_UPDATE_FREQ", 3600)))  # 1 hour
    
    # Risk Management
    stop_loss_pct: float = field(default_factory=lambda: float(os.environ.get("STOP_LOSS_PCT", 0.02)))  # 2% stop loss
    take_profit_pct: float = field(default_factory=lambda: float(os.environ.get("TAKE_PROFIT_PCT", 0.05)))  # 5% take profit
    max_leverage: int = field(default_factory=lambda: int(os.environ.get("MAX_LEVERAGE", 3)))
    
    # Learning Parameters
    learning_rate: float = field(default_factory=lambda: float(os.environ.get("LEARNING_RATE", 0.01)))
    exploration_rate: float = field(default_factory=lambda: float(os.environ.get("EXPLORATION_RATE", 0.1)))
    memory_size: int = field(default_factory=lambda: int(os.environ.get("MEMORY_SIZE", 10000)))
    
    # Logging Configuration
    log_level: str = field(default_factory=lambda: os.environ.get("LOG_LEVEL", "INFO"))
    log_file: str = field(default_factory=lambda: os.environ.get("LOG_FILE", "anote.log"))
    
    def validate(self) -> bool:
        """Validate configuration parameters."""
        try:
            if self.trading_mode == TradingMode.LIVE:
                if not self.api_key or not self.api_secret:
                    logging.error("Live trading requires API key and secret")
                    return False
            
            if self.max_position_size <= 0 or self.max_position_size > 1:
                logging.error("max_position_size must be between 0 and 1")
                return False
                
            if self.stop_loss_pct <= 0:
                logging.error("stop_loss_pct must be positive")
                return False
                
            return True
        except Exception as e:
            logging.error(f"Configuration validation failed: {e}")
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for Firebase storage."""
        return {
            "node_id": self.node_id,
            "node_role": self.node_role.value,
            "trading_mode": self.trading_mode.value,
            "exchange_id": self.exchange_id,
            "initial_capital": self.initial_capital,
            "max_position_size": self.max_position_size,
            "max_daily_loss": self.max_daily_loss,
            "config_version": "1.0"
        }

# Global configuration instance
config = ANOTEConfig()