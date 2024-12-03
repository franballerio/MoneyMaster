import gspread
from oauth2client.service_account import ServiceAccountCredentials


def authenticate_sheets():
    scope = ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "service_account.json", scope)
    return gspread.authorize(creds)


def test_google_sheets():
    try:
        gc = authenticate_sheets()
        sheet = gc.open("All time spendings").sheet1
        print(sheet.get_all_records())  # Test if you can fetch records
    except Exception as e:
        print(f"Error: {e}")


test_google_sheets()
