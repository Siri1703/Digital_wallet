import { Component } from '@angular/core';
import { ApiService } from '../../api.service';

@Component({
  selector: 'app-create-wallet',
  templateUrl: './create-wallet.component.html',
  styleUrls: ['./create-wallet.component.css']
})
export class CreateWalletComponent {
  walletName: string = '';
  userId: string = '';
  email: string = '';
  contact: number = 0;
  balance: number = 0;
  walletId: number = 0;

  constructor(private apiService: ApiService) {}

  createWallet() {
    const walletData = { name: this.walletName, user_id: this.userId, email: this.email, contact: this.contact, balance: this.balance, status:'active', created_at:Date.now(), wallet_id:this.walletId };
    this.apiService.createWallet(walletData).subscribe(
      (response) => {
        alert('Wallet created successfully!');
      },
      (      error: any) => {
        console.error("Error creating wallet:", error);
        alert(error.error.detail)
      }
    );
  }
}
