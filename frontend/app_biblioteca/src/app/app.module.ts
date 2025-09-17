import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LibroListComponent } from './components/libro-list/libro-list.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { LibroDetalleComponent } from './components/libro-detalle/libro-detalle.component';
import { RegisterComponent } from './components/register/register.component';
import { LoginComponent } from './components/login/login.component';
import { ProfileComponent } from './components/profile/profile.component';
import { PrestamosComponent } from './components/prestamos/prestamos.component';
import { AdminLibrosComponent } from './components/admin-libros/admin-libros.component';
import { AuthInterceptor } from './services/auth.interceptor';
import { LoaderComponent } from './components/shared/loader.component';
import { ResenaComponent } from './components/resena/resena.component';
import { ForgotPasswordComponent } from './components/forgot-password/forgot-password.component';
import { ResetPasswordComponent } from './components/reset-password/reset-password.component';
import { EsperaAprobacionComponent } from './components/espera-aprobacion/espera-aprobacion.component';
import { AdminUsuariosComponent } from './components/admin-usuarios/admin-usuarios.component';

@NgModule({
  declarations: [
    AppComponent,
    LibroListComponent,
    NavbarComponent,
    LibroDetalleComponent,
    RegisterComponent,
    LoginComponent,
    ProfileComponent,
    PrestamosComponent,
    AdminLibrosComponent,
    LoaderComponent,
    ResenaComponent,
    ForgotPasswordComponent,
    ResetPasswordComponent,
    EsperaAprobacionComponent,
    AdminUsuariosComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
