import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../api.service';

@Component({
  selector: 'app-withdraw',
  templateUrl: './withdraw.component.html',
  styleUrls: ['./withdraw.component.css']
})
export class WithdrawComponent {
  amount: number = 0;
  walletId: string = '';

  constructor(private route: ActivatedRoute, private apiService: ApiService) {
    this.walletId = this.route.snapshot.paramMap.get('walletId') || '';
  }

  withdraw() {
    this.apiService.withdraw(this.walletId, this.amount).subscribe(
      response => {
        alert('Withdrawal successful!');
      },
      error => {
        console.error("Error withdrawing funds:", error);
      }
    );
  }
}
