import { Component, OnInit } from '@angular/core';
import { PrestamoService } from '../../services/prestamo.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-admin-libros',
  templateUrl: './admin-libros.component.html',
  styleUrls: ['./admin-libros.component.css']
})
export class AdminLibrosComponent implements OnInit {
  prestamos: any[] = [];
  loading = true;
  error = '';
  page = 1;
  per_page = 6;
  total = 0;
  pages = 1;

  constructor(private prestamoService: PrestamoService, public authService: AuthService) {}

  ngOnInit() {
    this.cargarPagina(this.page);
  }

  cargarPagina(page: number) {
    this.loading = true;
    this.prestamoService.getPrestamosPaginados(page, this.per_page).subscribe({
      next: (data) => {
        this.prestamos = data.prestamos;
        this.total = data.total;
        this.page = data.page;
        this.pages = data.pages;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error al cargar préstamos';
        this.loading = false;
      }
    });
  }

  siguientePagina() {
    if (this.page < this.pages) {
      this.cargarPagina(this.page + 1);
    }
  }

  anteriorPagina() {
    if (this.page > 1) {
      this.cargarPagina(this.page - 1);
    }
  }

  marcarDevuelto(prestamo: any) {
    this.prestamoService.devolverPrestamo(prestamo.prestamoID).subscribe({
      next: (actualizado: any) => {
        prestamo.fecha_devuelta = actualizado.fecha_devuelta;
        prestamo.estadoID = 3; // Devuelto
        prestamo.estado_nombre = actualizado.estado_nombre;
        // Opcional: mostrar feedback visual
      },
      error: () => {
        // Opcional: mostrar error
      }
    });
  }

  cambiarEstado(prestamo: any) {
    this.prestamoService.actualizarEstadoPrestamo(prestamo.prestamoID, prestamo.estadoID).subscribe({
      next: (actualizado: any) => {
        prestamo.estado_nombre = actualizado.estado_nombre;
        prestamo.estadoID = actualizado.estadoID;
        // Opcional: feedback visual
      },
      error: () => {
        // Opcional: mostrar error
      }
    });
  }

  actualizarFecha(prestamo: any, campo: 'fecha_entrega' | 'fecha_devolucion', event: Event) {
    const input = event.target as HTMLInputElement;
    const valor = input.value;
    const body: any = {};
    body[campo] = valor;
    this.prestamoService.actualizarFechasPrestamo(prestamo.prestamoID, body).subscribe({
      next: () => {
        prestamo[campo] = valor;
      },
      error: () => {
        this.error = 'No se pudo actualizar la fecha del préstamo.';
      }
    });
  }
}
