import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {WebcamImage, WebcamInitError, WebcamUtil} from "ngx-webcam";
import {Observable, Subject} from "rxjs";
import {MatDialogRef} from "@angular/material/dialog";

@Component({
  selector: 'app-camera-popup',
  templateUrl: './camera-popup.component.html',
  styleUrls: ['./camera-popup.component.css']
})
export class CameraPopupComponent implements OnInit {

  public image!: WebcamImage;
  private isCameraExist = true;
  public  imageTaken = false;
  public loading = true;
  errors: WebcamInitError[] = [];
  private trigger: Subject<void> = new Subject<void>();
  private nextWebcam: Subject<boolean | string> = new Subject<boolean | string>();

  constructor(public dialogRef: MatDialogRef<CameraPopupComponent>,) { }


  ngOnInit(): void {
    WebcamUtil.getAvailableVideoInputs()
      .then((mediaDevices: MediaDeviceInfo[]) => {
        this.isCameraExist = mediaDevices && mediaDevices.length > 0;
      });
  }

  takeSnapshot(): void {
    this.trigger.next();
  }

  changeWebCame(directionOrDeviceId: boolean | string) {
    this.nextWebcam.next(directionOrDeviceId);
  }

  handleImage(webcamImage: WebcamImage) {
    this.image = webcamImage;
    this.imageTaken = true;
  }

  get triggerObservable(): Observable<void> {
    return this.trigger.asObservable();
  }

  get nextWebcamObservable(): Observable<boolean | string> {
    return this.nextWebcam.asObservable();
  }

  public cancel() {
    this.dialogRef.close();
  }


  public reset() {
    this.imageTaken = false;
  }

  public save() {
    this.dialogRef.close(this.image)
  }

  stopLoading() {
    this.loading = false;
  }
}
