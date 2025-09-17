import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LibroListComponent } from './components/libro-list/libro-list.component';
import { LibroDetalleComponent } from './components/libro-detalle/libro-detalle.component';
import { RegisterComponent } from './components/register/register.component';
import { LoginComponent } from './components/login/login.component';
import { AuthGuard } from './guards/auth.guard';
import { ProfileComponent } from './components/profile/profile.component';
import { PrestamosComponent } from './components/prestamos/prestamos.component';
import { AdminLibrosComponent } from './components/admin-libros/admin-libros.component';
import { ForgotPasswordComponent } from './components/forgot-password/forgot-password.component';
import { ResetPasswordComponent } from './components/reset-password/reset-password.component';
import { RolGuard } from './services/rol.guard';
import { EsperaAprobacionComponent } from './components/espera-aprobacion/espera-aprobacion.component';
import { AdminUsuariosComponent } from './components/admin-usuarios/admin-usuarios.component';

const routes: Routes = [
  { path: 'libros', component: LibroListComponent, canActivate: [AuthGuard, RolGuard] },
  { path: 'libros/:id', component: LibroDetalleComponent, canActivate: [AuthGuard, RolGuard] },
  { path: 'prestamos', component: PrestamosComponent, canActivate: [AuthGuard, RolGuard] },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'profile', component: ProfileComponent, canActivate: [AuthGuard, RolGuard] },
  { path: 'admin-libros', component: AdminLibrosComponent, canActivate: [AuthGuard, RolGuard] },
  { path: 'admin-usuarios', component: AdminUsuariosComponent, canActivate: [AuthGuard, RolGuard] },
  { path: 'forgot-password', component: ForgotPasswordComponent },
  { path: 'reset-password', component: ResetPasswordComponent },
  { path: 'espera-aprobacion', component: EsperaAprobacionComponent },
  { path: '', redirectTo: '/libros', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
