import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { StrategyService, Strategy } from '../../services/strategy.service';

@Component({
  selector: 'app-strategies',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  template: `
    <div class="strategies-container">
      <div class="header">
        <h1>Trading Strategies</h1>
        <button (click)="toggleForm()" class="btn-primary">
          {{ showForm ? 'Cancel' : 'New Strategy' }}
        </button>
      </div>

      <div *ngIf="showForm" class="form-section">
        <h2>{{ editingId ? 'Edit' : 'Create' }} Strategy</h2>
        <form [formGroup]="strategyForm" (ngSubmit)="onSubmit()">
          <div class="form-group">
            <label for="name">Strategy Name</label>
            <input
              type="text"
              id="name"
              formControlName="name"
              class="form-control"
              placeholder="e.g., MA Crossover Strategy"
            />
          </div>

          <div class="form-group">
            <label for="type">Strategy Type</label>
            <select id="type" formControlName="type" class="form-control">
              <option value="">Select a type</option>
              <option value="mac">Moving Average Crossover</option>
              <option value="rsi">RSI</option>
              <option value="macd">MACD</option>
            </select>
          </div>

          <div class="form-group">
            <label for="description">Description</label>
            <textarea
              id="description"
              formControlName="description"
              class="form-control"
              rows="3"
              placeholder="Describe your strategy..."
            ></textarea>
          </div>

          <div class="parameters-section">
            <h3>Parameters</h3>
            <div formGroupName="parameters">
              <div *ngIf="selectedStrategyType === 'mac'" class="param-group">
                <div class="form-group">
                  <label for="fast_period">Fast Period</label>
                  <input
                    type="number"
                    id="fast_period"
                    formControlName="fast_period"
                    class="form-control"
                    min="1"
                  />
                </div>
                <div class="form-group">
                  <label for="slow_period">Slow Period</label>
                  <input
                    type="number"
                    id="slow_period"
                    formControlName="slow_period"
                    class="form-control"
                    min="1"
                  />
                </div>
              </div>

              <div *ngIf="selectedStrategyType === 'rsi'" class="param-group">
                <div class="form-group">
                  <label for="rsi_period">RSI Period</label>
                  <input
                    type="number"
                    id="rsi_period"
                    formControlName="rsi_period"
                    class="form-control"
                    min="1"
                  />
                </div>
                <div class="form-group">
                  <label for="oversold_threshold">Oversold Threshold</label>
                  <input
                    type="number"
                    id="oversold_threshold"
                    formControlName="oversold_threshold"
                    class="form-control"
                    min="0"
                    max="100"
                  />
                </div>
                <div class="form-group">
                  <label for="overbought_threshold">Overbought Threshold</label>
                  <input
                    type="number"
                    id="overbought_threshold"
                    formControlName="overbought_threshold"
                    class="form-control"
                    min="0"
                    max="100"
                  />
                </div>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" [disabled]="strategyForm.invalid" class="btn-success">
              {{ editingId ? 'Update' : 'Create' }}
            </button>
            <button type="button" (click)="resetForm()" class="btn-secondary">
              Reset
            </button>
          </div>
        </form>
      </div>

      <div class="strategies-grid">
        <div *ngIf="strategies.length === 0 && !showForm" class="empty-state">
          <p>No strategies found. Create one to get started!</p>
        </div>

        <div *ngFor="let strategy of strategies" class="strategy-card">
          <div class="card-header">
            <h3>{{ strategy.name }}</h3>
            <span class="strategy-type">{{ getStrategyTypeName(strategy.type) }}</span>
          </div>

          <div class="card-body">
            <p *ngIf="strategy.description" class="description">
              {{ strategy.description }}
            </p>

            <div class="parameters">
              <h4>Parameters:</h4>
              <ul>
                <li *ngFor="let key of getParameterKeys(strategy.parameters)">
                  {{ key }}: {{ strategy.parameters[key] }}
                </li>
              </ul>
            </div>

            <div class="dates">
              <small>Created: {{ strategy.created_at | date: 'short' }}</small>
            </div>
          </div>

          <div class="card-footer">
            <button (click)="editStrategy(strategy)" class="btn-small btn-primary">
              Edit
            </button>
            <button (click)="deleteStrategy(strategy.id!)" class="btn-small btn-danger">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .strategies-container {
      padding: 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }

    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2rem;
    }

    .header h1 {
      color: #1a237e;
      margin: 0;
    }

    .form-section {
      background: white;
      padding: 2rem;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      margin-bottom: 2rem;
    }

    .form-section h2 {
      color: #1a237e;
      margin-top: 0;
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

    .parameters-section {
      background: #f5f5f5;
      padding: 1rem;
      border-radius: 4px;
      margin: 1rem 0;
    }

    .parameters-section h3 {
      margin-top: 0;
      color: #1a237e;
    }

    .param-group {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
    }

    .form-actions {
      display: flex;
      gap: 1rem;
      margin-top: 1.5rem;
    }

    .btn-primary, .btn-success, .btn-secondary, .btn-danger, .btn-small {
      padding: 0.75rem 1.5rem;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.3s;
    }

    .btn-primary, .btn-success {
      background-color: #667eea;
      color: white;
    }

    .btn-primary:hover, .btn-success:hover {
      background-color: #5568d3;
    }

    .btn-secondary {
      background-color: #999;
      color: white;
    }

    .btn-secondary:hover {
      background-color: #777;
    }

    .btn-danger {
      background-color: #d32f2f;
      color: white;
    }

    .btn-danger:hover {
      background-color: #b71c1c;
    }

    .btn-small {
      padding: 0.5rem 1rem;
      font-size: 0.875rem;
    }

    .btn-primary:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }

    .strategies-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 1.5rem;
    }

    .empty-state {
      grid-column: 1 / -1;
      text-align: center;
      padding: 3rem;
      color: #999;
    }

    .strategy-card {
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    .card-header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 1rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .card-header h3 {
      margin: 0;
      font-size: 1.1rem;
    }

    .strategy-type {
      background: rgba(255,255,255,0.3);
      padding: 0.25rem 0.75rem;
      border-radius: 20px;
      font-size: 0.875rem;
      font-weight: 500;
    }

    .card-body {
      padding: 1rem;
      flex: 1;
    }

    .description {
      margin: 0 0 1rem 0;
      color: #666;
      font-size: 0.95rem;
    }

    .parameters {
      margin: 1rem 0;
    }

    .parameters h4 {
      margin: 0 0 0.5rem 0;
      color: #1a237e;
      font-size: 0.95rem;
    }

    .parameters ul {
      margin: 0;
      padding-left: 1.5rem;
      list-style: none;
    }

    .parameters li {
      color: #666;
      font-size: 0.9rem;
      padding: 0.25rem 0;
    }

    .dates {
      color: #999;
      font-size: 0.85rem;
      margin-top: 1rem;
    }

    .card-footer {
      border-top: 1px solid #e0e0e0;
      padding: 1rem;
      display: flex;
      gap: 0.5rem;
    }

    .card-footer button {
      flex: 1;
    }
  `]
})
export class StrategiesComponent implements OnInit {
  strategies: Strategy[] = [];
  strategyForm!: FormGroup;
  showForm = false;
  editingId: number | null = null;
  selectedStrategyType: string | null = null;

  constructor(
    private strategyService: StrategyService,
    private fb: FormBuilder
  ) {}

  ngOnInit(): void {
    this.initializeForm();
    this.loadStrategies();
  }

  initializeForm(): void {
    this.strategyForm = this.fb.group({
      name: ['', Validators.required],
      type: ['', Validators.required],
      description: [''],
      parameters: this.fb.group({
        fast_period: [20],
        slow_period: [50],
        rsi_period: [14],
        oversold_threshold: [30],
        overbought_threshold: [70]
      })
    });

    this.strategyForm.get('type')?.valueChanges.subscribe(value => {
      this.selectedStrategyType = value;
    });
  }

  loadStrategies(): void {
    this.strategyService.getAll().subscribe({
      next: (strategies) => {
        this.strategies = strategies;
      },
      error: (error) => {
        console.error('Error loading strategies:', error);
      }
    });
  }

  onSubmit(): void {
    if (this.strategyForm.invalid) return;

    const formValue = this.strategyForm.value;
    const strategy: Strategy = {
      name: formValue.name,
      type: formValue.type,
      description: formValue.description,
      parameters: {
        [this.getParameterKeyByType(formValue.type, 'first')]: formValue.parameters[this.getParameterKeyByType(formValue.type, 'first')],
        [this.getParameterKeyByType(formValue.type, 'second')]: formValue.parameters[this.getParameterKeyByType(formValue.type, 'second')],
        ...(formValue.type === 'rsi' && {
          oversold_threshold: formValue.parameters.oversold_threshold,
          overbought_threshold: formValue.parameters.overbought_threshold
        })
      }
    };

    if (this.editingId) {
      this.strategyService.update(this.editingId, strategy).subscribe({
        next: () => {
          this.loadStrategies();
          this.toggleForm();
        },
        error: (error) => console.error('Error updating strategy:', error)
      });
    } else {
      this.strategyService.create(strategy).subscribe({
        next: () => {
          this.loadStrategies();
          this.toggleForm();
        },
        error: (error) => console.error('Error creating strategy:', error)
      });
    }
  }

  editStrategy(strategy: Strategy): void {
    this.editingId = strategy.id || null;
    this.strategyForm.patchValue(strategy);
    this.showForm = true;
  }

  deleteStrategy(id: number): void {
    if (confirm('Are you sure you want to delete this strategy?')) {
      this.strategyService.delete(id).subscribe({
        next: () => {
          this.loadStrategies();
        },
        error: (error) => console.error('Error deleting strategy:', error)
      });
    }
  }

  toggleForm(): void {
    this.showForm = !this.showForm;
    if (!this.showForm) {
      this.resetForm();
    }
  }

  resetForm(): void {
    this.strategyForm.reset();
    this.editingId = null;
    this.selectedStrategyType = null;
  }

  getStrategyTypeName(type: string): string {
    const typeNames: Record<string, string> = {
      mac: 'Moving Average Crossover',
      rsi: 'RSI',
      macd: 'MACD'
    };
    return typeNames[type] || type;
  }

  getParameterKeys(parameters: Record<string, any>): string[] {
    return Object.keys(parameters);
  }

  getParameterKeyByType(type: string, position: string): string {
    const keys: Record<string, Record<string, string>> = {
      mac: { first: 'fast_period', second: 'slow_period' },
      rsi: { first: 'rsi_period', second: 'rsi_period' },
      macd: { first: 'fast_period', second: 'slow_period' }
    };
    return keys[type]?.[position] || '';
  }
}
