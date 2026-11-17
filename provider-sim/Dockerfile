FROM python:3.12-slim
WORKDIR /app
RUN pip install fastapi "uvicorn[standard]" httpx
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
