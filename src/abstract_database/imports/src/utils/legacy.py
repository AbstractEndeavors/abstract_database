from .imports import *
def get_if_list(obj):
    if obj and isinstance(obj,list):
        return obj[0]

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
def get_key_column_js():
    return{'Type': ['type'],
          'Timestamp': ['timestamp'],
          'Price': ['price'],
          'SOL Amount': ['solamountui','solAmountUi','solamount','solAmount','SOLAmount'],
          'Token Amount': ['tokenamountui','tokenAmountUi','tokenamount','tokenAmount','TokenAmount'],
          'Signature': ['signature'],
          'isBuy':['isbuy','is_buy'],
          'User Address':['user_address'],
          'virtualSolReserves':['virtualsolreserves'],
          'virtualTokenReserves':['virtualtokenreserves']
           }
          
def get_txn_columns(key):

    for titleKey,values in get_key_column_js().items():
        if key in values:
            return titleKey
def get_value(value):
    return value
def get_data_columns(key):
    return key.replace(' ','').lower() 
def is_in_for_key(obj,key):
    keyFuncs = [get_value,get_data_columns,get_txn_columns]
    for keyFunc in keyFuncs:
        currKey = keyFunc(key)
        if currKey in obj:
            return currKey
def get_for_key(obj, key):
    """
    Safely retrieves the value for the given key from an object.
    Handles variations in key formatting (e.g., lowercase, space removal).
    """
    possible_values = [
        obj.get(key, None),
        obj.get(get_data_columns(key), None),
        obj.get(get_txn_columns(key), None)
    ]

    # Return the first non-empty result that isn't None
    for val in possible_values:
        if val is not None and not isinstance(val, pd.Series) and not pd.isnull(val):
            return val
    return None
def get_for_value(obj,key,default=None):
    input(obj)
    value = obj.get(key) or obj.get(get_data_columns(key)) or obj.get(get_txn_columns(key))
    return value or default
def get_data_columns(key):
    return key.replace(' ', '').lower() 
def get_txn_columns(key):
    for titleKey, values in get_key_column_js().items():
        if key in values:
            return titleKey

#GUI Keys
def make_insert(key):
    key = key.replace(' ', '_').upper()
    return f"-{key}-"
def make_insert_bool(key):
    key = key.replace(' ', '_').upper()
    return f"-{key}_BOOL-"
def make_check_bool(key):
    key = key.replace(' ', '_').upper()
    return f"-{key}_CHECK-"
def deKeyKey(key):
    return key.lower()[1:-1].replace('_',' ')
def getBool(key, value):
    return isinstance(value, metaDataTypeKeys.get(key))
