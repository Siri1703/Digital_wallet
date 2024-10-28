import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../api.service';

@Component({
  selector: 'app-deposit',
  templateUrl: './deposit.component.html',
  styleUrls: ['./deposit.component.css']
})
export class DepositComponent {
  amount: number = 0;
  walletId: string = '';

  constructor(private route: ActivatedRoute, private apiService: ApiService) {
    this.walletId = this.route.snapshot.paramMap.get('walletId') || '';
  }

  deposit() {
    console.log(this.amount);
    
    this.apiService.deposit(this.walletId, this.amount).subscribe(
      response => {
        alert('Deposit successful!');
      },
      error => {
        console.error("Error depositing funds:", error);
      }
    );
  }
}
