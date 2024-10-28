import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../api.service';

@Component({
  selector: 'app-transaction-history',
  templateUrl: './transaction-history.component.html',
  styleUrls: ['./transaction-history.component.css']
})
export class TransactionHistoryComponent {
  transactions: any[] = [];
  walletId: string = '';

  constructor(private route: ActivatedRoute, private apiService: ApiService) {
    this.walletId = this.route.snapshot.paramMap.get('walletId') || '';
    this.getTransactionHistory();
  }

  getTransactionHistory() {
    this.apiService.getTransactionHistory(this.walletId).subscribe(
      (data) => {
        this.transactions = data;
      },
      (error) => {
        console.error("Error fetching transaction history:", error);
      }
    );
  }
}
