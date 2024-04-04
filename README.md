**Cryptocurrency Tracker**

Cryptocurrency Tracker is a Python program built using FastAPI and JWT token authentication. It allows users to track various cryptocurrencies and their prices.

Installation:
- clone the repository:
  git clone https://github.com/dubuchick/cryptocurrency-tracker.git
- install dependencies:
  pip install -r requirements.txt

Usage:
- run these commands
  python
  import services
  services._create_database()
  quit()
  uvicorn main:app --reload

Steps:
1. Create a User first using the "/users" endpoint
2. Import the data by running the "/insert/data" endpoint
3. Use the rest of endpoints as listed on the code.

