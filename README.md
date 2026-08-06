# Hercules_Project
A simulator creating dirty data, a cleansing pipeline, and a clean data dashboard.
# 🏭 Supply Chain & MRP Optimization Pipeline (Infor M3 ERP)

## 📌 Project Overview
This production-grade analytics engineering pipeline fixes a critical manufacturing constraint: **corrupted and unvalidated ERP data causing Material Requirements Planning (MRP) loop failures.** 

Using **DuckDB** as the high-performance OLAP engine and **dbt (Data Build Tool)** for data modeling and quality testing, this pipeline ingests raw, un-governed data from an **Infor M3 ERP** instance, enforces automated **Data Contracts**, standardizes Master Data, and outputs a materialized analytical mart tracking **Supplier Lead-Time Drift** and working capital risk.

---

## 🏗️ Data Architecture (Medallion Pattern)

### 1. Ingestion Layer (Raw Source)
* Simulates the unvalidated transactional database tables (`raw_infor_item_master`, `raw_infor_purchase_orders`, `raw_infor_supplier_governance`) containing text anomalies, trailing spaces, and corrupted data entry values.

### 2. Staging Layer (`/models/staging`)
* **`stg_items.sql`**: Trims whitespace from SKU identifiers and remediates a critical system glitch where safety stock quantities were recorded as negative values (defaulting anomalies to `0.0`).
* **`stg_purchase_orders.sql`**: Converts textual strings into true system calendar dates and calculates `delivery_delay_days` to capture supplier latency.
* **`stg_suppliers.sql`**: Cleans vendor naming conventions and standardizes status labels into uniform uppercase strings (`ACTIVE`, `PROBATION`, `DISQUALIFIED`).

### 3. Marts Layer (`/models/marts`)
* **`fct_mrp_optimization.sql`**: Materializes a unified, physical reporting table joining the cleansed dimensions. This serves as the single source of truth for procurement teams to assess supplier delivery reliability.

---

## 🛡️ Data Governance & Automated Contracts (`schema.yml`)
To ensure high organizational trust and eliminate systemic operational errors, the staging layer enforces **9 automated schema validation tests** during deployment:
* **Primary Key Enforcement**: Strict `unique` and `not_null` constraints on `item_id` and `po_id` to eliminate record duplication.
* **Value Constraint Contracts**: Rejects negative inventory balances passing into warehouse logic.
* **Regulatory Accepted Values**: Restricts vendor compliance profiles strictly to authorized states (`ACTIVE`, `PROBATION`, `DISQUALIFIED`), immediately alerting data stewards if an unmapped status slips through the ERP.

---

## 📊 Executive Reporting Dashboard (Tableau Public)

<img width="1021" height="835" alt="hercules_mrp_preview png" src="https://github.com/user-attachments/assets/941b5dfa-7d70-46fc-8511-b1cd3d21a798" />


_👉 View the interactive workbook on my [Tableau Public Profile](https://tableau.com)._

### Business Insights Delivered:
* **Supplier Lead-Time Drift Chart**: Visually isolates the operational variance between a supplier's promised delivery date and the actual warehouse arrival date.
* **Product Line Risk Matrix**: A compressed heatmap highlighting exactly which product divisions (Sheet Metal vs. HVAC) are structurally bottlenecked by vendors currently sitting on Probationary status.
