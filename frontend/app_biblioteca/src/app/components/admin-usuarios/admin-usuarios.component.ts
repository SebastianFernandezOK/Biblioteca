import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-admin-usuarios',
  templateUrl: './admin-usuarios.component.html',
  styleUrls: ['./admin-usuarios.component.css']
})
export class AdminUsuariosComponent implements OnInit {
  usuarios: any[] = [];
  loading = true;
  error = '';
  editIndex: number | null = null;
  editUsuario: any = {};
  nuevoUsuario: any = {
    usuario_nombre: '',
    usuario_apellido: '',
    usuario_email: '',
    usuario_telefono: '',
    usuario_contrasena: '',
    rol: ''
  };
  creando = false;

  // Paginación
  page = 1;
  per_page = 5;
  total = 0;

  // Filtro
  filtroNombre: string = '';

  roles = [ 'admin', 'bibliotecario', 'usuario', 'suspendido' ];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.cargarUsuarios();
  }

  cargarUsuarios() {
    this.loading = true;
    let url = `/api/usuarios?page=${this.page}&per_page=${this.per_page}`;
    if (this.filtroNombre.trim()) {
      url += `&nombre=${encodeURIComponent(this.filtroNombre.trim())}`;
    }
    this.http.get<any>(url).subscribe({
      next: (data) => {
        this.usuarios = data.usuarios;
        this.total = data.total;
        this.loading = false;
      },
      error: () => { this.error = 'No se pudieron cargar los usuarios.'; this.loading = false; }
    });
  }

  aplicarFiltroNombre() {
    this.page = 1;
    this.cargarUsuarios();
  }

  cambiarPagina(delta: number) {
    this.page += delta;
    if (this.page < 1) this.page = 1;
    this.cargarUsuarios();
  }

  iniciarEdicion(i: number) {
    this.editIndex = i;
    this.editUsuario = { ...this.usuarios[i] };
  }

  cancelarEdicion() {
    this.editIndex = null;
    this.editUsuario = {};
  }

  guardarEdicion(i: number) {
    const id = this.usuarios[i].usuarioID;
    this.http.patch(`/api/usuarios/${id}`, this.editUsuario).subscribe({
      next: (data: any) => {
        this.usuarios[i] = data;
        this.cancelarEdicion();
      },
      error: () => { alert('Error al guardar cambios'); }
    });
  }

  eliminarUsuario(i: number) {
    if (!confirm('¿Seguro que deseas eliminar este usuario?')) return;
    const id = this.usuarios[i].usuarioID;
    this.http.delete(`/api/usuarios/${id}`).subscribe({
      next: () => { this.usuarios.splice(i, 1); },
      error: () => { alert('Error al eliminar usuario'); }
    });
  }

  crearUsuario() {
    this.creando = true;
    // Clonar y ajustar el objeto para usar la clave correcta con ñ
    const usuarioPayload = {
      ...this.nuevoUsuario,
      usuario_contraseña: this.nuevoUsuario.usuario_contrasena
    };
    delete usuarioPayload.usuario_contrasena;
    this.http.post('/api/usuarios', usuarioPayload).subscribe({
      next: (data: any) => {
        this.usuarios.push(data);
        this.nuevoUsuario = { usuario_nombre: '', usuario_apellido: '', usuario_email: '', usuario_telefono: '', usuario_contrasena: '', rol: '' };
        this.creando = false;
      },
      error: () => { alert('Error al crear usuario'); this.creando = false; }
    });
  }

  cambiarRol(i: number, nuevoRol: string) {
    const id = this.usuarios[i].usuarioID;
    this.http.patch(`/api/usuarios/${id}`, { rol: nuevoRol }).subscribe({
      next: (data: any) => { this.usuarios[i].rol = data.rol; },
      error: () => { alert('Error al cambiar rol'); }
    });
  }

  suspenderUsuario(i: number) {
    this.cambiarRol(i, 'suspendido');
  }

  get pageCount() {
    return Math.ceil(this.total / this.per_page);
  }
}
