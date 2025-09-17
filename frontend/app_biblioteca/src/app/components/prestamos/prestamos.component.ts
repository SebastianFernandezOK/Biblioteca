import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { PrestamoService } from '../../services/prestamo.service';

@Component({
  selector: 'app-prestamos',
  templateUrl: './prestamos.component.html',
  styleUrls: ['./prestamos.component.css']
})
export class PrestamosComponent implements OnInit {
  prestamos: any[] = [];
  loading = true;
  error = '';
  page = 1;
  per_page = 5;
  total = 0;
  pages = 1;

  constructor(private authService: AuthService, private prestamoService: PrestamoService) {}

  ngOnInit(): void {
    this.cargarPagina(this.page);
  }

  cargarPagina(page: number) {
    const id = this.authService.getUserId();
    if (id) {
      this.loading = true;
      this.prestamoService.getPrestamosByUsuarioPaginado(id, page, this.per_page).subscribe({
        next: (data) => {
          this.prestamos = data.prestamos;
          this.total = data.total;
          this.page = data.page;
          this.pages = data.pages;
          this.loading = false;
        },
        error: () => {
          this.error = 'No se pudieron cargar los préstamos.';
          this.loading = false;
        }
      });
    } else {
      this.loading = false;
      this.error = 'No se pudo identificar el usuario.';
    }
  }

  actualizarEstado(prestamoId: number, estadoID: number) {
    this.prestamoService.actualizarEstadoPrestamo(prestamoId, estadoID).subscribe({
      next: () => {
        this.cargarPagina(this.page);
      },
      error: () => {
        this.error = 'No se pudo actualizar el estado del préstamo.';
      }
    });
  }

  actualizarFecha(prestamoId: number, campo: 'fecha_entrega' | 'fecha_devolucion', event: Event) {
    const input = event.target as HTMLInputElement;
    const valor = input.value;
    const body: any = {};
    body[campo] = valor;
    this.prestamoService.actualizarFechasPrestamo(prestamoId, body).subscribe({
      next: () => {
        this.cargarPagina(this.page);
      },
      error: () => {
        this.error = 'No se pudo actualizar la fecha del préstamo.';
      }
    });
  }

  cambiarPagina(nueva: number) {
    if (nueva >= 1 && nueva <= this.pages) {
      this.cargarPagina(nueva);
    }
  }
}
