# AlgoTrade Lab - Frontend

Modern Angular-based dashboard for algorithmic trading platform.

## Features

- [LOCK] User authentication with JWT
- [TARGET] Trading strategy management
- [CHART] Interactive dashboard with charts
- [DATA] Backtest execution and visualization
- [CHART] Equity curve display
- [TABLE] Trade history tables
- [MOBILE] Responsive design

## Installation

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build:prod
```

## Development

```bash
# Serve at localhost:4200
npm start

# Run tests
npm test

# Run linting
npm run lint
```

## Project Structure

```
src/
├── app/
│   ├── components/
│   │   ├── auth/
│   │   │   └── login.component.ts
│   │   ├── dashboard/
│   │   │   └── dashboard.component.ts
│   │   ├── strategies/
│   │   │   └── strategies.component.ts
│   │   ├── backtests/
│   │   │   └── backtests.component.ts
│   │   └── layout/
│   │       └── layout.component.ts
│   ├── services/
│   │   ├── auth.service.ts
│   │   ├── strategy.service.ts
│   │   ├── backtest.service.ts
│   │   └── market-data.service.ts
│   ├── guards/
│   │   └── auth.guard.ts
│   ├── interceptors/
│   │   └── auth.interceptor.ts
│   ├── app.routes.ts
│   └── app.config.ts
├── styles.scss
└── index.html
```

## Technology Stack

- **Framework**: Angular 17
- **Language**: TypeScript
- **Styling**: SCSS
- **Charts**: Chart.js with ng2-charts
- **HTTP**: Angular HttpClient
- **Routing**: Angular Router with guards
- **State**: RxJS Observables

## API Integration

The frontend connects to the backend API at `http://localhost:8000/api`. 
The proxy configuration in `proxy.conf.json` handles routing during development.

### Authentication

1. Login with username/password
2. Receive JWT token
3. Token automatically included in all API requests via interceptor
4. Routes protected with AuthGuard

### Services

- **AuthService**: User authentication and token management
- **StrategyService**: CRUD operations for trading strategies
- **BacktestService**: Run backtests and retrieve results
- **MarketDataService**: Fetch market data for analysis

## Components

### Login
- User registration and login
- Form validation
- Error handling

### Dashboard
- Performance metrics
- Equity curve visualization
- Recent backtests list
- Summary statistics

### Strategies
- List all strategies
- Create/edit/delete strategies
- Parameter configuration
- Strategy type selection (MAC, RSI, MACD)

### Backtests
- Run new backtests
- View detailed results
- Performance metrics visualization
- Trade history table
- Backtest history management

### Layout
- Navigation bar
- User logout
- Protected routes

## Styling

SCSS variables and consistent design system:
- Primary color: #667eea
- Dark color: #1a237e
- Success: #2e7d32
- Danger: #d32f2f

## Responsive Design

- Mobile-first approach
- Grid-based layouts
- Flexible components
- Touch-friendly interactions

## Error Handling

- HTTP error interception
- User-friendly error messages
- Form validation feedback
- API error logging

## Future Enhancements

- [ ] Real-time WebSocket updates
- [ ] Advanced charting (TradingView)
- [ ] ML model comparison
- [ ] Portfolio optimization
- [ ] Risk management tools
- [ ] PDF report generation
- [ ] Dark mode theme

## Contributing

See CONTRIBUTING.md in the main project directory.

## License

MIT - See LICENSE in the main project directory.
