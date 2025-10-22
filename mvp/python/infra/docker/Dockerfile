FROM python:3.11-slim
WORKDIR /app
COPY mvp/python /app/mvp/python
COPY docs /app/docs
RUN pip install --no-cache-dir pydantic pyyaml
CMD ["python","-m","mvp.python.main"]
