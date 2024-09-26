# Store Monitoring

- This repo contains code for take home assignent for Loop AI.
- Tech stack: FastAPI, PostgreSQL, Alembic, SQLAlchemy

### Architecture
<img width="817" alt="Screenshot 2024-09-26 at 7 30 36 PM" src="https://github.com/user-attachments/assets/1dcec479-c2bb-4d33-8930-17fe169fe52d">

### Potential improvements
- Using threading to make report generation faster
- Caching the result of report in memory with a time to live. This prevents us from doing calculation again.
