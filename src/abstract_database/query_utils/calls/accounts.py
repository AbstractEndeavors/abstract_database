from .imports import *
def get_assigned_account(address):
    query = "SELECT assigned_account FROM wallet_account_assignments WHERE %s = ANY(addresses);"  # Assuming 'addresses' is the correct column name that holds an array.
    assigned_account = query_data(query, (address,))  # Ensure the parameter is passed as a tuple
    if assigned_account:
        assigned_account = assigned_account[0]['assigned_account']  # Extract the first result if available
    return assigned_account
def assert_user_wallets(profits):
    account_assignments = []
    for user_address,values in profits.items():
        signature = values.get('signature')
        response = update_and_add_wallet(user_address,signature)
        account_assignments.append(response)
    return account_assignments
def get_pairs_from_user_wallets(user_wallets):
    pairs = fetch_any_combo(columnNames='*',tableName='pairs',searchColumn='user_address',searchValue=user_wallets,anyValue=True,zipit=True)
    return pairs
