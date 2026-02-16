import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BacktestService, BacktestResult } from '../../services/backtest.service';
import { StrategyService, Strategy } from '../../services/strategy.service';
import { AuthService } from '../../services/auth.service';
import { ChartConfiguration } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';

interface UserProfile {
  id: number;
  username: string;
  email: string;
  full_name?: string;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, BaseChartDirective],
  template: `
    <div class="dashboard-container">
      <div class="dashboard-header">
        <h1>📊 Dashboard - {{ userProfile?.full_name || userProfile?.username }}</h1>
        <p class="subtitle">{{ getGreeting() }} - Your trading performance insights</p>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-header">
            <span class="icon">📈</span>
            <h3>Total Backtests</h3>
          </div>
          <p class="stat-value">{{ backtests.length }}</p>
          <span class="stat-label">backtests executed</span>
        </div>
        <div class="stat-card">
          <div class="stat-header">
            <span class="icon">�</span>
            <h3>Active Strategies</h3>
          </div>
          <p class="stat-value">{{ strategies.length }}</p>
          <span class="stat-label">strategies deployed</span>
        </div>
        <div class="stat-card">
          <div class="stat-header">
            <span class="icon">�💰</span>
            <h3>Avg ROI</h3>
          </div>
          <p class="stat-value" [ngClass]="{ positive: getAverageROI() > 0, negative: getAverageROI() < 0 }">
            {{ getAverageROI() | number: '1.2-2' }}%
          </p>
          <span class="stat-label">average return</span>
        </div>
        <div class="stat-card">
          <div class="stat-header">
            <span class="icon">⭐</span>
            <h3>Best Sharpe</h3>
          </div>
          <p class="stat-value">{{ getBestSharpeRatio() | number: '1.2-2' }}</p>
          <span class="stat-label">risk-adjusted return</span>
        </div>
        <div class="stat-card">
          <div class="stat-header">
            <span class="icon">🎯</span>
            <h3>Win Rate</h3>
          </div>
          <p class="stat-value">{{ getAverageWinRate() | number: '1.2-2' }}%</p>
          <span class="stat-label">success rate</span>
        </div>
      </div>

      <div class="charts-container">
        <div class="chart-wrapper">
          <div class="chart-header">
            <h2>📈 Equity Curve</h2>
            <span class="chart-badge">Last Backtest</span>
          </div>
          <canvas *ngIf="equityCurveChart" 
                  baseChart
                  [data]="equityCurveChart.data"
                  [options]="equityCurveChart.options"
                  [type]="equityCurveChart.type">
          </canvas>
        </div>

        <div class="chart-wrapper">
          <div class="chart-header">
            <h2>�� Performance</h2>
            <span class="chart-badge">Distribution</span>
          </div>
          <canvas *ngIf="performanceChart"
                  baseChart
                  [data]="performanceChart.data"
                  [options]="performanceChart.options"
                  [type]="performanceChart.type">
          </canvas>
        </div>
      </div>

      <div class="recent-backtests">
        <div class="section-header">
          <h2>🏆 Recent Backtests</h2>
          <span class="count">{{ backtests.length }} total</span>
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Symbol</th>
                <th>ROI</th>
                <th>Sharpe</th>
                <th>Win Rate</th>
                <th>Drawdown</th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let backtest of backtests.slice(0, 5)">
                <td class="date-cell">{{ backtest.created_at | date: 'short' }}</td>
                <td class="symbol-cell"><strong>{{ (backtest as any).symbol }}</strong></td>
                <td [ngClass]="{ positive: (backtest as any).roi > 0, negative: (backtest as any).roi < 0 }">
                  {{ (backtest as any).roi | number: '1.2-2' }}%
                </td>
                <td>{{ (backtest as any).sharpe_ratio | number: '1.2-2' }}</td>
                <td class="badge-cell">
                  <span [ngClass]="{ 'badge-high': (backtest as any).win_rate > 60, 'badge-mid': (backtest as any).win_rate > 40, 'badge-low': (backtest as any).win_rate <= 40 }">
                    {{ (backtest as any).win_rate | number: '1.1-1' }}%
                  </span>
                </td>
                <td [ngClass]="{ negative: backtest.metrics.max_drawdown < 0 }">
                  {{ backtest.metrics.max_drawdown | number: '1.2-2' }}%
                </td>
              </tr>
            </tbody>
          </table>
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
      --accent: #24243e;
      --text-light: rgba(255,255,255,0.8);
    }

    .dashboard-container {
      width: 100%;
    }

    .dashboard-header {
      margin-bottom: 2.5rem;
    }

    .dashboard-header h1 {
      color: white;
      font-size: 2.5rem;
      font-weight: 700;
      margin: 0 0 0.5rem 0;
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .subtitle {
      color: rgba(255,255,255,0.6);
      font-size: 1rem;
      margin: 0;
      font-weight: 500;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1.5rem;
      margin-bottom: 2.5rem;
    }

    .stat-card {
      background: linear-gradient(135deg, rgba(240,147,251,0.1), rgba(245,87,108,0.05));
      backdrop-filter: blur(10px);
      border: 1px solid rgba(245,87,108,0.2);
      border-radius: 16px;
      padding: 1.8rem;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      overflow: hidden;
    }

    .stat-card::before {
      content: '';
      position: absolute;
      top: -50%;
      right: -50%;
      width: 200%;
      height: 200%;
      background: linear-gradient(135deg, rgba(240,147,251,0.1), transparent);
      transition: all 0.3s;
    }

    .stat-card:hover {
      border-color: rgba(245,87,108,0.4);
      transform: translateY(-5px);
      box-shadow: 0 20px 40px rgba(245,87,108,0.2);
    }

    .stat-header {
      display: flex;
      align-items: center;
      gap: 1rem;
      margin-bottom: 1.2rem;
    }

    .stat-header .icon {
      font-size: 2rem;
      filter: drop-shadow(0 2px 4px rgba(245,87,108,0.2));
    }

    .stat-header h3 {
      color: rgba(255,255,255,0.8);
      font-size: 0.95rem;
      font-weight: 600;
      margin: 0;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .stat-value {
      font-size: 2.2rem;
      font-weight: 700;
      margin: 0.5rem 0;
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .stat-value.positive {
      color: #2ecc71;
    }

    .stat-value.negative {
      color: #e74c3c;
    }

    .stat-label {
      color: rgba(255,255,255,0.5);
      font-size: 0.85rem;
      font-weight: 500;
    }

    .charts-container {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
      gap: 1.5rem;
      margin-bottom: 2.5rem;
    }

    .chart-wrapper {
      background: linear-gradient(135deg, rgba(240,147,251,0.05), rgba(245,87,108,0.05));
      backdrop-filter: blur(10px);
      border: 1px solid rgba(245,87,108,0.2);
      border-radius: 16px;
      padding: 1.8rem;
      transition: all 0.3s;
    }

    .chart-wrapper:hover {
      border-color: rgba(245,87,108,0.4);
      box-shadow: 0 20px 40px rgba(245,87,108,0.15);
    }

    .chart-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.5rem;
    }

    .chart-header h2 {
      color: white;
      font-size: 1.3rem;
      font-weight: 700;
      margin: 0;
    }

    .chart-badge {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      color: white;
      padding: 0.4rem 0.8rem;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
    }

    .recent-backtests {
      background: linear-gradient(135deg, rgba(240,147,251,0.05), rgba(245,87,108,0.05));
      backdrop-filter: blur(10px);
      border: 1px solid rgba(245,87,108,0.2);
      border-radius: 16px;
      padding: 2rem;
    }

    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.5rem;
    }

    .section-header h2 {
      color: white;
      font-size: 1.4rem;
      font-weight: 700;
      margin: 0;
    }

    .count {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      color: white;
      padding: 0.5rem 1rem;
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 700;
    }

    .table-wrapper {
      overflow-x: auto;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      color: white;
    }

    th {
      background: rgba(240,147,251,0.1);
      color: rgba(255,255,255,0.9);
      padding: 1rem;
      text-align: left;
      font-weight: 700;
      font-size: 0.9rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 2px solid rgba(245,87,108,0.2);
    }

    td {
      padding: 1rem;
      border-bottom: 1px solid rgba(245,87,108,0.1);
      color: rgba(255,255,255,0.8);
    }

    tbody tr {
      transition: all 0.2s;
    }

    tbody tr:hover {
      background: rgba(245,87,108,0.05);
    }

    .date-cell {
      font-weight: 500;
      color: rgba(255,255,255,0.7);
    }

    .symbol-cell {
      font-weight: 700;
      color: #f5576c;
    }

    .badge-cell {
      text-align: center;
    }

    .badge-cell span {
      display: inline-block;
      padding: 0.4rem 0.8rem;
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 700;
    }

    .badge-high {
      background: rgba(46,204,113,0.2);
      color: #2ecc71;
    }

    .badge-mid {
      background: rgba(241,196,15,0.2);
      color: #f1c40f;
    }

    .badge-low {
      background: rgba(231,76,60,0.2);
      color: #e74c3c;
    }

    .positive {
      color: #2ecc71 !important;
      font-weight: 700;
    }

    .negative {
      color: #e74c3c !important;
      font-weight: 700;
    }

    @media (max-width: 768px) {
      .dashboard-header h1 {
        font-size: 1.8rem;
      }

      .stats-grid {
        grid-template-columns: 1fr;
      }

      .charts-container {
        grid-template-columns: 1fr;
      }
    }
  `]
})
export class DashboardComponent implements OnInit {
  userProfile: UserProfile | null = null;
  strategies: Strategy[] = [];
  backtests: BacktestResult[] = [];
  equityCurveChart: ChartConfiguration | null = null;
  performanceChart: ChartConfiguration | null = null;
  loading = true;

  constructor(
    private backtestService: BacktestService,
    private strategyService: StrategyService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.loadUserData();
  }

  loadUserData(): void {
    // Load user profile
    this.authService.getProfile().subscribe({
      next: (profile: UserProfile) => {
        this.userProfile = profile;
        this.loadStrategies();
        this.loadBacktests();
      },
      error: (error) => {
        console.error('Error loading profile:', error);
        this.loading = false;
      }
    });
  }

  loadStrategies(): void {
    this.strategyService.getAll().subscribe(
      (data: Strategy[]) => {
        this.strategies = data;
      },
      (error) => console.error('Error loading strategies:', error)
    );
  }

  loadBacktests(): void {
    this.backtestService.getHistory().subscribe({
      next: (results: BacktestResult[]) => {
        this.backtests = results.sort((a, b) => 
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
        this.setupCharts();
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading backtests:', error);
        this.loading = false;
      }
    });
  }

  getGreeting(): string {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 18) return 'Good afternoon';
    return 'Good evening';
  }

  setupCharts(): void {
    if (this.backtests.length > 0) {
      this.setupEquityCurveChart();
      this.setupPerformanceChart();
    }
  }

  setupEquityCurveChart(): void {
    const latestBacktest = this.backtests[0];
    if (!latestBacktest.equity_curve || latestBacktest.equity_curve.length === 0) {
      return;
    }

    this.equityCurveChart = {
      type: 'line',
      data: {
        labels: latestBacktest.equity_curve.map((_, i) => `Step ${i + 1}`),
        datasets: [
          {
            label: 'Equity Curve',
            data: latestBacktest.equity_curve,
            borderColor: '#f5576c',
            backgroundColor: 'rgba(245, 87, 108, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4,
            pointRadius: 0,
            pointHoverRadius: 6,
            pointBackgroundColor: '#f093fb',
            pointBorderColor: 'white',
            pointBorderWidth: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: false,
            ticks: {
              color: 'rgba(255,255,255,0.6)'
            },
            grid: {
              color: 'rgba(255,255,255,0.1)'
            }
          },
          x: {
            ticks: {
              color: 'rgba(255,255,255,0.6)'
            },
            grid: {
              color: 'rgba(255,255,255,0.05)'
            }
          }
        }
      }
    };
  }

  setupPerformanceChart(): void {
    const labels = this.backtests.slice(0, 10).map(b => (b as any).symbol);
    const data = this.backtests.slice(0, 10).map(b => (b as any).roi);

    this.performanceChart = {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'ROI',
            data,
            backgroundColor: data.map(d => d > 0 ? 'rgba(46, 204, 113, 0.7)' : 'rgba(231, 76, 60, 0.7)'),
            borderColor: data.map(d => d > 0 ? '#2ecc71' : '#e74c3c'),
            borderWidth: 1,
            borderRadius: 8
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        indexAxis: 'y' as const,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          x: {
            ticks: {
              color: 'rgba(255,255,255,0.6)'
            },
            grid: {
              color: 'rgba(255,255,255,0.1)'
            }
          },
          y: {
            ticks: {
              color: 'rgba(255,255,255,0.8)',
              font: {
                weight: 600 as any
              }
            },
            grid: {
              display: false
            }
          }
        }
      }
    };
  }

  getAverageROI(): number {
    if (this.backtests.length === 0) return 0;
    return this.backtests.reduce((acc, b) => acc + (b as any).roi, 0) / this.backtests.length;
  }

  getBestSharpeRatio(): number {
    if (this.backtests.length === 0) return 0;
    return Math.max(...this.backtests.map(b => (b as any).sharpe_ratio));
  }

  getAverageWinRate(): number {
    if (this.backtests.length === 0) return 0;
    return this.backtests.reduce((acc, b) => acc + (b as any).win_rate, 0) / this.backtests.length;
  }
}
