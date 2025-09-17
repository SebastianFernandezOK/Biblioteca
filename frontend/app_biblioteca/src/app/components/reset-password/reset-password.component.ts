import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.css']
})
export class ResetPasswordComponent {
  resetForm: FormGroup;
  token: string = '';
  message: string = '';
  error: string = '';
  loading = false;

  constructor(
    private route: ActivatedRoute,
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.resetForm = this.fb.group({
      new_password: ['', [Validators.required, Validators.minLength(6)]]
    });
    this.token = this.route.snapshot.queryParamMap.get('token') || '';
  }

  onSubmit() {
    if (this.resetForm.invalid || !this.token) return;
    this.loading = true;
    this.authService.resetPassword(this.token, this.resetForm.value.new_password)
      .subscribe({
        next: res => {
          this.message = '¡Contraseña actualizada!';
          this.loading = false;
          setTimeout(() => this.router.navigate(['/login']), 2000);
        },
        error: err => {
          this.error = err.error?.message || 'Error al actualizar la contraseña.';
          this.loading = false;
        }
      });
  }
}
