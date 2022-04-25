import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login/login.component';
import {ReactiveFormsModule} from "@angular/forms";
import {MatCardModule} from "@angular/material/card";
import {WebcamModule} from "ngx-webcam";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import {MatButtonModule} from "@angular/material/button";
import { SignupComponent } from './signup/signup.component';
import { CameraPopupComponent } from './camera-popup/camera-popup.component';
import {MatDialogModule} from "@angular/material/dialog";
import {MatListModule} from "@angular/material/list";
import {MatIconModule} from "@angular/material/icon";
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import {MatSnackBarModule} from "@angular/material/snack-bar";




@NgModule({
  declarations: [
    LoginComponent,
    SignupComponent,
    CameraPopupComponent
  ],
  imports: [
    ReactiveFormsModule,
    MatCardModule,
    WebcamModule,
    CommonModule,
    MatFormFieldModule,
    MatSnackBarModule,
    MatInputModule,
    MatButtonModule,
    MatDialogModule,
    MatListModule,
    MatIconModule,
    MatProgressSpinnerModule
  ]
})
export class AuthModule { }
