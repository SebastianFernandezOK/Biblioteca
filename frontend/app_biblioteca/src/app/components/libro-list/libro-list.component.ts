import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { LibroService } from '../../services/libro.service';
import { GeneroService } from '../../services/genero.service';
import { AuthService } from '../../services/auth.service';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-libro-list',
  templateUrl: './libro-list.component.html',
  styleUrls: ['./libro-list.component.css']
})
export class LibroListComponent implements OnInit {
  libros: any[] = [];
  generos: any[] = [];
  filtroGeneroID: string = '';
  filtroNombre: string = '';
  filtroAutor: string = '';
  page: number = 1;
  perPage: number = 10;
  totalPages: number = 1;
  total: number = 0;
  libroEditando: any = null;
  editForm: FormGroup;
  mostrarModalAgregar: boolean = false;
  agregarForm: FormGroup = this.fb.group({
    titulo: [''],
    editorial: [''],
    generoID: [''],
    cantidad: [0],
    image: [''],
    autor: ['']
  });
  selectedFile: File | null = null;

  constructor(
    private libroService: LibroService,
    private generoService: GeneroService,
    private router: Router,
    public authService: AuthService,
    private fb: FormBuilder
  ) {
    this.editForm = this.fb.group({
      titulo: [''],
      editorial: [''],
      generoID: [''],
      cantidad: [0],
      image: [''],
      autor: ['']
    });
  }

  ngOnInit(): void {
    this.generoService.getGeneros().subscribe(generos => {
      this.generos = generos;
    });
    this.getLibros();
  }

  getLibros(): void {
    this.libroService.getLibros(this.page, this.perPage, this.filtroNombre, this.filtroGeneroID, this.filtroAutor).subscribe(data => {
      this.libros = data.items;
      this.totalPages = data.pages;
      this.total = data.total;
    });
  }

  filtrarLibros(): void {
    this.page = 1;
    this.getLibros();
  }

  changePage(newPage: number): void {
    if (newPage >= 1 && newPage <= this.totalPages) {
      this.page = newPage;
      this.getLibros();
    }
  }

  onImgError(event: any) {
    event.target.src = 'assets/default-cover.png';
  }

  verDetalle(libro: any) {
    this.router.navigate(['/libros', libro.libroID]);
  }

  abrirAgregarLibro() {
    this.mostrarModalAgregar = true;
    this.agregarForm.reset();
  }

  abrirModalEditar(libro: any) {
    if (!libro) {
      alert('Error: No se pudo cargar el libro para editar.');
      return;
    }
    this.libroEditando = libro;
    this.editForm.patchValue({
      titulo: libro.titulo,
      editorial: libro.editorial,
      generoID: libro.generoID,
      cantidad: libro.cantidad,
      image: libro.image,
      autor: libro.autor
    });
  }

  cerrarModalEditar() {
    this.libroEditando = null;
    this.editForm.reset();
  }

  guardarEdicion() {
    if (!this.libroEditando) return;
    const datos = this.editForm.value;
    // Cambiar 'generoID' por 'genero' para compatibilidad con backend
    const datosCompatibles = {
      ...datos,
      genero: datos.generoID,
    };
    delete datosCompatibles.generoID;
    const formData = new FormData();
    formData.append('titulo', datosCompatibles.titulo);
    formData.append('editorial', datosCompatibles.editorial);
    formData.append('genero', datosCompatibles.genero);
    formData.append('cantidad', datosCompatibles.cantidad);
    formData.append('autor', datosCompatibles.autor);
    // Si se seleccionó una nueva imagen, la enviamos; si no, enviamos el nombre actual
    if (this.selectedFile) {
      formData.append('image', this.selectedFile);
    } else {
      formData.append('image', datosCompatibles.image);
    }
    this.libroService.actualizarLibro(this.libroEditando.libroID, formData).subscribe(() => {
      Object.assign(this.libroEditando, datosCompatibles);
      this.cerrarModalEditar();
      this.getLibros();
    });
  }

  cerrarModalAgregar() {
    this.mostrarModalAgregar = false;
    this.agregarForm.reset();
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    this.selectedFile = file ? file : null;
  }

  guardarNuevoLibro() {
    if (this.agregarForm.invalid) return;
    const titulo = this.agregarForm.get('titulo')?.value;
    const editorial = this.agregarForm.get('editorial')?.value;
    const genero = this.agregarForm.get('generoID')?.value;
    const cantidad = this.agregarForm.get('cantidad')?.value;
    const autor = this.agregarForm.get('autor')?.value;
    if (!titulo || !editorial || !genero || !cantidad || !this.selectedFile) {
      alert('Todos los campos y la imagen son obligatorios.');
      return;
    }
    const formData = new FormData();
    formData.append('titulo', titulo);
    formData.append('editorial', editorial);
    formData.append('genero', genero); // Cambiado a 'genero'
    formData.append('cantidad', cantidad);
    formData.append('autor', autor);
    formData.append('image', this.selectedFile);
    this.libroService.agregarLibro(formData).subscribe((nuevoLibro) => {
      this.getLibros();
      this.cerrarModalAgregar();
      this.selectedFile = null;
    });
  }

  eliminarLibro(libro: any) {
    if (!libro) return;
    // Si la cantidad es mayor a 1, restamos 1 y actualizamos
    if (libro.cantidad > 1) {
      this.libroService.actualizarCantidad(libro.libroID, libro.cantidad - 1).subscribe(() => {
        this.getLibros();
      });
    } else if (libro.cantidad === 1) {
      // Si la cantidad es 1, el backend lo eliminará
      this.libroService.actualizarCantidad(libro.libroID, 0).subscribe({
        next: () => {
          this.getLibros();
        },
        error: (err) => {
          if (err && err.error && err.error.message && err.error.message.includes('préstamos')) {
            alert('No se puede eliminar el libro porque tiene préstamos pendientes o activos.');
          } else {
            alert('No se pudo eliminar el libro.');
          }
        }
      });
    }
  }

  getStarType(star: number, valoracion: number): string {
    return star <= Math.round(valoracion || 0) ? 'star' : 'star_border';
  }
}
