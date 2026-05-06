# LoanLedger — Django + React

A loan tracking app converted from a Motoko/ICP backend to **Django REST Framework** + **React** (no build step).

## Project Structure

```
loanledger/
├── backend/               # Django project
│   ├── manage.py
│   ├── requirements.txt
│   ├── loanledger/        # Django settings & URLs
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── loans/             # Loans app
│       ├── models.py      # Loan & Repayment models
│       ├── serializers.py
│       ├── views.py       # API views
│       └── urls.py
└── frontend/
    └── index.html         # Self-contained React app (no build needed)
```

## Quick Start

### 1. Backend (Django)

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (creates db.sqlite3)
python manage.py migrate --run-syncdb

# Start the server
python manage.py runserver
# → running at http://localhost:8000
```

### 2. Frontend (React)

Just open `frontend/index.html` directly in a browser — it loads React from CDN and calls the Django API at `http://localhost:8000/api`.

```bash
# macOS
open frontend/index.html

# Linux
xdg-open frontend/index.html
```

> If you serve from a different host/port, update `API_BASE` at the top of `frontend/index.html`.

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/loans/` | List all loans |
| POST | `/api/loans/` | Create a loan |
| GET | `/api/loans/<id>/` | Get a single loan |
| DELETE | `/api/loans/<id>/` | Delete a loan |
| GET | `/api/loans/<id>/repayments/` | List repayments for a loan |
| POST | `/api/loans/<id>/repayments/` | Record a repayment |

### Create Loan (POST `/api/loans/`)
```json
{
  "given_to": "Rahul Sharma",
  "amount_given": 50000,
  "given_date": "2026-01-15",
  "notes": "Optional notes"
}
```

### Record Repayment (POST `/api/loans/1/repayments/`)
```json
{
  "amount_returned": 10000,
  "return_date": "2026-02-01",
  "notes": "First installment"
}
```

## Business Logic (same as original)

- `pending_amount = amount_given - total_returned` — computed automatically on every save
- `status` flips to `completed` when `pending_amount == 0`
- Repayment amount cannot exceed `pending_amount` (validated server-side)
- Loans are ordered newest-first
- Deleting a loan cascades and removes all its repayments

## Features (matching original UI)

- **Dashboard** — loan grid with summary stats (Total Given / Pending / Recovered)
- **New Loan** — form with validation
- **Loan Detail** — summary card, record repayment form, repayment history
- **Delete loan** — with confirmation dialog
- Toast notifications for all actions
- Responsive layout (mobile + desktop)
- Loading skeletons

 xdg-open index.html  
 Opening in existing browser session.

