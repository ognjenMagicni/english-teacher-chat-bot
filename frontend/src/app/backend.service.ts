import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Audio } from './audio.model';
@Injectable({
  providedIn: 'root'
})
export class BackendService {
  httpClient = inject(HttpClient)

  sendAudio(blob: Blob):Observable<string>{
    console.log("component sendAudio: started")
    let url = "http://localhost:8000/sendAudio"
    const formData = new FormData();
    formData.append('file', blob, 'recording.webm');
    return this.httpClient.post<string>(url,formData)
  }
  runBot():Observable<void>{
    console.log("component runBot: started")
    let url = "http://localhost:8000/runBot"
    return this.httpClient.post<void>(url,null)
  }
}
