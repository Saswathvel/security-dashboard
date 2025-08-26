For testing purpose only --
##  Tools Required on the Host

- **git**
- **node** (for some repos' npm install)
- **gitleaks**
- **syft**
- **osv-scanner**
- **codeql**
- **protobuf-compiler**

---

###  Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 app.py

Backend will run on: http://localhost:5001
```

###  Frontend
```bash
cd frontend
npm install
npm run dev

Frontend will run on: http://localhost:3000
```

###Demo
admin : admin123
