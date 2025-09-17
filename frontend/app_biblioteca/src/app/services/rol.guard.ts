import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from './auth.service';

@Injectable({ providedIn: 'root' })
export class RolGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(): boolean {
    const rol = this.authService.getUserRole();
    const rolesValidos = ['usuario', 'admin', 'bibliotecario'];
    if (!rol || !rolesValidos.includes(rol)) {
      this.router.navigate(['/espera-aprobacion']);
      return false;
    }
    return true;
  }
}
