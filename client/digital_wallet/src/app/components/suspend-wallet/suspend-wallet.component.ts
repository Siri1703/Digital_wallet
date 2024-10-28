import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../api.service';

@Component({
  selector: 'app-suspend-wallet',
  templateUrl: './suspend-wallet.component.html',
  styleUrls: ['./suspend-wallet.component.css']
})
export class SuspendWalletComponent {
  walletId: string = '';

  constructor(private route: ActivatedRoute, private apiService: ApiService) {
    this.walletId = this.route.snapshot.paramMap.get('walletId') || '';
  }

  suspendWallet() {
    this.apiService.suspendWallet(this.walletId).subscribe(
      response => {
        alert('Wallet suspended successfully!');
      },
      error => {
        console.error("Error suspending wallet:", error);
      }
    );
  }
}
