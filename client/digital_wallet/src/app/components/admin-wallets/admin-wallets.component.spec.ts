import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminWalletsComponent } from './admin-wallets.component';

describe('AdminWalletsComponent', () => {
  let component: AdminWalletsComponent;
  let fixture: ComponentFixture<AdminWalletsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AdminWalletsComponent]
    });
    fixture = TestBed.createComponent(AdminWalletsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
