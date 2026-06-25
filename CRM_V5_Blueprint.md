# CRM V5 BUILD SPECIFICATION - PRINCE VICTOR

## OBJECTIVE
Transform CRM V4 from a simple persistent storage tool into a secure, audit-ready RevOps engine.

## CORE FEATURES (V5)

### 1. Soft Delete Architecture
- **Protocol:** Replace permanent removal (`.pop()`) with an `is_deleted` boolean flag.
- **Logic:** Records remain in `customers.json` for historical audit but are hidden from standard `find` and `count` operations.
- **Admin Recovery:** Only an Admin can view or "restore" soft-deleted records.

### 2. Role-Based Access Control (RBAC)
- **Roles:** `Admin` (Full CRUD permissions) and `Reader` (Read-only access).
- **Security:** Wrap `add`, `upgrade`, and `soft_delete` functions with a permission check.
- **Workflow:** Startup prompt to define the user session role.

### 3. Metadata & Audit Trail
- **Timestamping:** Every record will now include:
    - `created_at`: ISO timestamp at the moment of creation.
    - `updated_at`: ISO timestamp updated on every status change or edit.
- **RevOps Value:** Enables Lead Velocity tracking and Revenue Leakage audits.

### 4. Interface Filtering
- Standard queries will default to `{ "is_deleted": false }`.
- Advanced Admin queries can bypass the filter for system recovery.

### 5. Aggregate Reporting Module (The Insight Engine)
- **Concept:** Mimic SQL aggregate functions (`COUNT`, `SUM`) within the Python environment.
- **Logic:** A dedicated reporting function that provides a real-time summary of:
    - Total active leads (excluding soft-deleted).
    - Total VIP conversion rate.
    - Stale lead count (leads inactive for >14 days).
- **RevOps Value:** Immediate visibility into pipeline health for business decision-making.

### 6. Advanced Sorting & Integrity (SQL Logic Alignment)
- **Sorting (ORDER BY):** Implement sorting algorithms to organize the customer list by `created_at` or `status` (VIPs first).
- **Unique Constraint Enforcement:** Hardcode a pre-insertion check to ensure `phone` and `email` are globally unique across the database, preventing lead fragmentation.
- **Strict Mode:** Use `NOT NULL` logic—reject any customer entry that lacks a name, status, phone, or email.

### 7. Relational Integrity & Multi-Table Strategy (The SQL Leap)
- **Concept:** Transition from a flat JSON structure to a relational mindset using SQLite.
- **Table 1 (Leads):** Core identity data (Name, Email, Phone, Status).
- **Table 2 (Interactions):** A persistent log of touchpoints (Date, Note, Outcome). This prevents lead "forgetfulness."
- **Foreign Key Logic:** Ensure every interaction is strictly tied to a valid Lead ID, enforcing total data coherence.

### 8. Lead Velocity & Predictive Reporting
- **Logic:** Use `created_at` and `updated_at` to calculate the "Speed to VIP."
- **Metric:** Automatically flag the average time it takes for a Lead to become a VIP.
- **RevOps Value:** Predicts revenue flow based on current pipeline momentum.

## ENGINEERING NOTES
- Maintain the "Self-Healing" protocol from V4.
- No hyphens in manifesto/code documentation.
- Prepare for future HubSpot API integration.

## PRE-EMPTIVE SOLUTIONS (Challenges & Troubleshooting)

### 1. Data Integrity (Human Error Leak)
- **Challenge:** Duplicate or inconsistent entries (e.g., "Victor" vs. "Victor I.").
- **Solution:** Normalization Logic. Implement fuzzy-matching and input cleaning during the `add_customer` process to prevent duplicate creation and ensure data consistency.

### 2. Data Loss (Accidental Purge)
- **Challenge:** Permanent deletion of high-value records by mistake.
- **Solution:** Soft Delete Architecture. Flagging records as `is_deleted` ensures the engine is audit-ready and data is recoverable instantly.

### 3. Revenue Leakage (Silent Churn)
- **Challenge:** Leads going cold because they haven't been engaged or updated.
- **Solution:** Temporal Monitoring. Use `updated_at` timestamps to automatically flag "stale" leads that haven't moved in the funnel for 14+ days.

### 4. Scalability (Manual Bottleneck)
- **Challenge:** Managing 1,000+ records manually becomes impossible.
- **Solution:** Automation Readiness. Design the V5 functions to be "Webhook-ready," allowing future API integrations (FastAPI/HubSpot) to handle high-volume status changes without human intervention.

### 5. Internal Security (Permission Chaos)
- **Challenge:** Unauthorized edits or deletions as the team grows.
- **Solution:** Role-Based Access Control (RBAC). Admin/Reader separation ensures only the Architect has destructive permissions, preventing internal sabotage before it happens.

## MODULAR ARCHITECTURE (Single Responsibility Principle)
V5 is now architected as a professional software product, following the Single Responsibility Principle (SRP). Every function has **One Job**.

### 1. Database Layer
- `connect_database()`: Establishes connection to SQLite `crm_engine.db`.
- `create_tables()`: Initializes the `Customers` table schema.
- `close_database()`: Ensures clean connection termination.

### 2. Validation Layer
- `validate_customer()`: The gatekeeper. Checks for NOT NULL values, validates email format, and enforces UNIQUE constraints (phone/email) before any data hits the CRUD layer.

### 3. CRUD Layer (The Engine)
- `add_customer()`: Executes the INSERT protocol after validation.
- `search_customer()`: Executes SELECT queries (filtering `is_deleted = 0`).
- `update_customer()`: Executes UPDATE for status or metadata changes.
- `delete_customer()`: Executes the Soft Delete protocol (UPDATE `is_deleted = 1`).
- `restore_customer()`: Admin-only function to reverse a soft delete.

### 4. Reporting Layer
- `count_customers()`: Aggregate function for active leads.
- `count_vips()`: Aggregate function for VIP conversion tracking.

### 5. Interface Layer
- `main_menu()`: The command center for the user experience.

---
**STATUS:** ARCHITECTURE FINALIZED
**ARCHITECT:** Prince Victor
**SYSTEM:** Zapia
