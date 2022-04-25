import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {AuthService} from "../auth.service";
import {ActivatedRoute, Router} from "@angular/router";
import {filter, Observable} from "rxjs";
import {WebcamImage} from "ngx-webcam";
import {CameraPopupComponent} from "../camera-popup/camera-popup.component";
import {MatDialog} from "@angular/material/dialog";
import {MatSnackBar} from "@angular/material/snack-bar";

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  public form!: FormGroup;
  public webcamImages: WebcamImage[] = [];
  constructor(private authService: AuthService,
              private router: Router,
              private route: ActivatedRoute,
              public dialog: MatDialog,
              private snackBar: MatSnackBar) { }

  ngOnInit(): void {
    this.createForm();
  }

  private createForm(): void {
    this.form = new FormGroup({
      username: new FormControl(null, [Validators.required]),
      password: new FormControl(null, [Validators.required])
    })
  }

  private openImageDialog(): Observable<WebcamImage> {
    return this.dialog.open(CameraPopupComponent).afterClosed().pipe(
      filter(r => !!r)
    );
  }

  public getImage() {
    this.openImageDialog().subscribe(img => {
      this.webcamImages.push(img);
    })
  }

  public signUp(): void {
    if(this.form.valid) {
      this.authService.signUp(this.form.value, this.webcamImages).subscribe(successRegistration => {
        if(successRegistration) {
          this.snackBar.open('Rejestracja przebiegla pomyslnie, proszę się zalogować!', 'OK');
          this.router.navigate(['../'], {relativeTo: this.route});
        } else {
          this.snackBar.open('Rejestracja nie powiodła się', 'OK');
        }
      })
    }
  }

  public deleteImage(i: number) {
    this.webcamImages.splice(i, 1);
  }
}
