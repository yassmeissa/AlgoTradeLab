import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink, Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink],
  template: `
    <div class="layout-container">
      <nav class="navbar">
        <div class="navbar-brand">
          <div class="brand-logo">₿</div>
          <h1>AlgoTrade</h1>
        </div>
        <div class="navbar-menu">
          <a routerLink="/dashboard" routerLinkActive="active" class="nav-link">
            <span class="nav-icon">📊</span>
            <span>Dashboard</span>
          </a>
          <a routerLink="/strategies" routerLinkActive="active" class="nav-link">
            <span class="nav-icon">⚙️</span>
            <span>Strategies</span>
          </a>
          <a routerLink="/backtests" routerLinkActive="active" class="nav-link">
            <span class="nav-icon">🧪</span>
            <span>Backtests</span>
          </a>
          <a routerLink="/analytics" routerLinkActive="active" class="nav-link">
            <span class="nav-icon">📈</span>
            <span>Analytics</span>
          </a>
          <button (click)="logout()" class="btn-logout">↗ Exit</button>
        </div>
      </nav>
      <main class="main-content">
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
  styles: [`
    :host {
      --primary: #f5576c;
      --secondary: #f093fb;
      --dark-bg: #0f0c29;
      --darker-bg: #302b63;
      --accent: #24243e;
    }

    .layout-container {
      display: flex;
      flex-direction: column;
      height: 100vh;
      background: linear-gradient(135deg, var(--dark-bg) 0%, var(--darker-bg) 50%, var(--accent) 100%);
    }

    .navbar {
      background: linear-gradient(90deg, rgba(15,12,41,0.95) 0%, rgba(48,43,99,0.95) 100%);
      backdrop-filter: blur(10px);
      color: white;
      padding: 1.2rem 2.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 10px 40px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1);
      border-bottom: 1px solid rgba(245,87,108,0.2);
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .navbar-brand {
      display: flex;
      align-items: center;
      gap: 1rem;
      cursor: pointer;
      transition: all 0.3s;
    }

    .navbar-brand:hover {
      transform: scale(1.05);
    }

    .brand-logo {
      font-size: 2rem;
      font-weight: 900;
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      filter: drop-shadow(0 2px 4px rgba(245,87,108,0.3));
    }

    .navbar-brand h1 {
      margin: 0;
      font-size: 1.5rem;
      font-weight: 700;
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      letter-spacing: 0.5px;
    }

    .navbar-menu {
      display: flex;
      gap: 0.3rem;
      align-items: center;
    }

    .nav-link {
      color: rgba(255,255,255,0.8);
      text-decoration: none;
      padding: 0.8rem 1.4rem;
      border-radius: 10px;
      cursor: pointer;
      font-weight: 600;
      font-size: 0.95rem;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      display: flex;
      align-items: center;
      gap: 0.6rem;
      position: relative;
      overflow: hidden;
    }

    .nav-link::before {
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(135deg, rgba(240,147,251,0.15), rgba(245,87,108,0.15));
      opacity: 0;
      transition: opacity 0.3s;
      border-radius: 10px;
    }

    .nav-link:hover::before,
    .nav-link.active::before {
      opacity: 1;
    }

    .nav-link:hover,
    .nav-link.active {
      color: white;
      box-shadow: 0 5px 20px rgba(245,87,108,0.3);
    }

    .nav-icon {
      font-size: 1.2rem;
      display: inline-block;
    }

    .btn-logout {
      background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
      color: white;
      border: none;
      padding: 0.8rem 1.6rem;
      border-radius: 10px;
      cursor: pointer;
      font-weight: 700;
      font-size: 0.95rem;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      display: flex;
      align-items: center;
      gap: 0.5rem;
      box-shadow: 0 5px 20px rgba(245,87,108,0.3);
      margin-left: 1rem;
    }

    .btn-logout:hover {
      transform: translateY(-3px);
      box-shadow: 0 8px 30px rgba(245,87,108,0.4);
    }

    .btn-logout:active {
      transform: translateY(-1px);
    }

    .main-content {
      flex: 1;
      overflow-y: auto;
      padding: 2.5rem;
    }

    .main-content::-webkit-scrollbar {
      width: 8px;
    }

    .main-content::-webkit-scrollbar-track {
      background: rgba(255,255,255,0.05);
    }

    .main-content::-webkit-scrollbar-thumb {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      border-radius: 4px;
    }

    .main-content::-webkit-scrollbar-thumb:hover {
      background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
    }

    @media (max-width: 768px) {
      .navbar {
        padding: 1rem 1.5rem;
        flex-wrap: wrap;
        gap: 1rem;
      }

      .navbar-menu {
        flex: 1;
        width: 100%;
        gap: 0.2rem;
        order: 3;
      }

      .nav-link span:not(.nav-icon) {
        display: none;
      }

      .nav-link {
        padding: 0.7rem 1rem;
      }

      .btn-logout {
        margin-left: 0;
      }

      .main-content {
        padding: 1.5rem;
      }
    }
  `]
})
export class LayoutComponent implements OnInit {
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {}

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
