select
    supplier_id,
    trim(supplier_name) as supplier_name,
    
    -- Standardize un-governed text inputs to UPPERCASE
    upper(trim(supplier_status)) as supplier_status
from {{ source('infor_m3', 'raw_infor_supplier_governance') }}
