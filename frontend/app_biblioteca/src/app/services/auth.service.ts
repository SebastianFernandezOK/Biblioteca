import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private tokenKey = 'token';

  constructor(private http: HttpClient) {}

  login(credentials: { usuario_email: string; usuario_contraseña: string }): Observable<any> {
    return this.http.post<any>('/api/login', credentials).pipe(
      tap(res => {
        if (res.access_token) {
          localStorage.setItem(this.tokenKey, res.access_token);
        }
      })
    );
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem(this.tokenKey);
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  getUserEmail(): string | null {
    const token = this.getToken();
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.usuario_email || null;
    } catch {
      return null;
    }
  }

  getUserId(): string | null {
    const token = this.getToken();
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.sub ? payload.sub.toString() : null;
    } catch {
      return null;
    }
  }

  getUserRole(): string | null {
    const token = this.getToken();
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.rol || null;
    } catch {
      return null;
    }
  }

  get isBibliotecario(): boolean {
    const token = localStorage.getItem('token');
    if (!token) return false;
    // Decodificar el token y verificar el rol (ajusta según tu estructura de JWT)
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.rol === 'bibliotecario' || payload.rol === 'admin';
    } catch {
      return false;
    }
  }

  get isAdmin(): boolean {
    const token = localStorage.getItem('token');
    if (!token) return false;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.rol === 'admin';
    } catch {
      return false;
    }
  }

  forgotPassword(email: string): Observable<any> {
    return this.http.post('/api/auth/forgot-password', { email });
  }

  resetPassword(token: string, newPassword: string): Observable<any> {
    return this.http.post('/api/auth/reset-password', { token, new_password: newPassword });
  }
}
