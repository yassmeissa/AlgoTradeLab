import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BacktestService, BacktestResult } from '../../services/backtest.service';

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="analytics-container">
      <h1>Analytics & Reports</h1>

      <div class="filters">
        <button 
          *ngFor="let period of periods"
          (click)="selectPeriod(period)"
          [class.active]="selectedPeriod === period"
          class="period-btn"
        >
          {{ period }}
        </button>
      </div>

      <div class="stats-section">
        <h2>Overall Statistics</h2>
        <div class="stats-grid">
          <div class="stat-box">
            <h3>Total Backtests</h3>
            <p class="stat-value">{{ backtests.length }}</p>
          </div>
          <div class="stat-box">
            <h3>Avg ROI</h3>
            <p class="stat-value" [ngClass]="{ positive: getAverageROI() > 0 }">
              {{ getAverageROI() | number: '1.2-2' }}%
            </p>
          </div>
          <div class="stat-box">
            <h3>Best ROI</h3>
            <p class="stat-value positive">{{ getBestROI() | number: '1.2-2' }}%</p>
          </div>
          <div class="stat-box">
            <h3>Avg Win Rate</h3>
            <p class="stat-value">{{ getAverageWinRate() | number: '1.2-2' }}%</p>
          </div>
          <div class="stat-box">
            <h3>Avg Sharpe Ratio</h3>
            <p class="stat-value">{{ getAverageSharpe() | number: '1.2-2' }}</p>
          </div>
          <div class="stat-box">
            <h3>Avg Max Drawdown</h3>
            <p class="stat-value negative">{{ getAverageDrawdown() | number: '1.2-2' }}%</p>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host {
      --primary: #f5576c;
      --secondary: #f093fb;
      --dark-bg: #0f0c29;
      --darker-bg: #302b63;
    }

    .analytics-container {
      width: 100%;
    }

    h1 {
      color: white;
      font-size: 2.5rem;
      font-weight: 700;
      margin: 0 0 0.5rem 0;
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .filters {
      display: flex;
      gap: 0.8rem;
      margin-bottom: 2.5rem;
      flex-wrap: wrap;
    }

    .period-btn {
      padding: 0.8rem 1.6rem;
      border: 2px solid rgba(245,87,108,0.2);
      background: rgba(255,255,255,0.05);
      border-radius: 10px;
      cursor: pointer;
      font-weight: 600;
      color: rgba(255,255,255,0.7);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      font-size: 0.95rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .period-btn:hover {
      border-color: var(--primary);
      color: white;
      background: rgba(245,87,108,0.1);
    }

    .period-btn.active {
      background: linear-gradient(135deg, var(--primary), var(--secondary));
      color: white;
      border-color: transparent;
      box-shadow: 0 10px 30px rgba(245,87,108,0.3);
    }

    .stats-section {
      background: linear-gradient(135deg, rgba(240,147,251,0.05), rgba(245,87,108,0.05));
      backdrop-filter: blur(10px);
      border: 1px solid rgba(245,87,108,0.2);
      padding: 2rem;
      border-radius: 16px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.1);
      margin-bottom: 2.5rem;
    }

    .stats-section h2 {
      color: white;
      margin-top: 0;
      margin-bottom: 1.5rem;
      font-size: 1.4rem;
      font-weight: 700;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 1.5rem;
    }

    .stat-box {
      background: linear-gradient(135deg, rgba(240,147,251,0.1), rgba(245,87,108,0.08));
      border: 1px solid rgba(245,87,108,0.2);
      padding: 1.5rem;
      border-radius: 12px;
      text-align: center;
      transition: all 0.3s;
    }

    .stat-box:hover {
      border-color: rgba(245,87,108,0.4);
      transform: translateY(-3px);
      box-shadow: 0 10px 30px rgba(245,87,108,0.2);
    }

    .stat-box h3 {
      margin: 0 0 0.5rem 0;
      color: rgba(255,255,255,0.7);
      font-size: 0.85rem;
      text-transform: uppercase;
      font-weight: 600;
      letter-spacing: 0.5px;
    }

    .stat-value {
      margin: 0.5rem 0 0.8rem 0;
      font-size: 2rem;
      font-weight: 700;
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .positive {
      color: #2ecc71 !important;
    }

    .negative {
      color: #e74c3c !important;
    }
  `]
})
export class AnalyticsComponent implements OnInit {
  backtests: BacktestResult[] = [];
  selectedPeriod = '6M';
  periods = ['1M', '3M', '6M', '1Y', 'All'];

  constructor(private backtestService: BacktestService) {}

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.backtestService.getHistory().subscribe({
      next: (results) => {
        this.backtests = this.filterByPeriod(results);
      },
      error: (error) => console.error('Error loading backtests:', error)
    });
  }

  selectPeriod(period: string): void {
    this.selectedPeriod = period;
    this.loadData();
  }

  filterByPeriod(backtests: BacktestResult[]): BacktestResult[] {
    if (this.selectedPeriod === 'All') return backtests;

    const now = new Date();
    const months = parseInt(this.selectedPeriod) || 
                   (this.selectedPeriod === '1Y' ? 12 : 6);

    const cutoffDate = new Date();
    cutoffDate.setMonth(cutoffDate.getMonth() - months);

    return backtests.filter(bt => {
      const btDate = new Date(bt.created_at);
      return btDate >= cutoffDate;
    });
  }

  getAverageROI(): number {
    if (this.backtests.length === 0) return 0;
    return this.backtests.reduce((acc, bt) => acc + bt.metrics.roi, 0) / this.backtests.length;
  }

  getBestROI(): number {
    if (this.backtests.length === 0) return 0;
    return Math.max(...this.backtests.map(bt => bt.metrics.roi));
  }

  getAverageWinRate(): number {
    if (this.backtests.length === 0) return 0;
    return this.backtests.reduce((acc, bt) => acc + bt.metrics.win_rate, 0) / this.backtests.length;
  }

  getAverageSharpe(): number {
    if (this.backtests.length === 0) return 0;
    return this.backtests.reduce((acc, bt) => acc + bt.metrics.sharpe_ratio, 0) / this.backtests.length;
  }

  getAverageDrawdown(): number {
    if (this.backtests.length === 0) return 0;
    return this.backtests.reduce((acc, bt) => acc + bt.metrics.max_drawdown, 0) / this.backtests.length;
  }
}
