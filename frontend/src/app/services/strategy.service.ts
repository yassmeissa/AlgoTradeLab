import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Strategy {
  id?: number;
  name: string;
  type: 'mac' | 'rsi' | 'macd';
  parameters: Record<string, any>;
  description?: string;
  created_at?: string;
  updated_at?: string;
}

@Injectable({
  providedIn: 'root'
})
export class StrategyService {
  private apiUrl = 'http://localhost:8000/api/strategies';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Strategy[]> {
    return this.http.get<Strategy[]>(this.apiUrl);
  }

  getById(id: number): Observable<Strategy> {
    return this.http.get<Strategy>(`${this.apiUrl}/${id}`);
  }

  create(strategy: Strategy): Observable<Strategy> {
    return this.http.post<Strategy>(this.apiUrl, strategy);
  }

  update(id: number, strategy: Strategy): Observable<Strategy> {
    return this.http.put<Strategy>(`${this.apiUrl}/${id}`, strategy);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
