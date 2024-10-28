import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CreateWalletComponent } from './components/create-wallet/create-wallet.component';
import { DepositComponent } from './components/deposit/deposit.component';
import { WithdrawComponent } from './components/withdraw/withdraw.component';
import { TransferComponent } from './components/transfer/transfer.component';
import { TransactionHistoryComponent } from './components/transaction-history/transaction-history.component';
import { AdminWalletsComponent } from './components/admin-wallets/admin-wallets.component';
import { AdminTransactionsComponent } from './components/admin-transactions/admin-transactions.component';
import { AdminReportsComponent } from './components/admin-reports/admin-reports.component';
import { SuspendWalletComponent } from './components/suspend-wallet/suspend-wallet.component';

@NgModule({
  declarations: [
    AppComponent,
    CreateWalletComponent,
    DepositComponent,
    WithdrawComponent,
    TransferComponent,
    TransactionHistoryComponent,
    AdminWalletsComponent,
    AdminTransactionsComponent,
    AdminReportsComponent,
    SuspendWalletComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
