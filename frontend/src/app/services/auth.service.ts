import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';

interface LoginRequest {
  email: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type?: string;
  expires_in?: number;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api/auth';
  private tokenSubject = new BehaviorSubject<string | null>(
    localStorage.getItem('token')
  );

  public token$ = this.tokenSubject.asObservable();

  constructor(private http: HttpClient) {}

  register(username: string, email: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, {
      email,
      username,
      password
    });
  }

  login(email: string | null, password: string, username: string | null = null): Observable<LoginResponse> {
    const body: any = { password };
    
    if (email) {
      body.email = email;
    } else if (username) {
      body.username = username;
    }
    
    return this.http.post<LoginResponse>(`${this.apiUrl}/login`, body).pipe(
      tap(response => {
        localStorage.setItem('token', response.access_token);
        this.tokenSubject.next(response.access_token);
      })
    );
  }

  logout(): void {
    localStorage.removeItem('token');
    this.tokenSubject.next(null);
  }

  getToken(): string | null {
    return this.tokenSubject.value;
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  getProfile(): Observable<any> {
    return this.http.get(`${this.apiUrl}/me`);
  }
}
