import { Component } from '@angular/core';
import { ApiService } from '../../api.service';

@Component({
  selector: 'app-admin-transactions',
  templateUrl: './admin-transactions.component.html',
  styleUrls: ['./admin-transactions.component.css']
})
export class AdminTransactionsComponent {
  transactions: any[] = [];
  transactionType: string = '';
  startDate: string = '';
  endDate: string = '';

  constructor(private apiService: ApiService) {
    this.getAdminTransactions();
  }

  getAdminTransactions() {
    this.apiService.getAdminTransactions(this.transactionType, this.startDate, this.endDate).subscribe(
      (data) => {
        this.transactions = data.transactions;
      },
      (error) => {
        console.error("Error fetching transactions:", error);
      }
    );
  }
}
