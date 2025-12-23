# User Wallet API

A secure and minimal User Wallet API built with Django and Django REST Framework.
This project demonstrates fintech-grade wallet logic, including safe money handling using Decimal, atomic transactions, and JWT authentication.

# Features

User authentication with JWT

Automatic wallet creation on user registration

View wallet balance

Credit wallet

Debit wallet (with insufficient funds protection)

Atomic transactions to prevent race conditions

Proper money handling using DecimalField

# Tech Stack

Python

Django

Django REST Framework

Simple JWT (Authentication)

SQLite (default, easily swappable)

📁 Project Structure
UserWallet/
├── UserWallet/
│   ├── urls.py
│   └── settings.py
│
├── wallet/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── signals.py
│   ├── urls.py
│   └── apps.py
│
├── manage.py
└── requirements.txt

# Installation & Setup
1️⃣ Clone the Repository
git clone <your-repo-url>
cd UserWallet

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

🔧 Environment Configuration

Create a .env file (optional for development):

DEBUG=True
SECRET_KEY=your-secret-key

🗄 Database Migration
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

▶️ Run Server
python manage.py runserver


Server will run on:

http://127.0.0.1:8000/

🔐 Authentication (JWT)
Obtain Token
POST /api/token/


Body:

{
  "username": "your_username",
  "password": "your_password"
}

Refresh Token
POST /api/token/refresh/

💰 Wallet API Endpoints
🔹 Get Wallet Balance
GET /api/wallet/balance/
Authorization: Bearer <access_token>

🔹 Credit Wallet
POST /api/wallet/credit/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

amount=5000

🔹 Debit Wallet
POST /api/wallet/debit/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

amount=2000

# Important Design Decisions

Decimal instead of float for money accuracy

Atomic database transactions to prevent double spending

Serializer-based validation to protect wallet operations

Signal-based wallet creation on user registration

# Error Handling

Empty or invalid amounts are rejected

Insufficient funds return a clear error response

Unauthorized requests are blocked by default

# Future Improvements

Transaction history & ledger

Payment gateway integration (Paystack / Flutterwave)

Wallet limits

Multi-currency support

Admin dashboard

# Author

Buchi Rex-David
Backend Developer (Python | Django)

# License

This project is open-source and available for learning and demonstration purposes.