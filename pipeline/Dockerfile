from python:3.14.2-slim
run pip install pandas pyarrow

workdir /app
copy pipeline.py /app/pipeline.py
entrypoint ["python", "/app/pipeline.py"]