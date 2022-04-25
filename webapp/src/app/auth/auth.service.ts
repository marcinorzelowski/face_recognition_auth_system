import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {WebcamImage} from "ngx-webcam";
import {Observable} from "rxjs";
import {SignUpData} from "../common/model/auth-model";


export interface UserLoginData {
  username: string,
  password: string
}
@Injectable({
  providedIn: 'root'
})
export class AuthService {

  url = 'http://localhost:8080'
  constructor(private http: HttpClient) { }


  public login(user: UserLoginData, image: WebcamImage) {

    const file = this.createFileFromImage(image);
    const formData = new FormData();
    formData.append('user', JSON.stringify(user))
    formData.append('image', file, 'image');
    this.http.post(this.url + '/authenticate', formData).subscribe(x => console.log(x))
  }

  public signUp(user: any, images: WebcamImage[]): Observable<boolean> {
    const formData = new FormData();
    const files = images.map(img => this.createFileFromImage(img));
    formData.append('user',  JSON.stringify(user));
    files.forEach(x => formData.append('images', x));
    return this.http.post<boolean>(this.url + '/signup', formData);

  }

  private createFileFromImage(img: WebcamImage): File {
    const base64 = img.imageAsBase64;
    const imageName = 'name.png';
    const imageBlob = this.dataURItoBlob(base64);
    return new File([imageBlob], imageName, { type: 'image/png' });
  }

  // public signUp(form: any): Observable<SignUpData> {
  //   return this.http.post<SignUpData>(this.url + '/signup', form);
  // }

  dataURItoBlob(dataURI: string) {
    const byteString = window.atob(dataURI);
    const arrayBuffer = new ArrayBuffer(byteString.length);
    const int8Array = new Uint8Array(arrayBuffer);
    for (let i = 0; i < byteString.length; i++) {
      int8Array[i] = byteString.charCodeAt(i);
    }
    const blob = new Blob([int8Array], { type: 'image/png' });
    return blob;
  }

}
