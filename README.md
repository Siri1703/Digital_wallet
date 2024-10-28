## Digital Wallet

# Objective: 
Create a digital wallet management application that allows users to create and manage wallets, make transactions (deposits, withdrawals, and transfers), and view transaction histories. The system should include an admin dashboard to oversee and manage user activities.

# User Endpoints:
`POST /wallets:` Create a new wallet.
`POST /wallets/{wallet_id}/deposit:` Deposit funds into a wallet.
`POST /wallets/{wallet_id}/withdraw:` Withdraw funds from a wallet.
`POST /wallets/{wallet_id}/transfer:` Transfer funds to another wallet.
`GET /wallets/{wallet_id}/transactions:` Retrieve transaction history for a specific wallet.
# Admin Endpoints:
`GET /admin/wallets:` Retrieve a list of all wallets with basic details.
`GET /admin/transactions:` Retrieve all transactions with filters (e.g., transaction type, date range).
`PUT /admin/wallets/{wallet_id}/suspend: `Suspend a wallet for suspicious activity.
`GET /admin/reports: `Generate reports on deposits, withdrawals, and transfers over a given time period.

## Setup:

# Backend:
** Navigate to Server folder in the project <br/>
** Run command `poetry install` which will install all the dependencies required for the project<br/>
** Run your Mongodb server and you can use mongo compass for visualizing your database
** Run command `poetry run uvicorn app.main:app --host 0.0.0.0 --port 8003 --env-file .env --reload` which will start the backend server<br/>
** It will create all the collections mentioned in `db.py` file<br>
** All the endpoints can be accessible in http://localhost:8003/docs in swagger ui format<br>

# Frontend
** Frontend is developed using Angular framework<br>
** Navigate to client/digital_wallet folder<br>
** Run `npm i` to install all the packages in the project folder<br>
** Run ng serve which will run the application and it is accessible in http://localhost:4200/<br>
** Below are the endpoints to the application to create , update , delete wallets from user and admin perspective<br>
`http://localhost:4200/create-wallet`
`http://localhost:4200/deposit/:walletId`
`http://localhost:4200/withdraw/:walletId`
`http://localhost:4200/transfer/:walletId`
`http://localhost:4200/transactions/:walletId`
`http://localhost:4200/admin/wallets`
`http://localhost:4200/admin/transactions`
`http://localhost:4200/admin/reports`
`http://localhost:4200/admin/suspend/:walletId`


