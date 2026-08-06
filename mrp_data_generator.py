import duckdb
import random
from datetime import datetime, timedelta

conn = duckdb.connect('hercules_mrp.db')

# Create Raw ERP Tables
conn.execute('CREATE OR REPLACE TABLE raw_infor_item_master (item_id VARCHAR, description VARCHAR, product_line VARCHAR, safety_stock_qty DOUBLE, standard_lead_time_days DOUBLE);')
conn.execute('CREATE OR REPLACE TABLE raw_infor_purchase_orders (po_id VARCHAR, item_id VARCHAR, supplier_id VARCHAR, qty_ordered DOUBLE, promised_delivery_date VARCHAR, actual_delivery_date VARCHAR);')
conn.execute('CREATE OR REPLACE TABLE raw_infor_supplier_governance (supplier_id VARCHAR, supplier_name VARCHAR, supplier_status VARCHAR);')

# Populate Mock Raw Item Master Data (With dirty text spaces and anomalies)
items = [
    ('SKU-1001 ', ' 1/4 Inch Steel Sheet', 'Sheet Metal', 500.0, 14.0),
    ('SKU-1002', '3/8 Inch Steel Sheet ', 'Sheet Metal', -50.0, 14.0), # Negative stock anomaly!
    ('SKU-2001', 'HVAC Duct Housing V1', 'HVAC Fabrications', 150.0, 21.0),
    ('SKU-2002 ', 'HVAC Dampener Assembly', 'HVAC Fabrications', 0.0, 30.0),
    ('SKU-3001', 'Copper Coil 50ft', 'Raw Copper', 100.0, 45.0)
]
for item in items:
    conn.execute('INSERT INTO raw_infor_item_master VALUES (?, ?, ?, ?, ?)', item)

# Populate Purchase Orders (With delayed timelines to calculate Lead Time Drift)
pos = [
    ('PO-8801', 'SKU-1001 ', 'SUPP-99', 1000.0, '2026-07-01', '2026-07-20'), # Delayed by 5 days!
    ('PO-8802', 'SKU-1002', 'SUPP-99', 500.0, '2026-07-05', '2026-07-04'),
    ('PO-8803', 'SKU-2001', 'SUPP-44', 200.0, '2026-07-10', '2026-07-10'),
    ('PO-8804', 'SKU-2002 ', 'SUPP-44', 300.0, '2026-07-12', '2026-07-26'), # Delayed by 14 days!
    ('PO-8805', 'SKU-3001', 'SUPP-11', 50.0, '2026-07-15', '2026-07-15')
]
for po in pos:
    conn.execute('INSERT INTO raw_infor_purchase_orders VALUES (?, ?, ?, ?, ?, ?)', po)

# Populate Supplier Governance Profiles (With unstandardized status labels)
suppliers = [
    ('SUPP-11', 'Apex Steel Corp ', 'Active'),
    ('SUPP-44', 'Midwest Fab Supply', 'PROBATION'), # Ungoverned text state!
    ('SUPP-99', 'Global Copper Dist', 'Disqualified') # Critically broken supplier!
]
for supplier in suppliers:
    conn.execute('INSERT INTO raw_infor_supplier_governance VALUES (?, ?, ?)', supplier)

conn.close()
print('?? Hercules ERP Mock Data Generated Successfully in hercules_mrp.db!')
