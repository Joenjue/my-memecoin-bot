# Solana Meme Coin Trading Bot

A comprehensive Python-based meme coin trading bot for Solana, specifically targeting new launches on Pump.fun and migrations to Raydium. The bot uses ML/AI to predict pump potential and automatically executes trades via Jupiter Aggregator API with advanced risk management.

## Features

- **Real-Time Monitoring**: Monitors Pump.fun and Raydium for new token launches via WebSocket and API polling
- **Security Checks**: Comprehensive rug/honeypot detection using honeypot.is API and on-chain analysis
- **ML/AI Prediction**: LightGBM classifier with 75+ features to predict token pump potential (aiming for 50-70% win rate)
- **Sentiment Analysis**: Integrates X/Twitter and Reddit sentiment analysis using FinBERT
- **Automated Trading**: Executes buys/sells via Jupiter Aggregator API with risk management
- **Risk Management**: Position sizing (1-2% of portfolio), trailing stops, multi-level take-profits, stop-losses
- **Backtesting**: Historical simulation with equity curve visualization
- **Logging**: Comprehensive logging to console and file

## Requirements

- Python 3.10+
- API keys for:
  - Helius RPC
  - Birdeye
  - Honeypot.is (optional)
  - X/Twitter (optional, for sentiment)
  - Reddit (optional, for sentiment)
  - Telegram (optional, for alerts)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd solana_meme_bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

4. Set up your wallet:
   - Add your wallet private key to `.env`
   - Ensure your wallet has SOL for trading

## Configuration

Edit `.env` file with your configuration:

- `HELIUS_API_KEY`: Your Helius RPC API key
- `BIRDEYE_API_KEY`: Your Birdeye API key
- `WALLET_PRIVATE_KEY`: Your wallet private key (base58 encoded)
- `DRY_RUN`: Set to `true` for testing without real trades
- `ML_THRESHOLD`: ML prediction threshold (default: 0.72)
- `MAX_POSITION_SIZE_PCT`: Maximum position size as % of portfolio (default: 2.0)
- `MAX_CONCURRENT_POSITIONS`: Maximum concurrent positions (default: 5)
- `STOP_LOSS_PCT`: Stop-loss percentage (default: -20.0)
- `TAKE_PROFIT_3X`, `TAKE_PROFIT_5X`, `TAKE_PROFIT_10X`: Take-profit levels

## Usage

### Start Monitoring

Start the bot to monitor for new tokens and execute trades:

```bash
python main.py start_monitor
```

### Train Model

Train the ML model on historical data:

```bash
python main.py train_model --data historical_data.csv
```

### Backtest

Backtest the trading strategy on historical data:

```bash
python main.py backtest --data historical_data.csv --start 2024-01-01 --end 2024-12-31
```

## Project Structure

```
solana_meme_bot/
├── main.py           # Main CLI interface
├── monitor.py        # Real-time token monitoring
├── checks.py         # Security and rug/honeypot checks
├── ml_model.py       # ML prediction model
├── sentiment.py      # Sentiment analysis
├── trader.py         # Trading execution
├── config.py         # Configuration management
├── utils.py          # Utility functions
├── requirements.txt  # Python dependencies
├── .env.example      # Environment variables template
└── README.md         # This file
```

## Trading Strategy

1. **Token Detection**: Monitor Pump.fun and Raydium for new token launches
2. **Security Checks**: Verify token is not a honeypot/rug pull
3. **On-Chain Analysis**: Collect on-chain metrics (liquidity, volume, holders, etc.)
4. **Sentiment Analysis**: Analyze social media sentiment (X/Twitter, Reddit)
5. **ML Prediction**: Use ML model to predict pump potential
6. **Trade Execution**: Execute buy if prediction exceeds threshold
7. **Position Management**: Monitor positions and execute stop-loss/take-profit

## Risk Management

- **Position Sizing**: Maximum 1-2% of portfolio per trade
- **Stop-Loss**: Automatic stop-loss at -20%
- **Take-Profit**: Multi-level take-profits (30% at 3x, 40% at 5x, rest at 10x)
- **Trailing Stop**: Trailing stop-loss enabled (20% below highest price)
- **Timeout**: Automatic sell after 30 minutes
- **Max Positions**: Maximum 5 concurrent positions

## ML Model

The ML model uses LightGBM with 75+ features:

- **On-Chain Features**: Liquidity, volume, holders, price velocity, buy/sell ratios
- **Social Features**: Twitter/Reddit mentions, engagement, sentiment scores
- **Technical Features**: RSI, MACD, volatility, moving averages
- **Metadata Features**: Token name/symbol characteristics, launch time

## Disclaimer

This bot is for educational purposes only. Trading cryptocurrencies involves significant risk. Always:
- Test in dry-run mode first
- Start with small amounts
- Monitor your positions closely
- Never risk more than you can afford to lose

## License

MIT License

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Support

For issues or questions, please open an issue on GitHub.

