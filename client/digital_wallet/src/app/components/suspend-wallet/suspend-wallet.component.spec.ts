import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SuspendWalletComponent } from './suspend-wallet.component';

describe('SuspendWalletComponent', () => {
  let component: SuspendWalletComponent;
  let fixture: ComponentFixture<SuspendWalletComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SuspendWalletComponent]
    });
    fixture = TestBed.createComponent(SuspendWalletComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
