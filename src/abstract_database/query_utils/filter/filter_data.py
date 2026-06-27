from .imports import *
def fetch_filtered_transactions_paginated_old(
    sol_amount, 
    operator=">",
    timestamp_operator=None, 
    limit=None, 
    offset=0,
    years=0,
    months=0,
    weeks=0,
    days=0,
    hours=0,
    minutes=0,
    seconds=0,
    timestamp=None,
    *args,
    **kwargs
):
    # Build the base query and include a LEFT JOIN to get tcn counts per pair.
    base_query = f"""
        FROM 
            transactions t
        JOIN 
            pairs p ON t.pair_id = p.id
        LEFT JOIN 
            metadata m ON p.meta_id = m.id
        LEFT JOIN (
            SELECT 
                pair_id, 
                SUM(jsonb_array_length(tcns)) AS tcn_count
            FROM 
                transactions
            GROUP BY 
                pair_id
        ) tcns_count ON p.id = tcns_count.pair_id
        WHERE 
            t.signature IN (
                SELECT signature FROM pairs WHERE signature IS NOT NULL
            )
        AND 
            t.program_id = p.program_id
        AND 
            EXISTS (
                SELECT 1
                FROM jsonb_array_elements(t.tcns) AS elem
                WHERE (elem ->> 'sol_amount')::numeric {operator} %s
    """
    params = [sol_amount]

    ts = derive_timestamp(
        years=years,
        months=months,
        weeks=weeks,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        timestamp=timestamp
    )
    
    if ts and timestamp_operator:
        base_query += f" AND (elem ->> 'timestamp')::bigint {timestamp_operator} %s"
        params.append(int(ts))
    
    # Close the EXISTS clause.
    base_query += ")"
    if metaDataKeys:
        # Optionally, validate the keys against an allowed list to prevent SQL injection.
        for key, flag in metaDataKeys.items():
            if flag:
                # True: value should not be None or false
                query += f" AND (m.{key} IS NOT NULL AND m.{key} <> false)"
            else:
                # False: value should be either None or false
                query += f" AND (m.{key} IS NULL OR m.{key} = false)"
    
    query += " ORDER BY t.updated_at DESC LIMIT %s OFFSET %s;"
    # Build the final data query including the tcn_count column.
    data_query = f"""
        SELECT
            p.*, 
            m.*,
            t.*,
            COALESCE(tcns_count.tcn_count, 0) AS tcn_count
        {base_query}
        ORDER BY t.updated_at DESC
        LIMIT %s OFFSET %s;
    """
    data_params = params + [limit, offset]
    transactions = query_data_as_dict(data_query, data_params)
    
    return transactions
def fetch_filtered_transactions_paginated(
        sol_amount, 
        operator=">",
        timestamp_operator=None, 
        limit=None, 
        offset=0,
        years=0,
        months=0,
        weeks=0,
        days=0,
        hours=0,
        minutes=0,
        seconds=0,
        timestamp=None,
        metaDataKeys=None,
        *args,
        **kwargs
    ):
        # Build the base query and include a LEFT JOIN to get tcn counts per pair.
        base_query = f"""
            FROM 
                transactions t
            JOIN 
                pairs p ON t.pair_id = p.id
            LEFT JOIN 
                metadata m ON p.meta_id = m.id
            LEFT JOIN (
                SELECT 
                    pair_id, 
                    SUM(jsonb_array_length(tcns)) AS tcn_count
                FROM 
                    transactions
                GROUP BY 
                    pair_id
            ) tcns_count ON p.id = tcns_count.pair_id
            WHERE 
                t.signature IN (
                    SELECT signature FROM pairs WHERE signature IS NOT NULL
                )
            AND 
                t.program_id = p.program_id
            AND 
                EXISTS (
                    SELECT 1
                    FROM jsonb_array_elements(t.tcns) AS elem
                    WHERE (elem ->> 'sol_amount')::numeric {operator} %s
        """
        params = [sol_amount]

        ts = derive_timestamp(
            years=years,
            months=months,
            weeks=weeks,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            timestamp=timestamp
        )
        
def fetch_filtered_transactions_paginated(
    sol_amount, 
    operator=">",
    timestamp_operator=None, 
    limit=None, 
    offset=0,
    years=0,
    months=0,
    weeks=0,
    days=0,
    hours=0,
    minutes=0,
    seconds=0,
    timestamp=None,
    metaDataKeys=None,
    *args,
    **kwargs
):
    # Build the base query and include a LEFT JOIN to get tcn counts per pair.
    base_query = f"""
        FROM 
            transactions t
        JOIN 
            pairs p ON t.pair_id = p.id
        LEFT JOIN 
            metadata m ON p.meta_id = m.id
        LEFT JOIN (
            SELECT 
                pair_id, 
                SUM(jsonb_array_length(tcns)) AS tcn_count
            FROM 
                transactions
            GROUP BY 
                pair_id
        ) tcns_count ON p.id = tcns_count.pair_id
        WHERE 
            t.signature IN (
                SELECT signature FROM pairs WHERE signature IS NOT NULL
            )
        AND 
            t.program_id = p.program_id
        AND 
            EXISTS (
                SELECT 1
                FROM jsonb_array_elements(t.tcns) AS elem
                WHERE (elem ->> 'sol_amount')::numeric {operator} %s
    """
    params = [sol_amount]

    ts = derive_timestamp(
        years=years,
        months=months,
        weeks=weeks,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        timestamp=timestamp
    )
    
    if ts:
        if timestamp_operator == None:
            timestamp_operator = ">"
        base_query += f" AND (elem ->> 'timestamp')::bigint {timestamp_operator} %s"
        params.append(int(ts))
    
    # Close the EXISTS clause.
    base_query += ")"
    
    # Add metadata filtering conditions.
    if metaDataKeys:
        for key, filter_val in metaDataKeys.items():
            # Skip any global options.
            if key == '__option':
                continue

            # Use a CASE expression that only casts to JSON if the text looks like valid JSON.
            # Here we check that the first two characters equal '{"'
            json_case = (
                f"(CASE WHEN m.{key} IS NOT NULL AND substring(m.{key} from 1 for 2) = '{{\"' "
                f"THEN m.{key}::jsonb ->> '__option' ELSE m.{key} END)"
            )
            
            if isinstance(filter_val, dict):
                option_value = filter_val.get('__option')
                if option_value == "None" or option_value is None:
                    # Require that the value is NULL or (if JSON) its '__option' equals 'None'.
                    base_query += f" AND (m.{key} IS NULL OR {json_case} = 'None')"
                else:
                    base_query += f" AND (m.{key} IS NOT NULL AND {json_case} <> %s)"
                    params.append(option_value)
            else:
                # When filter_val is a boolean.
                if filter_val:
                    base_query += f" AND (m.{key} IS NOT NULL AND {json_case} NOT IN ('None','false'))"
                else:
                    base_query += f" AND (m.{key} IS NULL OR {json_case} IN ('None','false'))"
    
    # Build the final data query including the tcn_count column.
    data_query = f"""
        SELECT
            p.*, 
            m.*,
            t.*,
            COALESCE(tcns_count.tcn_count, 0) AS tcn_count
        {base_query}
        ORDER BY t.updated_at DESC
        LIMIT %s OFFSET %s;
    """
    data_params = params + [limit, offset]
    transactions = query_data_as_dict(data_query, data_params)
    
    return transactions

