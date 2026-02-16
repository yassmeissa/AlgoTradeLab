import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { BacktestService, BacktestRequest, BacktestResult } from '../../services/backtest.service';
import { StrategyService, Strategy } from '../../services/strategy.service';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration } from 'chart.js';

@Component({
  selector: 'app-backtests',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, BaseChartDirective],
  template: `
    <div class="backtests-container">
      <div class="header">
        <h1>Backtests</h1>
      </div>

      <div class="content-wrapper">
        <div class="form-section">
          <h2>Run New Backtest</h2>
          <form [formGroup]="backtestForm" (ngSubmit)="runBacktest()">
            <div class="form-group">
              <label for="strategy_id">Strategy</label>
              <select id="strategy_id" formControlName="strategy_id" class="form-control">
                <option value="">Select a strategy</option>
                <option *ngFor="let strategy of strategies" [value]="strategy.id">
                  {{ strategy.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="symbol">Symbol</label>
              <input
                type="text"
                id="symbol"
                formControlName="symbol"
                class="form-control"
                placeholder="e.g., AAPL, BTC"
              />
            </div>

            <div class="date-group">
              <div class="form-group">
                <label for="start_date">Start Date</label>
                <input
                  type="date"
                  id="start_date"
                  formControlName="start_date"
                  class="form-control"
                />
              </div>
              <div class="form-group">
                <label for="end_date">End Date</label>
                <input
                  type="date"
                  id="end_date"
                  formControlName="end_date"
                  class="form-control"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="initial_capital">Initial Capital</label>
              <input
                type="number"
                id="initial_capital"
                formControlName="initial_capital"
                class="form-control"
                min="1000"
                step="1000"
              />
            </div>

            <button
              type="submit"
              [disabled]="backtestForm.invalid || isRunning"
              class="btn-submit"
            >
              {{ isRunning ? 'Running...' : 'Run Backtest' }}
            </button>
          </form>
        </div>

        <div *ngIf="selectedBacktest" class="results-section">
          <h2>Backtest Results</h2>

          <div class="metrics-grid">
            <div class="metric-card">
              <h4>Total Return</h4>
              <p [ngClass]="{ positive: (selectedBacktest as any).total_return > 0, negative: (selectedBacktest as any).total_return < 0 }">
                {{ '$' + ((selectedBacktest as any).total_return | number: '1.2-2') }}
              </p>
            </div>
            <div class="metric-card">
              <h4>ROI</h4>
              <p [ngClass]="{ positive: (selectedBacktest as any).roi > 0, negative: (selectedBacktest as any).roi < 0 }">
                {{ (selectedBacktest as any).roi | number: '1.2-2' }}%
              </p>
            </div>
            <div class="metric-card">
              <h4>Sharpe Ratio</h4>
              <p>{{ (selectedBacktest as any).sharpe_ratio | number: '1.2-2' }}</p>
            </div>
            <div class="metric-card">
              <h4>Max Drawdown</h4>
              <p [ngClass]="{ negative: (selectedBacktest as any).max_drawdown < 0 }">
                {{ (selectedBacktest as any).max_drawdown | number: '1.2-2' }}%
              </p>
            </div>
            <div class="metric-card">
              <h4>Win Rate</h4>
              <p>{{ (selectedBacktest as any).win_rate | number: '1.2-2' }}%</p>
            </div>
            <div class="metric-card">
              <h4>Total Trades</h4>
              <p>{{ (selectedBacktest as any).total_trades }}</p>
            </div>
            <div class="metric-card">
              <h4>Profit Factor</h4>
              <p>{{ (selectedBacktest as any).profit_factor | number: '1.2-2' }}</p>
            </div>
          </div>

          <div *ngIf="equityChart" class="chart-container">
            <h3>Equity Curve</h3>
            <canvas baseChart
                    [data]="equityChart.data"
                    [options]="equityChart.options"
                    [type]="equityChart.type">
            </canvas>
          </div>

          <div class="trades-table">
            <h3>Trades</h3>
            <table>
              <thead>
                <tr>
                  <th>Entry Date</th>
                  <th>Entry Price</th>
                  <th>Exit Date</th>
                  <th>Exit Price</th>
                  <th>PnL</th>
                  <th>PnL %</th>
                </tr>
              </thead>
              <tbody>
                <tr *ngFor="let trade of selectedBacktest.trades">
                  <td>{{ trade.entry_date | date: 'short' }}</td>
                  <td>{{ '$' + (trade.entry_price | number: '1.2-2') }}</td>
                  <td>{{ trade.exit_date | date: 'short' }}</td>
                  <td>{{ '$' + (trade.exit_price | number: '1.2-2') }}</td>
                  <td [ngClass]="{ positive: trade.pnl > 0, negative: trade.pnl < 0 }">
                    {{ '$' + (trade.pnl | number: '1.2-2') }}
                  </td>
                  <td [ngClass]="{ positive: trade.pnl_percent > 0, negative: trade.pnl_percent < 0 }">
                    {{ trade.pnl_percent | number: '1.2-2' }}%
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="history-section">
        <h2>Backtest History</h2>
        <table class="history-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Strategy</th>
              <th>Symbol</th>
              <th>ROI</th>
              <th>Sharpe</th>
              <th>Win Rate</th>
              <th>Max Drawdown</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let backtest of backtests" [class.selected]="backtest.id === selectedBacktest?.id">
              <td>{{ backtest.created_at | date: 'short' }}</td>
              <td>{{ getStrategyName(backtest.strategy_id) }}</td>
              <td>{{ backtest.symbol }}</td>
              <td [ngClass]="{ positive: (backtest as any).roi > 0, negative: (backtest as any).roi < 0 }">
                {{ (backtest as any).roi | number: '1.2-2' }}%
              </td>
              <td>{{ (backtest as any).sharpe_ratio | number: '1.2-2' }}</td>
              <td>{{ (backtest as any).win_rate | number: '1.2-2' }}%</td>
              <td [ngClass]="{ negative: (backtest as any).max_drawdown < 0 }">
                {{ (backtest as any).max_drawdown | number: '1.2-2' }}%
              </td>
              <td>
                <button (click)="selectBacktest(backtest)" class="btn-small btn-primary">
                  View
                </button>
                <button (click)="deleteBacktest(backtest.id)" class="btn-small btn-danger">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `,
  styles: [`
    .backtests-container {
      padding: 2rem;
      max-width: 1400px;
      margin: 0 auto;
    }

    .header {
      margin-bottom: 2rem;
    }

    .header h1 {
      color: #1a237e;
      margin: 0;
    }

    .content-wrapper {
      display: grid;
      grid-template-columns: 1fr 2fr;
      gap: 2rem;
      margin-bottom: 2rem;
    }

    .form-section, .results-section {
      background: white;
      padding: 1.5rem;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .form-section h2, .results-section h2, .history-section h2 {
      color: #1a237e;
      margin-top: 0;
      margin-bottom: 1.5rem;
      font-size: 1.2rem;
    }

    .form-group {
      margin-bottom: 1rem;
    }

    label {
      display: block;
      margin-bottom: 0.5rem;
      font-weight: 500;
      color: #333;
    }

    .form-control {
      width: 100%;
      padding: 0.75rem;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-size: 1rem;
      font-family: inherit;
    }

    .form-control:focus {
      outline: none;
      border-color: #667eea;
      box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    .date-group {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
    }

    .btn-submit {
      width: 100%;
      padding: 0.75rem;
      background-color: #667eea;
      color: white;
      border: none;
      border-radius: 4px;
      font-weight: 600;
      cursor: pointer;
      transition: background-color 0.3s;
    }

    .btn-submit:hover:not(:disabled) {
      background-color: #5568d3;
    }

    .btn-submit:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }

    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 1rem;
      margin-bottom: 2rem;
    }

    .metric-card {
      background: #f5f5f5;
      padding: 1rem;
      border-radius: 4px;
      text-align: center;
    }

    .metric-card h4 {
      margin: 0 0 0.5rem 0;
      color: #666;
      font-size: 0.875rem;
      text-transform: uppercase;
      font-weight: 500;
    }

    .metric-card p {
      margin: 0;
      font-size: 1.5rem;
      font-weight: 700;
      color: #1a237e;
    }

    .positive {
      color: #2e7d32 !important;
    }

    .negative {
      color: #d32f2f !important;
    }

    .chart-container {
      margin-bottom: 2rem;
    }

    .chart-container h3 {
      color: #1a237e;
      margin-bottom: 1rem;
    }

    .trades-table {
      margin-bottom: 2rem;
    }

    .trades-table h3 {
      color: #1a237e;
      margin-bottom: 1rem;
    }

    table {
      width: 100%;
      border-collapse: collapse;
    }

    th {
      background-color: #f5f5f5;
      padding: 0.75rem;
      text-align: left;
      font-weight: 600;
      color: #1a237e;
      border-bottom: 2px solid #e0e0e0;
      font-size: 0.875rem;
    }

    td {
      padding: 0.75rem;
      border-bottom: 1px solid #e0e0e0;
    }

    tr:hover {
      background-color: #f9f9f9;
    }

    .selected {
      background-color: #e3f2fd;
    }

    .history-section {
      background: white;
      padding: 1.5rem;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .history-table {
      width: 100%;
    }

    .btn-small {
      padding: 0.4rem 0.8rem;
      font-size: 0.75rem;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-weight: 600;
      margin-right: 0.5rem;
    }

    .btn-primary {
      background-color: #667eea;
      color: white;
    }

    .btn-primary:hover {
      background-color: #5568d3;
    }

    .btn-danger {
      background-color: #d32f2f;
      color: white;
    }

    .btn-danger:hover {
      background-color: #b71c1c;
    }

    @media (max-width: 1024px) {
      .content-wrapper {
        grid-template-columns: 1fr;
      }

      .date-group {
        grid-template-columns: 1fr;
      }
    }
  `]
})
export class BacktestsComponent implements OnInit {
  backtestForm!: FormGroup;
  strategies: Strategy[] = [];
  backtests: BacktestResult[] = [];
  selectedBacktest: BacktestResult | null = null;
  isRunning = false;
  equityChart: ChartConfiguration | null = null;

  constructor(
    private fb: FormBuilder,
    private backtestService: BacktestService,
    private strategyService: StrategyService
  ) {}

  ngOnInit(): void {
    this.initializeForm();
    this.loadStrategies();
    this.loadBacktests();
  }

  initializeForm(): void {
    this.backtestForm = this.fb.group({
      strategy_id: ['', Validators.required],
      symbol: ['', Validators.required],
      start_date: ['', Validators.required],
      end_date: ['', Validators.required],
      initial_capital: [10000, [Validators.required, Validators.min(1000)]]
    });
  }

  loadStrategies(): void {
    this.strategyService.getAll().subscribe({
      next: (strategies) => {
        this.strategies = strategies;
      },
      error: (error) => console.error('Error loading strategies:', error)
    });
  }

  loadBacktests(): void {
    this.backtestService.getHistory().subscribe({
      next: (backtests) => {
        this.backtests = backtests;
      },
      error: (error) => console.error('Error loading backtests:', error)
    });
  }

  runBacktest(): void {
    if (this.backtestForm.invalid) return;

    this.isRunning = true;
    const request: BacktestRequest = this.backtestForm.value;

    this.backtestService.runBacktest(request).subscribe({
      next: (result) => {
        this.backtests.unshift(result);
        this.selectBacktest(result);
        this.isRunning = false;
      },
      error: (error) => {
        console.error('Error running backtest:', error);
        this.isRunning = false;
      }
    });
  }

  selectBacktest(backtest: BacktestResult): void {
    this.selectedBacktest = backtest;
    this.initializeEquityChart();
  }

  deleteBacktest(id: number): void {
    if (confirm('Are you sure you want to delete this backtest?')) {
      this.backtestService.delete(id).subscribe({
        next: () => {
          this.backtests = this.backtests.filter(bt => bt.id !== id);
          if (this.selectedBacktest?.id === id) {
            this.selectedBacktest = null;
          }
        },
        error: (error) => console.error('Error deleting backtest:', error)
      });
    }
  }

  initializeEquityChart(): void {
    if (!this.selectedBacktest) return;

    this.equityChart = {
      type: 'line',
      data: {
        labels: Array.from({ length: this.selectedBacktest.equity_curve.length }, (_, i) => i),
        datasets: [
          {
            label: 'Equity',
            data: this.selectedBacktest.equity_curve,
            borderColor: '#667eea',
            backgroundColor: 'rgba(102, 126, 234, 0.1)',
            fill: true,
            tension: 0.4,
            pointRadius: 0
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: true }
        },
        scales: {
          y: { beginAtZero: false }
        }
      }
    };
  }

  getStrategyName(strategyId: number): string {
    const strategy = this.strategies.find(s => s.id === strategyId);
    return strategy?.name || 'Unknown';
  }
}
