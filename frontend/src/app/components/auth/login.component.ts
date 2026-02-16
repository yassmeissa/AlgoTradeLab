import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  template: `
    <div class="auth-container">
      <div class="auth-wrapper">
        <div class="auth-card">
          <div class="auth-header">
            <div class="logo">₿</div>
            <h1>AlgoTrade</h1>
            <p>Advanced Trading Strategy Backtester</p>
          </div>

          <form [formGroup]="loginForm" (ngSubmit)="onSubmit()" class="auth-form">
            <div class="form-group">
              <label>Email or Username</label>
              <input 
                type="text" 
                formControlName="emailOrUsername"
                placeholder="your@email.com or username"
                class="form-input"
              />
              <span *ngIf="loginForm.get('emailOrUsername')?.hasError('required') && loginForm.get('emailOrUsername')?.touched" class="error-msg">
                Email or username is required
              </span>
            </div>

            <div class="form-group">
              <label>Password</label>
              <input 
                type="password" 
                formControlName="password"
                placeholder="Enter your password"
                class="form-input"
              />
              <span *ngIf="loginForm.get('password')?.hasError('required') && loginForm.get('password')?.touched" class="error-msg">
                Password is required
              </span>
            </div>

            <span *ngIf="errorMessage" class="error-banner">{{ errorMessage }}</span>

            <button type="submit" class="btn-submit" [disabled]="!loginForm.valid">
              {{ isLoading ? 'Signing in...' : 'Sign In' }}
            </button>
          </form>

          <div class="auth-footer">
            <p>Don't have an account? <a routerLink="/register" class="link">Create one</a></p>
          </div>
        </div>

        <div class="auth-background"></div>
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

    .auth-container {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, var(--dark-bg) 0%, var(--darker-bg) 50%, var(--accent, #24243e) 100%);
      overflow: hidden;
      position: relative;
    }

    .auth-wrapper {
      width: 100%;
      max-width: 450px;
      z-index: 10;
      position: relative;
    }

    .auth-card {
      background: linear-gradient(135deg, rgba(15,12,41,0.8), rgba(48,43,99,0.8));
      backdrop-filter: blur(20px);
      border: 1px solid rgba(245,87,108,0.2);
      border-radius: 24px;
      padding: 3rem 2.5rem;
      box-shadow: 0 20px 60px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);
    }

    .auth-header {
      text-align: center;
      margin-bottom: 2.5rem;
    }

    .logo {
      font-size: 3rem;
      font-weight: 900;
      margin-bottom: 1rem;
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      filter: drop-shadow(0 2px 4px rgba(245,87,108,0.3));
    }

    .auth-header h1 {
      color: white;
      font-size: 2rem;
      font-weight: 700;
      margin: 0;
      letter-spacing: 0.5px;
    }

    .auth-header p {
      color: rgba(255,255,255,0.6);
      font-size: 0.95rem;
      margin: 0.5rem 0 0 0;
    }

    .auth-form {
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
      margin-bottom: 2rem;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    label {
      color: rgba(255,255,255,0.9);
      font-weight: 600;
      font-size: 0.95rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .form-input {
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(245,87,108,0.2);
      border-radius: 12px;
      padding: 0.9rem 1.2rem;
      color: white;
      font-size: 1rem;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .form-input::placeholder {
      color: rgba(255,255,255,0.4);
    }

    .form-input:focus {
      outline: none;
      background: rgba(255,255,255,0.08);
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(245,87,108,0.1);
    }

    .error-msg {
      color: #e74c3c;
      font-size: 0.85rem;
      font-weight: 500;
      margin-top: 0.25rem;
    }

    .error-banner {
      background: rgba(231,76,60,0.1);
      border: 1px solid rgba(231,76,60,0.3);
      color: #ff6b6b;
      padding: 1rem;
      border-radius: 10px;
      font-size: 0.9rem;
      text-align: center;
      font-weight: 500;
    }

    .btn-submit {
      background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
      color: white;
      border: none;
      padding: 1rem;
      border-radius: 12px;
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      box-shadow: 0 10px 30px rgba(245,87,108,0.3);
    }

    .btn-submit:hover:not(:disabled) {
      transform: translateY(-3px);
      box-shadow: 0 15px 40px rgba(245,87,108,0.4);
    }

    .btn-submit:active:not(:disabled) {
      transform: translateY(-1px);
    }

    .btn-submit:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }

    .auth-footer {
      text-align: center;
      color: rgba(255,255,255,0.7);
      font-size: 0.9rem;
    }

    .link {
      color: var(--primary);
      text-decoration: none;
      font-weight: 700;
      transition: all 0.2s;
    }

    .link:hover {
      color: var(--secondary);
      text-decoration: underline;
    }

    .auth-background {
      position: absolute;
      top: -50%;
      right: -20%;
      width: 500px;
      height: 500px;
      background: radial-gradient(circle, rgba(240,147,251,0.1) 0%, transparent 70%);
      border-radius: 50%;
      pointer-events: none;
    }

    @media (max-width: 768px) {
      .auth-card {
        padding: 2rem 1.5rem;
      }

      .auth-header h1 {
        font-size: 1.5rem;
      }

      .auth-form {
        gap: 1.2rem;
      }
    }
  `]
})
export class LoginComponent {
  loginForm: FormGroup;
  errorMessage = '';
  isLoading = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      emailOrUsername: ['', [Validators.required]],
      password: ['', [Validators.required]]
    });
  }

  onSubmit(): void {
    if (this.loginForm.invalid) return;

    this.isLoading = true;
    this.errorMessage = '';

    const { emailOrUsername, password } = this.loginForm.value;
    
    // Determine if it's email or username
    const isEmail = emailOrUsername.includes('@');
    const email = isEmail ? emailOrUsername : null;
    const username = !isEmail ? emailOrUsername : null;

    this.authService.login(email, password, username).subscribe({
      next: () => {
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.errorMessage = err.error?.message || 'Login failed. Please try again.';
        this.isLoading = false;
      }
    });
  }

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      emailOrUsername: ['', [Validators.required]],
      password: ['', [Validators.required]]
    });
  }
}

