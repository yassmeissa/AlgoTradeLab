import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface MarketData {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

@Injectable({
  providedIn: 'root'
})
export class MarketDataService {
  private apiUrl = 'http://localhost:8000/api/market-data';

  constructor(private http: HttpClient) {}

  getMarketData(
    symbol: string,
    startDate: string,
    endDate: string
  ): Observable<MarketData[]> {
    return this.http.get<MarketData[]>(
      `${this.apiUrl}/${symbol}`,
      {
        params: {
          start_date: startDate,
          end_date: endDate
        }
      }
    );
  }

  getSymbols(): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiUrl}/symbols`);
  }
}
