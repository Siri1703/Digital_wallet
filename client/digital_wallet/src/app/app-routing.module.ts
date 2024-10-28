import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CreateWalletComponent } from './components/create-wallet/create-wallet.component';
import { DepositComponent } from './components/deposit/deposit.component';
import { WithdrawComponent } from './components/withdraw/withdraw.component';
import { TransferComponent } from './components/transfer/transfer.component';
import { TransactionHistoryComponent } from './components/transaction-history/transaction-history.component';
import { AdminWalletsComponent } from './components/admin-wallets/admin-wallets.component';
import { AdminTransactionsComponent } from './components/admin-transactions/admin-transactions.component';
import { AdminReportsComponent } from './components/admin-reports/admin-reports.component';
import { SuspendWalletComponent } from './components/suspend-wallet/suspend-wallet.component';

const routes: Routes = [
  { path: '', redirectTo: '/create-wallet', pathMatch: 'full' },
  { path: 'create-wallet', component: CreateWalletComponent },
  { path: 'deposit/:walletId', component: DepositComponent },
  { path: 'withdraw/:walletId', component: WithdrawComponent },
  { path: 'transfer/:walletId', component: TransferComponent },
  { path: 'transactions/:walletId', component: TransactionHistoryComponent },
  { path: 'admin/wallets', component: AdminWalletsComponent },
  { path: 'admin/transactions', component: AdminTransactionsComponent },
  { path: 'admin/reports', component: AdminReportsComponent },
  { path: 'admin/suspend/:walletId', component: SuspendWalletComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
