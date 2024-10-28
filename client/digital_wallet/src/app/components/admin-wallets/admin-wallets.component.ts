import { Component } from '@angular/core';
import { ApiService } from '../../api.service';

@Component({
  selector: 'app-admin-wallets',
  templateUrl: './admin-wallets.component.html',
  styleUrls: ['./admin-wallets.component.css']
})
export class AdminWalletsComponent {
  wallets: any[] = [];

  constructor(private apiService: ApiService) {
    this.getAdminWallets();
  }

  getAdminWallets() {
    this.apiService.getAdminWallets().subscribe(
      (data) => {
        this.wallets = data;
      },
      (error) => {
        console.error("Error fetching wallets:", error);
      }
    );
  }
}
