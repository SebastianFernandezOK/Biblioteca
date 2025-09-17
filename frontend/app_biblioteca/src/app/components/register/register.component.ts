import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  registerForm: FormGroup;
  error: string = '';
  success: string = '';

  constructor(private fb: FormBuilder, private http: HttpClient, private router: Router) {
    this.registerForm = this.fb.group({
      usuario_nombre: ['', Validators.required],
      usuario_apellido: ['', Validators.required],
      usuario_contraseña: ['', Validators.required],
      usuario_email: ['', [Validators.required, Validators.email]],
      usuario_telefono: ['', Validators.required]
      // No enviar rol
    });
  }

  onSubmit() {
    if (this.registerForm.valid) {
      this.http.post('/api/usuarios', this.registerForm.value).subscribe({
        next: () => {
          this.success = 'Usuario registrado correctamente';
          this.error = '';
          this.router.navigate(['/login']);
        },
        error: (err) => {
          this.error = err.error?.message || 'Error al registrar usuario';
          this.success = '';
        }
      });
    }
  }
}
