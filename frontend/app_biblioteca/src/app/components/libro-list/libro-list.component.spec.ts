import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LibroListComponent } from './libro-list.component';

describe('LibroListComponent', () => {
  let component: LibroListComponent;
  let fixture: ComponentFixture<LibroListComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LibroListComponent]
    });
    fixture = TestBed.createComponent(LibroListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
