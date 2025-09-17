import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ResenaService {
  constructor(private http: HttpClient) {}

  getResenasByLibro(libroID: number): Observable<any[]> {
    return this.http.get<any[]>(`/api/resenas/libro/${libroID}`);
  }

  crearResena(data: any) {
    return this.http.post('/api/resenas', data);
  }
}
