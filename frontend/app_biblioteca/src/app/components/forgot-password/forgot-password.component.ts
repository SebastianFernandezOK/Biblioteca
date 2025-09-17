import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css']
})
export class ForgotPasswordComponent {
  email = '';
  message = '';
  error = '';

  constructor(private auth: AuthService) {}

  submit() {
    this.auth.forgotPassword(this.email).subscribe({
      next: () => this.message = '¡Revisa tu correo para el enlace de recuperación!',
      error: err => this.error = err.error.message || 'Error al enviar el correo'
    });
  }
}
