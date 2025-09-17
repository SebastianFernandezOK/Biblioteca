import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  usuario: any = null;
  menuAbierto = false;

  constructor(public authService: AuthService, private router: Router, private http: HttpClient) {}

  ngOnInit(): void {
    const id = this.authService.getUserId();
    if (id) {
      this.http.get(`/api/usuarios/${id}`).subscribe({
        next: (data: any) => {
          this.usuario = data;
        },
        error: () => {}
      });
    }
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  isBibliotecario(): boolean {
    const role = this.authService.getUserRole();
    return role === 'bibliotecario';
  }

  isAdmin(): boolean {
    const role = this.authService.getUserRole();
    return role === 'admin';
  }

  getProfileImage(): string {
    if (this.usuario && this.usuario.image) {
      return '/api/uploads/users/' + this.usuario.image;
    }
    return 'assets/default-profile.png';
  }

  toggleMenu() {
    this.menuAbierto = !this.menuAbierto;
  }

  cerrarMenu() {
    this.menuAbierto = false;
  }
}
