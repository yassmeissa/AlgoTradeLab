import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface BacktestRequest {
  strategy_id: number;
  symbol: string;
  start_date: string;
  end_date: string;
  initial_capital: number;
}

export interface BacktestMetrics {
  total_return: number;
  roi: number;
  sharpe_ratio: number;
  max_drawdown: number;
  win_rate: number;
  total_trades: number;
  profit_factor: number;
}

export interface BacktestResult {
  id: number;
  strategy_id: number;
  symbol: string;
  start_date: string;
  end_date: string;
  metrics: BacktestMetrics;
  equity_curve: number[];
  trades: any[];
  created_at: string;
}

@Injectable({
  providedIn: 'root'
})
export class BacktestService {
  private apiUrl = 'http://localhost:8000/api/backtests';

  constructor(private http: HttpClient) {}

  runBacktest(request: BacktestRequest): Observable<BacktestResult> {
    return this.http.post<BacktestResult>(`${this.apiUrl}/run`, request);
  }

  getResult(id: number): Observable<BacktestResult> {
    return this.http.get<BacktestResult>(`${this.apiUrl}/${id}`);
  }

  getHistory(): Observable<BacktestResult[]> {
    return this.http.get<BacktestResult[]>(`${this.apiUrl}/`);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
