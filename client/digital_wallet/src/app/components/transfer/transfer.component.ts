import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../api.service';

@Component({
  selector: 'app-transfer',
  templateUrl: './transfer.component.html',
  styleUrls: ['./transfer.component.css']
})
export class TransferComponent {
  amount: number = 0;
  recipientWalletId: string = '';
  walletId: string = '';

  constructor(private route: ActivatedRoute, private apiService: ApiService) {
    this.walletId = this.route.snapshot.paramMap.get('walletId') || '';
  }

  transfer() {
    const transferData = { amount: this.amount, recipient_wallet_id: this.recipientWalletId };
    this.apiService.transfer(this.walletId, transferData).subscribe(
      response => {
        alert('Transfer successful!');
      },
      error => {
        console.error("Error transferring funds:", error);
      }
    );
  }
}
