from .imports import *
def convert_key_value_to_timestamp(key,value):
    if key in ['updated_at','creation_date']:
        value = int(value.timestamp())
    return value
def convert_row_data_to_timestamp(row):
    for key,value in row.items():
        row[key] = convert_key_value_to_timestamp(key,value)
    return row
def convert_rows_data_to_timestamp(rows):
    for i,row in enumerate(rows):
        rows[i] = convert_row_data_to_timestamp(row)
    return rows
def convert_chart_data_keys_to_int(chart_data):
    new_chart_data = {}
    for series, subdict in chart_data.items():
        # Convert the keys in each sub-dictionary to integer timestamps.
        new_subdict = { int(k.timestamp()): v for k, v in subdict.items() }
        new_chart_data[series] = new_subdict
    return new_chart_data

def convert_chart_data_keys(chart_data):
    new_chart_data = {}
    for series, subdict in chart_data.items():
        # Convert the keys in each sub-dictionary to strings.
        new_subdict = { str(k): v for k, v in subdict.items() }
        new_chart_data[series] = new_subdict
    return new_chart_data

def get_time_interval(seconds =0,minutes=0, hours=0, days=0, weeks=0,months=0, years=0,*args,**kwargs):
    """Calculate a UNIX timestamp for the given time offset."""
    secs = 1
    mins = secs*60
    hr = 60 * mins
    day = 24 * hr
    week = 7 * day
    year = 365 * day
    month = year/12
    return ((secs * seconds) + (mins * minutes) + (hr * hours) + (day * days) + (week * weeks) + (month * months) + (year * years))

def get_time(time_interval,*args,**kwargs):
    timeStamp = time.time() - time_interval
    return int(timeStamp)  # Return integer timestamp

def derive_timestamp(timestamp=None,seconds =0,minutes=0, hours=0, days=0, weeks=0,months=0, years=0,*args,**kwargs):
    time_interval = get_time_interval(seconds=seconds,minutes=minutes, hours=hours, days=days, weeks=weeks,months=months, years=years)
    if time_interval:
        timestamp = get_time(time_interval)
    return timestamp
def get_timestamp_from_data(data,*args,**kwargs):
    years = data.get('years',0)
    months = data.get('months',0)
    weeks = data.get('weeks',0)
    days = data.get('days',0)
    hours = data.get('hours',0)
    minutes = data.get('minutes',0)
    seconds = data.get('seconds',0)
    timestamp = data.get('timestamp')
    time_interval = get_time_interval(seconds=seconds,minutes=minutes, hours=hours, days=days, weeks=weeks,months=months, years=years)
    if time_interval:
        timestamp = get_time(time_interval)
    return timestamp

def convert_timestamps_to_unix(txn_data_list, timestamp_key='timestamp'):

    """

    Converts all timestamps in the provided list of transaction data to Unix timestamp (seconds since epoch).



    Args:

    txn_data_list (list of dict): List of transaction data dictionaries.

    timestamp_key (str): The key in the transaction dict where the timestamp is stored.



    Returns:

    list of dict: The transaction data list with converted timestamps.

    """
    for txn in txn_data_list:
        if timestamp_key in txn and isinstance(txn[timestamp_key], str):
            try:
                # Convert to Unix timestamp
                txn[timestamp_key] = int(pd.to_datetime(txn[timestamp_key]).timestamp())
            except Exception as e:
                print(f"Failed to convert timestamp for transaction ID {txn.get('id')}: {e}")
    return txn_data_list



def is_valid_pair(pair, min_timestamp):
    """
    Checks if the 'timestamp' key in the pair is greater than or equal to
    the minimum timestamp minus 1 day.
    
    Args:
    pair (dict): A dictionary containing a 'timestamp' key.
    min_timestamp (float): The minimum timestamp to compare against.
    
    Returns:
    bool: True if the pair's timestamp is within the desired range, False otherwise.
    """
    if 'timestamp' not in pair:
        raise KeyError("The key 'timestamp' is not present in the 'pair' dictionary.")
    
    try:
        pair_timestamp = pair['timestamp']
        
        # If the timestamp is an integer or float (Unix timestamp)
        if isinstance(pair_timestamp, (int, float)):  
            pair_timestamp = datetime.fromtimestamp(pair_timestamp)
        
        # If the timestamp is a string, try to parse it using multiple possible formats
        elif isinstance(pair_timestamp, str):  
            try:
                pair_timestamp = datetime.fromisoformat(pair_timestamp)  # ISO 8601 format
            except ValueError:
                try:
                    pair_timestamp = datetime.strptime(pair_timestamp, '%a, %d %b %Y %H:%M:%S %Z')  # RFC 1123 format
                except ValueError as e:
                    raise ValueError(f"Unsupported timestamp format for value '{pair_timestamp}'") from e
        
        # Calculate the minimum valid timestamp as 1 day before min_timestamp
        min_valid_timestamp = datetime.fromtimestamp(min_timestamp) - timedelta(days=1)
        
        # Compare the timestamps
        return pair_timestamp.timestamp() >= min_valid_timestamp.timestamp()
    
    except Exception as e:
        raise ValueError(f"Error processing timestamp from pair: {e}")
def convert_timestamp_to_datetime(df, timestamp_column='timestamp', datetime_column='datetime'):
    """
    Converts the 'timestamp' column to 'datetime' with error handling and logging.
    
    Parameters:
    - df (pd.DataFrame): The DataFrame to operate on.
    - timestamp_column (str): The name of the timestamp column.
    - datetime_column (str): The name of the resulting datetime column.

    Returns:
    - pd.DataFrame: The updated DataFrame with the new datetime column as the index.
    """
    # 1. Check if the DataFrame is empty
    if df is None or df.empty:
        raise ValueError(f"The DataFrame is empty. Cannot convert '{timestamp_column}' to '{datetime_column}'.")

    # 2. Check if the timestamp column exists in the DataFrame
    if timestamp_column not in df.columns:
        raise ValueError(f"Column '{timestamp_column}' not found in DataFrame. Available columns: {df.columns.tolist()}")

    try:
        # 3. Extract the 'timestamp' column
        timestamp_data = df[timestamp_column]
        
        # 4. Ensure the timestamp data is not empty
        if timestamp_data is None or timestamp_data.empty:
            raise ValueError(f"'{timestamp_column}' is empty or not found in the DataFrame.")
        
        # 5. Convert timestamp to numeric, if possible
        timestamp_data = pd.to_numeric(timestamp_data, errors='coerce')
        
        # 6. Convert to datetime (coerce to NaT if the conversion fails)
        df[datetime_column] = pd.to_datetime(timestamp_data, unit='s', errors='coerce')

        # 7. Check if all timestamps failed to convert
        if df[datetime_column].isnull().all():
            invalid_timestamps = df[timestamp_column].unique()[:10]  # Sample of invalid timestamps
            raise ValueError(f"All timestamps failed to convert. Sample invalid timestamps: {invalid_timestamps}")

        # 8. Option to log or handle invalid timestamps
        invalid_timestamps = df[df[datetime_column].isnull()]
        if not invalid_timestamps.empty:
            print(f"Warning: {len(invalid_timestamps)} invalid timestamps found in column '{timestamp_column}'.")
            print(f"Sample of invalid timestamps: {invalid_timestamps[timestamp_column].head().tolist()}")

        # 9. Remove rows where datetime conversion failed (optional)
        df = df[df[datetime_column].notnull()]

        # 10. Set datetime as the index and sort the DataFrame
        df.set_index(datetime_column, inplace=True)
        df.sort_index(inplace=True)

    except Exception as e:
        raise ValueError(f"Error converting '{timestamp_column}' to '{datetime_column}': {e}")

    return df
