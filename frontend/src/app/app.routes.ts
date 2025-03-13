import { Routes } from '@angular/router';
import { ComponentComponent } from './component/component.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

export const routes: Routes = [
    {path:"e",component:ComponentComponent},
    {path:"**",component:PageNotFoundComponent}
];
