import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8003';  // Your FastAPI backend URL

  constructor(private http: HttpClient) {}

  createWallet(walletData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/wallets`, walletData);
  }

  deposit(walletId: string, amount: number): Observable<any> {
    console.log(amount);
    
    return this.http.post(`${this.baseUrl}/wallets/${walletId}/deposit`, { amount:amount });
  }

  withdraw(walletId: string, amount: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/wallets/${walletId}/withdraw`, { amount });
  }

  transfer(walletId: string, transferData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/wallets/${walletId}/transfer`, transferData);
  }

  getTransactionHistory(walletId: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/wallets/${walletId}/transactions`);
  }

  getAdminWallets(): Observable<any> {
    return this.http.get(`${this.baseUrl}/admin/wallets`);
  }

  getAdminTransactions(transactionType?: string, startDate?: string, endDate?: string): Observable<any> {
    let url = `${this.baseUrl}/admin/transactions?`;
    if (transactionType) url += `transaction_type=${transactionType}&`;
    if (startDate) url += `start_date=${startDate}&`;
    if (endDate) url += `end_date=${endDate}`;
    return this.http.get(url);
  }

  suspendWallet(walletId: string): Observable<any> {
    return this.http.put(`${this.baseUrl}/admin/wallets/${walletId}/suspend`, {});
  }

  generateReports(startDate?: string, endDate?: string): Observable<any> {
    let url = `${this.baseUrl}/admin/reports?`;
    if (startDate) url += `start_date=${startDate}&`;
    if (endDate) url += `end_date=${endDate}`;
    return this.http.get(url);
  }
}
