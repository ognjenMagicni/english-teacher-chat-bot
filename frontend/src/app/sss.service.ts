import { Injectable,inject } from '@angular/core';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class SssService {
  eventSource = inject(EventSource);

  listen(url: string): Observable<string> {
    return new Observable(observer => {
      this.eventSource = new EventSource(url);
      this.eventSource.onmessage = (event) => observer.next(event.data);
      this.eventSource.onerror = (error) => observer.error(error);
      
      return () => this.eventSource.close();
    });
  }
}
