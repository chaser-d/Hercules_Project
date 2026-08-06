select
    po_id,
    trim(item_id) as item_id,
    supplier_id,
    qty_ordered,
    
    -- Convert text strings into true calendar dates
    cast(promised_delivery_date as DATE) as promised_date,
    cast(actual_delivery_date as DATE) as actual_date,
    
    -- Calculate the exact lead-time variance/delay
    date_diff('day', cast(promised_delivery_date as DATE), cast(actual_delivery_date as DATE)) as delivery_delay_days
from {{ source('infor_m3', 'raw_infor_purchase_orders') }}
