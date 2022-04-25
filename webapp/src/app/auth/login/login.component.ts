import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {WebcamImage} from "ngx-webcam";
import {AuthService} from "../auth.service";
import {MatDialog} from "@angular/material/dialog";
import {CameraPopupComponent} from "../camera-popup/camera-popup.component";
import {filter, Observable} from "rxjs";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  webcamImage: WebcamImage | undefined;
  form!: FormGroup;

  constructor(private fb: FormBuilder, private authService: AuthService, public dialog: MatDialog) { }

  ngOnInit(): void {
    this.createForm()
  }

  createForm(): void {
    this.form = new FormGroup({
      username: new FormControl('', []),
      password: new FormControl('')
    })
  }

  private openImageDialog(): Observable<WebcamImage> {
    return this.dialog.open(CameraPopupComponent).afterClosed().pipe(
      filter(r => !!r)
    );
  }

  public getImage() {
    this.openImageDialog().subscribe(img => {
      this.webcamImage = img;
    })
  }

  submit(): void {
    const img = this.webcamImage?.imageAsBase64;
    if (this.webcamImage !== undefined) {
      const loginData = this.form.value;
      this.authService.login(loginData, this.webcamImage);
    }

  }

}
