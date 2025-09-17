import { Injectable, NgZone } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({ providedIn: 'root' })
export class InactivityService {
  private timeout: any;
  private readonly maxInactivity = 15 * 60 * 1000; // 15 minutos

  constructor(private router: Router, private ngZone: NgZone) {
    this.resetTimer();
    window.addEventListener('mousemove', () => this.resetTimer());
    window.addEventListener('keydown', () => this.resetTimer());
    window.addEventListener('click', () => this.resetTimer());
  }

  resetTimer() {
    clearTimeout(this.timeout);
    this.timeout = setTimeout(() => {
      localStorage.removeItem('token');
      this.ngZone.run(() => this.router.navigate(['/login']));
    }, this.maxInactivity);
  }
}
