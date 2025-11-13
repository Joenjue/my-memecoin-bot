"""
Utility functions for logging, data processing, and common operations.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from colorama import Fore, Style, init
import json

# Initialize colorama for Windows
init(autoreset=True)

from config import Config


def setup_logger(name: str = "solana_bot") -> logging.Logger:
    """
    Set up a logger with both file and console handlers.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, Config.LOG_LEVEL.upper()))
    
    # Remove existing handlers
    logger.handlers = []
    
    # File handler
    file_handler = logging.FileHandler(Config.LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger


def format_sol_amount(lamports: int) -> float:
    """Convert lamports to SOL."""
    return lamports / 1e9


def format_usd(value: float) -> str:
    """Format USD value."""
    return f"${value:,.2f}"


def format_percentage(value: float) -> str:
    """Format percentage."""
    return f"{value:.2f}%"


def log_trade(logger: logging.Logger, action: str, token: str, details: Dict[str, Any]):
    """Log a trade action with formatted details."""
    logger.info(f"{Fore.CYAN}{action}{Style.RESET_ALL} - Token: {token}")
    for key, value in details.items():
        logger.info(f"  {key}: {value}")


def save_trade_to_file(trade_data: Dict[str, Any], filename: str = "trades.json"):
    """Save trade data to JSON file."""
    filepath = Path(filename)
    
    if filepath.exists():
        with open(filepath, 'r') as f:
            trades = json.load(f)
    else:
        trades = []
    
    trades.append({
        **trade_data,
        "timestamp": datetime.now().isoformat()
    })
    
    with open(filepath, 'w') as f:
        json.dump(trades, f, indent=2)


def calculate_position_size(portfolio_value: float, token_price: float, max_pct: float = 2.0) -> float:
    """
    Calculate position size based on portfolio value and max percentage.
    
    Args:
        portfolio_value: Total portfolio value in USD
        token_price: Token price in USD
        max_pct: Maximum percentage of portfolio to risk
        
    Returns:
        Position size in token units
    """
    max_usd = portfolio_value * (max_pct / 100)
    return max_usd / token_price if token_price > 0 else 0


def is_meme_coin_name(name: str) -> bool:
    """
    Check if token name suggests it's a meme coin.
    
    Args:
        name: Token name or symbol
        
    Returns:
        True if likely a meme coin
    """
    if not name:
        return False
    
    name_lower = name.lower()
    
    # Meme coin indicators
    meme_keywords = [
        'pepe', 'doge', 'shib', 'floki', 'bonk', 'wif', 'meme',
        'inu', 'cat', 'dog', 'frog', 'moon', 'rocket', 'gem',
        'diamond', 'hands', 'ape', 'chad', 'gigachad', 'wojak'
    ]
    
    return any(keyword in name_lower for keyword in meme_keywords)


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator for retrying functions on failure.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay * (attempt + 1))
            return None
        return wrapper
    return decorator


def validate_token_address(address: str) -> bool:
    """
    Validate Solana token address format.
    
    Args:
        address: Token address to validate
        
    Returns:
        True if valid format
    """
    if not address or len(address) < 32 or len(address) > 44:
        return False
    try:
        import base58
        base58.b58decode(address)
        return True
    except:
        return False

