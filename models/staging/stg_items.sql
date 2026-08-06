select
    trim(item_id) as item_id,
    trim(description) as item_description,
    product_line,
    
    -- Fix data anomaly: safety stock cannot be negative. Default to 0 if corrupted.
    case 
        when safety_stock_qty < 0 then 0.0 
        else safety_stock_qty 
    end as safety_stock_qty,
    
    standard_lead_time_days
from {{ source('infor_m3', 'raw_infor_item_master') }}
