import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { PrestamoService } from '../../services/prestamo.service';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  usuario: any = null;
  error: string = '';
  prestamos: any[] = [];
  page = 1;
  per_page = 5;
  total = 0;
  pages = 1;
  profileForm: FormGroup;
  message: string = '';
  editMode: boolean = false;
  selectedImage: File | null = null;

  constructor(
    private authService: AuthService,
    private http: HttpClient,
    private router: Router,
    private prestamoService: PrestamoService,
    private fb: FormBuilder
  ) {
    this.profileForm = this.fb.group({
      usuario_nombre: [''],
      usuario_apellido: [''],
      usuario_email: [''],
      usuario_telefono: ['']
    });
  }

  ngOnInit(): void {
    const id = this.authService.getUserId();
    if (id) {
      this.http.get(`/api/usuarios/${id}`).subscribe({
        next: (data: any) => {
          this.usuario = data;
          this.profileForm.patchValue(data);
        },
        error: () => { this.error = 'No se pudo cargar el perfil.'; }
      });
      this.cargarPagina(this.page);
    } else {
      this.error = 'No se pudo identificar el usuario.';
    }
  }

  cargarPagina(page: number) {
    const id = this.authService.getUserId();
    if (id) {
      this.prestamoService.getPrestamosByUsuarioPaginado(id, page, this.per_page).subscribe({
        next: (data) => {
          this.prestamos = data.prestamos;
          this.total = data.total;
          this.page = data.page;
          this.pages = data.pages;
        },
        error: () => { this.error = 'No se pudieron cargar los préstamos.'; }
      });
    }
  }

  cambiarPagina(nueva: number) {
    if (nueva >= 1 && nueva <= this.pages) {
      this.cargarPagina(nueva);
    }
  }

  onEdit() {
    this.editMode = true;
    this.message = '';
    this.error = '';
    if (this.usuario) {
      this.profileForm.patchValue(this.usuario);
    }
  }

  onCancelEdit() {
    this.editMode = false;
    this.profileForm.patchValue(this.usuario);
    this.message = '';
    this.error = '';
  }

  onImageSelected(event: any) {
    if (event.target.files && event.target.files.length > 0) {
      this.selectedImage = event.target.files[0];
    }
  }

  onSubmit() {
    const id = this.authService.getUserId();
    const formData = new FormData();
    // Agregar los datos del formulario
    Object.entries(this.profileForm.value).forEach(([key, value]) => {
      formData.append(key, value as string);
    });
    // Agregar la imagen si se seleccionó
    if (this.selectedImage) {
      formData.append('image', this.selectedImage);
    }
    this.http.patch(`/api/usuarios/${id}`, formData).subscribe({
      next: (data: any) => {
        this.message = 'Datos actualizados correctamente.';
        this.editMode = false;
        this.selectedImage = null;
        this.usuario = { ...this.usuario, ...this.profileForm.value, image: data.image };
      },
      error: err => this.error = err.error?.message || 'Error al actualizar los datos.'
    });
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  getProfileImage(): string {
    if (this.usuario && this.usuario.image) {
      return '/api/uploads/users/' + this.usuario.image;
    }
    return 'assets/default-profile.png';
  }
}
