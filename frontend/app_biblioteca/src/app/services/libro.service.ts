import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LibroService {
  private apiUrl = '/api/libros'; // Cambia la URL si tu endpoint es diferente

  constructor(private http: HttpClient) { }

  getLibros(page: number = 1, perPage: number = 10, search: string = '', generoID: string = ''): Observable<any> {
    let params = new HttpParams()
      .set('page', page)
      .set('per_page', perPage);
    if (search) {
      params = params.set('search', search);
    }
    if (generoID) {
      params = params.set('generoID', generoID);
    }
    return this.http.get<any>(this.apiUrl, { params });
  }

  getLibroById(id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}`);
  }

  actualizarCantidad(libroID: string, cantidad: number): Observable<any> {
    // PATCH al endpoint correcto
    return this.http.patch<any>(`${this.apiUrl}/${libroID}`, { cantidad });
  }

  actualizarLibro(libroID: string, datos: any): Observable<any> {
    // PUT para actualizar el libro completo
    return this.http.put<any>(`${this.apiUrl}/${libroID}`, datos);
  }

  agregarLibro(datos: any): Observable<any> {
    // POST para agregar un nuevo libro
    return this.http.post<any>(this.apiUrl, datos);
  }

  deleteById(libroID: string): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${libroID}`);
  }
}
