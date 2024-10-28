import { Component } from '@angular/core';
import { ApiService } from '../../api.service';

@Component({
  selector: 'app-admin-reports',
  templateUrl: './admin-reports.component.html',
  styleUrls: ['./admin-reports.component.css']
})
export class AdminReportsComponent {
  report: any[] = [];
  startDate: string = '';
  endDate: string = '';

  constructor(private apiService: ApiService) {}

  generateReports() {
    this.apiService.generateReports(this.startDate, this.endDate).subscribe(
      (data) => {
        this.report = data.report;
      },
      (error) => {
        console.error("Error generating reports:", error);
      }
    );
  }
}
