from .imports import *
def fetch_rows_with_filters(*args,**kwargs):
  return call_solcatcher_db('api/fetch_filtered_transactions_paginated',**kwargs)
def incriment_sol(window,values):
  current_value = values['-SOL_THRESHOLD_INPUT-']
  try:
      new_value = round(float(current_value) + 0.1, 1)
      configManager().updateConfig(init_sol = new_value)
      window['-SOL_THRESHOLD_INPUT-'].update(str(new_value))
  except ValueError:
      sg.popup_error("Invalid SOL Amount Threshold. Please enter a numeric value.")
def decriment_sol(window,values):
  current_value = values['-SOL_THRESHOLD_INPUT-']
  try:
      new_value = round(float(current_value) - 0.1, 1)
      if new_value >= 0:
          configManager().updateConfig(init_sol = new_value)
          window['-SOL_THRESHOLD_INPUT-'].update(str(new_value))
      else:
          sg.popup_error("SOL Amount Threshold cannot be negative.")
      
  except ValueError:
      sg.popup_error("Invalid SOL Amount Threshold. Please enter a numeric value.")
def validate_sol_threshold(values):
  sol_threshold_input = values['-SOL_THRESHOLD_INPUT-'].strip()
  sol_threshold = sol_threshold_input
  # Validate solAmount threshold input
  if sol_threshold_input == '':
      sol_threshold = 1.0  # Default value if input is empty
  else:
      try:
          sol_threshold = round(float(sol_threshold_input), 1)
          if sol_threshold < 0:
              sg.popup_error("SOL Amount Threshold cannot be negative. Using default value 1.0.")
              sol_threshold = 1.0
      except ValueError:
          sg.popup_error("Invalid SOL Amount Threshold. Please enter a numeric value.")
          sol_threshold = 1.0
  configManager().updateConfig(init_sol = sol_threshold)
def clear_tables(window):
  txn_data = []
  window['-TXN_TABLE-'].update(values=[])
  window['-IMAGE-'].update(data=None)
  window['-NAME-'].update(f"Name: N/A")
  window['-INIT_SOL_AMOUNT-'].update(f"Init SOL Amount: N/A")
  window['-INIT_TOKEN_AMOUNT-'].update(f"Init Token Amount: N/A")
  window['-INIT_VIRTUAL_SOL_RESERVES-'].update(f"Init Virtual SOL Reserves: N/A")
  window['-INIT_VIRTUAL_TOKEN_RESERVES-'].update(f"Init Virtual Token Reserves: N/A")
  window['-INIT_PRICE-'].update(f"Init Price: N/A")
  return txn_data
def get_min_timestamp(time_range):
    """
    Converts a selected time range into a Unix timestamp.
    """
    current_time = time.time()
    if time_range.startswith("Last") and  time_range.endswith("min"):
        seconds= int(time_range.split(' ')[1])*60
        time_min= int(current_time - seconds)
    elif time_range == "Last Hour":
        time_min= int(current_time - 3600)  # 1 hour = 3600 seconds
    elif time_range == "Last Day":
        time_min= int(current_time - 86400)  # 1 day = 86400 seconds
    elif time_range == "Last Week":
        time_min= int(current_time - 604800)  # 1 week = 604800 seconds
    elif time_range == "Last Month":
        time_min= int(current_time - 2592000)  # Approx. 30 days
    elif time_range == "All Time":
        time_min= 0  # No minimum timestamp
    else:
        time_min= 0  # Default to 'All Time' if unrecognized
    configManager().updateConfig(time_min=time_min)
    return time_min

def refresh(window,values):
  # Retrieve current filter values
  validate_sol_threshold(values)

  # Fetch and process main data with current filters
  rows = fetch_rows_with_filters(config_mgr.get_config_js('init_sol'), config_mgr.get_config_js('time_min'))
  main_columns = get_column_names(rows)
  main_data = rows

  # Update main table
  window['-MAIN_TABLE-'].update(
      values=get_main_data_columns(main_columns,main_data)
      # Removed headings=main_columns
  )
  # Clear transaction table and image display
  txn_data = clear_tables(window)
  configManager().updateConfig(last_refresh = get_time())
  return window
def get_all_case(objs):
    objs = make_list(objs or [])
    objs_copy = objs.copy()
    new_objs = []
    for i,obj in enumerate(objs):
        new_objs.append(obj)
        if isinstance(obj,str):
            new_objs.append(obj.lower())
            new_objs.append(obj.upper())
    return list(set(new_objs))
def is_true(obj):
    trues = get_all_case([True,'true','tru',1,float(1),'1'])
    if obj in trues:
        return True
    return False
def is_false(obj):
    falses = get_all_case([False,'false','fals',0,float(0),'0'])
    if obj in falses:
        return True
    return False
def toggle_var(obj):
    if is_true(obj):
        return False
    if is_false(obj):
        return True
    if obj:
        return False
    return True
