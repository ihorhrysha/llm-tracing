# LLM Tracing

The goal of this repo is to progres monitoring/observability approaches for LLM services in Python.

## Steps:

### 0.1.0 
Simple FastAPI app that uses logging with Python's built-in logging module
### 0.2.0 
Simple FastAPI app that uses custom JSON logger and configured root-level logger.
### 0.3.0 
Q&A LLM app with SQLite backend. 
It uses as an input human questions about data, translate them to SQL and generated the answer based on the retrieved data.
https://python.langchain.com/v0.1/docs/use_cases/sql/quickstart/

The app works fine. For example, given the following question:
```
list the most popular albums
```
We will get nicely formatted answer:
```
The most popular albums based on the total number of tracks sold are:
1. Minha Historia - 27 tracks sold
2. Greatest Hits - 26 tracks sold
3. Unplugged - 25 tracks sold
4. Acústico - 22 tracks sold
5. Greatest Kiss - 20 tracks sold
```
But what's happening under the hood? How can we trace the execution of the app?