import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { LibroService } from '../../services/libro.service';
import { AuthService } from '../../services/auth.service';
import { PrestamoService } from '../../services/prestamo.service';
import { ResenaService } from '../../services/resena.service';

@Component({
  selector: 'app-libro-detalle',
  templateUrl: './libro-detalle.component.html',
  styleUrls: ['./libro-detalle.component.css']
})
export class LibroDetalleComponent implements OnInit {
  libro: any;
  loading = true;
  error = '';
  success: string = '';

  // Reseña
  valoracion: number = 0;
  comentario: string = '';
  resenaSuccess: string = '';
  resenaError: string = '';
  resenas: any[] = [];

  @Output() reseñaAgregada = new EventEmitter<void>();

  constructor(
    private route: ActivatedRoute,
    private libroService: LibroService,
    private location: Location,
    private authService: AuthService,
    private prestamoService: PrestamoService,
    private resenaService: ResenaService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.libroService.getLibroById(id).subscribe({
        next: (data) => {
          this.libro = data;
          this.loading = false;
          this.cargarResenas();
        },
        error: () => {
          this.error = 'No se pudo cargar el libro.';
          this.loading = false;
        }
      });
    }
  }

  cargarResenas() {
    if (!this.libro || !this.libro.libroID) return;
    this.resenaService.getResenasByLibro(this.libro.libroID).subscribe({
      next: (data) => { this.resenas = data; },
      error: () => { this.resenas = []; }
    });
  }

  enviarResena() {
    const usuarioID = this.authService.getUserId();
    if (!usuarioID) {
      this.resenaError = 'Debes iniciar sesión para reseñar.';
      return;
    }
    if (!this.valoracion || !this.comentario.trim()) {
      this.resenaError = 'Completa la valoración y el comentario.';
      return;
    }
    const data = {
      valoracion: this.valoracion,
      comentario: this.comentario,
      usuarioID: usuarioID,
      libroID: this.libro.libroID
    };
    this.resenaService.crearResena(data).subscribe({
      next: () => {
        this.resenaSuccess = 'Reseña enviada.';
        this.resenaError = '';
        this.valoracion = 0;
        this.comentario = '';
        this.cargarResenas(); // Recarga la lista de reseñas
      },
      error: () => {
        this.resenaError = 'No se pudo enviar la reseña.';
        this.resenaSuccess = '';
      }
    });
  }

  volver() {
    this.location.back();
  }

  pedirPrestamo() {
    if (!this.libro || this.libro.cantidad <= 0) {
      this.error = 'No hay ejemplares disponibles.';
      return;
    }
    const usuarioID = this.authService.getUserId();
    if (!usuarioID) {
      this.error = 'No se pudo identificar el usuario.';
      return;
    }
    const hoy = new Date();
    const fecha_entrega = hoy.toISOString().split('T')[0];
    const fecha_devolucion = new Date(hoy.getTime() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]; // 7 días después
    const data = {
      usuarioID: Number(usuarioID),
      libroID: this.libro.libroID,
      fecha_entrega,
      fecha_devolucion
    };
    this.prestamoService.crearPrestamo(data).subscribe({
      next: () => {
        this.success = 'Préstamo realizado correctamente.';
        this.error = '';
        this.libro.cantidad -= 1;
      },
      error: () => {
        this.error = 'No se pudo realizar el préstamo.';
        this.success = '';
      }
    });
  }

  getStarType(star: number, valoracion: number): string {
    return star <= Math.round(valoracion || 0) ? 'star' : 'star_border';
  }
}
