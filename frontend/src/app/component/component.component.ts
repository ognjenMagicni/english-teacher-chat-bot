import { Component,inject, OnInit } from "@angular/core";
import { CommonModule, NgIf } from "@angular/common";
import { BackendService } from "../backend.service";
import { Audio } from "../audio.model";
import { SssService } from "../sss.service";
@Component({
  selector: 'app-component',
  imports: [NgIf,CommonModule],
  templateUrl: './component.component.html',
  styleUrl: './component.component.css'
})

export class ComponentComponent{
  private mediaRecorder!: MediaRecorder;
  private audioChunks: Blob[] = [];
  public audioUrl: string | null = null;
  public audioBlob: Blob | null = null;
  public isRecording = false;
  public downloadBool = false
  message?:string|null

  backendService = inject(BackendService)

  async startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);
      this.audioChunks = [];
      this.isRecording = true;

      this.mediaRecorder.ondataavailable = event => {
        this.audioChunks.push(event.data);
      };

      this.mediaRecorder.onstop = () => {
        this.audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
        this.audioUrl = URL.createObjectURL(this.audioBlob);
      };

      this.mediaRecorder.start();
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  }

  stopRecording() {
    if (this.mediaRecorder && this.isRecording) {
      this.mediaRecorder.stop();
      this.isRecording = false;
      this.downloadBool = true;
    }
  }

  downloadRecording() {
    if (this.audioBlob) {
      this.backendService.sendAudio(this.audioBlob).subscribe(payload=>{
        this.message = payload
        console.log(payload)
      })
    }
  }


  
}
