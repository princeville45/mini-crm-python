# CRM V5 PRO: Modular Enterprise Architecture
**Designed and Engineered by Prince Victor**

## 🏗️ Architectural Vision
This repository is not just a CRM; it is a blueprint for **Layered RevOps Engineering**. The system is built on the principle of **Separation of Concerns (SoC)**, ensuring that data integrity, business logic, and user interaction never overlap.

## 🛠️ Key Engineering Concepts

### 1. Layered Ownership Model
The architecture is decoupled into four distinct layers:
- **Presentation Layer (`main.py`)**: Handles user interaction and data display.
- **Business Logic Layer (`logic.py`)**: Processes lead scoring and classification rules.
- **Data Access Layer (`db.py`)**: Manages SQLite transactions.
- **Configuration Layer (`config.py`)**: Centralizes all global constants.

### 2. Relational Integrity (SQL First)
Utilizes **relational logic** with SQLite to enforce data types and constraints, mirroring enterprise-grade CRM environments.

### 3. Abstraction & Modularity
The codebase is **pluggable**. Swapping databases or UI components can be done without breaking core business logic.

## 🚀 Why This Matters for RevOps
- **Isolating Errors**: UI bugs cannot corrupt the database.
- **Scaling Logic**: Update rules in `logic.py` without touching the data schema.
- **Auditability**: Strict data flow path from Input to Relational Storage.

## 🎓 Engineering Journal
This build demonstrates technical competence in **Python Modular Design**, **Statistical Architecture**, and **Automation Logic**.
