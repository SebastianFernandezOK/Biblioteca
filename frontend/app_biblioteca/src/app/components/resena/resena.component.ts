import { Component, Input, OnInit, OnChanges } from '@angular/core';
import { ResenaService } from '../../services/resena.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-resena',
  templateUrl: './resena.component.html',
  styleUrls: ['./resena.component.css']
})
export class ResenaComponent implements OnInit, OnChanges {
  @Input() libroID!: number;
  resenas: any[] = [];
  valoracion: number = 0;
  comentario: string = '';
  resenaSuccess: string = '';
  resenaError: string = '';

  constructor(private resenaService: ResenaService, private authService: AuthService) {}

  ngOnInit(): void {
    this.cargarResenas();
  }

  ngOnChanges(): void {
    this.cargarResenas();
  }

  cargarResenas() {
    if (!this.libroID) return;
    this.resenaService.getResenasByLibro(this.libroID).subscribe({
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
      libroID: this.libroID
    };
    this.resenaService.crearResena(data).subscribe({
      next: () => {
        this.resenaSuccess = 'Reseña enviada.';
        this.resenaError = '';
        this.valoracion = 0;
        this.comentario = '';
        this.cargarResenas();
      },
      error: (err) => {
        if (err.status === 403 && err.error && err.error.message) {
          this.resenaError = err.error.message;
        } else {
          this.resenaError = 'No se pudo enviar la reseña.';
        }
        this.resenaSuccess = '';
      }
    });
  }
}
