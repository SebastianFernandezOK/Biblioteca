import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class PrestamoService {
  constructor(private http: HttpClient) {}

  crearPrestamo(data: any) {
    return this.http.post('/api/prestamos', data);
  }

  getAllPrestamos(): Observable<any[]> {
    return this.http.get<any[]>('/api/prestamos');
  }

  devolverPrestamo(prestamoId: number) {
    return this.http.put(`/api/prestamos/${prestamoId}/devolver`, {});
  }

  getPrestamosPaginados(page: number, per_page: number, libro: string = ''): Observable<any> {
    let url = `/api/prestamos?page=${page}&per_page=${per_page}`;
    if (libro) {
      url += `&libro=${encodeURIComponent(libro)}`;
    }
    return this.http.get<any>(url);
  }

  actualizarEstadoPrestamo(prestamoId: number, estadoID: number) {
    return this.http.put(`/api/prestamos/${prestamoId}`, { estadoID });
  }

  actualizarFechasPrestamo(prestamoId: number, data: any) {
    return this.http.put(`/api/prestamos/${prestamoId}`, data);
  }

  getPrestamosByUsuarioPaginado(usuarioId: string, page: number, per_page: number): Observable<any> {
    return this.http.get<any>(`/api/prestamos/usuario/${usuarioId}?page=${page}&per_page=${per_page}`);
  }

  eliminarPrestamo(prestamoId: number) {
    return this.http.delete(`/api/prestamos/${prestamoId}`);
  }
}
