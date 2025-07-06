# 0x00. Python - Generators

## 📚 Project Description

This project explores the use of Python generators to efficiently process large datasets, stream SQL results one-by-one, paginate lazily, and perform memory-safe computations. By leveraging the `yield` keyword and generator functions, we simulate real-world backend scenarios such as loading CSVs into databases, batch processing, and computing aggregates without consuming excessive memory.

---

## 🧠 Learning Objectives

By the end of this project, I was able to:

- Understand how Python generators work and when to use them
- Use `yield` to stream large datasets instead of loading everything in memory
- Create generators that work with SQL data
- Implement batch processing logic with controlled memory usage
- Build lazy pagination systems
- Perform memory-efficient aggregation on streamed data
- Integrate Python with MySQL for realistic backend simulations

---

## 📁 Project Structure

| File | Description |
|------|-------------|
| `seed.py` | Connects to MySQL, creates DB and tables, inserts users from CSV |
| `0-stream_users.py` | Streams users one-by-one using a generator |
| `1-batch_processing.py` | Streams and processes users in batches (filters age > 25) |
| `2-lazy_paginate.py` | Lazily paginates database results using a generator |
| `4-stream_ages.py` | Streams only user ages and calculates the average in a memory-safe way |
| `user_data.csv` | Provided dataset used to populate the database |
| `0-main.py` → `4-main.py` | Test scripts provided by ALX to validate each task |

---

## 🧪 Tasks Breakdown

### ✅ Task 0: Getting Started with Python Generators
- **Objective**: Create the `ALX_prodev` database and the `user_data` table. Import CSV data using Python.
- **Script**: `seed.py`
- **Functions**:
  - `connect_db()`
  - `create_database(connection)`
  - `connect_to_prodev()`
  - `create_table(connection)`
  - `insert_data(connection, file_path)`

---

### ✅ Task 1: Generator to Stream Rows One-by-One
- **Objective**: Create a generator that yields one row from the `user_data` table at a time.
- **Script**: `0-stream_users.py`
- **Function**: `stream_users()`

---

### ✅ Task 2: Batch Processing of Large Data
- **Objective**: Stream users in batches, filter by age > 25, and yield them.
- **Script**: `1-batch_processing.py`
- **Functions**:
  - `stream_users_in_batches(batch_size)`
  - `batch_processing(batch_size)`

---

### ✅ Task 3: Lazy Pagination with Generators
- **Objective**: Simulate a paginated data fetcher using a generator and offset logic.
- **Script**: `2-lazy_paginate.py`
- **Functions**:
  - `paginate_users(page_size, offset)`
  - `lazy_paginate(page_size)`

---

### ✅ Task 4: Memory-Efficient Average Age Calculator
- **Objective**: Stream only the `age` column and compute the average without using SQL's `AVG`.
- **Script**: `4-stream_ages.py`
- **Functions**:
  - `stream_user_ages()`
  - Inline logic to compute average using only two loops

---

## 🚀 How to Run Locally

> **Make sure MySQL server is running and accessible**

1. **Install MySQL Connector:**
```bash
pip install mysql-connector-python
