import os
import pandas as pd
from dotenv import load_dotenv
from kiteconnect import KiteConnect
import logging
import time # For potential rate limiting

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_kite_client():
    """
    Initializes and returns a KiteConnect client instance.
    Handles loading API credentials from .env.
    """
    load_dotenv() # Load environment variables from .env file

    api_key = os.getenv('KITE_API_KEY')
    api_secret = os.getenv('KITE_API_SECRET')
    access_token = os.getenv('KITE_ACCESS_TOKEN')

    if not api_key or not api_secret:
        logging.error("KITE_API_KEY and KITE_API_SECRET must be set in the .env file.")
        return None

    kite = KiteConnect(api_key=api_key)

    # --- Zerodha Authentication Flow (First-time setup guidance) ---
    # If you don't have an access_token, you need to perform the login flow.
    # 1. Go to the login URL printed below in your browser.
    # 2. Log in with your Zerodha credentials.
    # 3. After successful login, you will be redirected to your Redirect URL
    #    (configured in your Zerodha developer app) with a 'request_token' in the URL.
    # 4. Copy that 'request_token'.
    # 5. Uncomment the `generate_session` block below, replace "YOUR_REQUEST_TOKEN_HERE"
    #    with the copied token, and run the script.
    # 6. The script will print the 'access_token'. Copy it and paste it into your .env file
    #    as KITE_ACCESS_TOKEN, then comment out the `generate_session` block again.
    # 7. For subsequent runs, the script will directly use the KITE_ACCESS_TOKEN from .env.

    if not access_token:
        logging.warning("KITE_ACCESS_TOKEN not found in .env. You need to perform the login flow.")
        logging.info(f"Go to this URL to login and get your request_token: {kite.login_url()}")
        logging.info("After logging in, copy the 'request_token' from the redirect URL.")
        logging.info("Then, uncomment the 'generate_session' block below, replace 'YOUR_REQUEST_TOKEN_HERE' with your token, and run this script again.")
        logging.info("Once you get the access token, add it to your .env file as KITE_ACCESS_TOKEN.")
        # Example for generating session (UNCOMMENT AND REPLACE TOKEN FOR FIRST RUN):
        # try:
        #     initial_data = kite.generate_session("YOUR_REQUEST_TOKEN_HERE", api_secret=api_secret)
        #     access_token = initial_data["access_token"]
        #     logging.info(f"Generated Access Token: {access_token}")
        #     logging.info("Please add this token to your .env file as KITE_ACCESS_TOKEN and re-run the script.")
        #     return None # Exit as token needs to be saved
        # except Exception as e:
        #     logging.error(f"Error generating session: {e}")
        #     return None
        return None # Exit if access token is not available

    kite.set_access_token(access_token)
    logging.info("KiteConnect client initialized successfully with access token.")
    return kite

def get_instrument_token(kite, company_name, all_instruments):
    """
    Finds the instrument token for a given company name.
    Prioritizes exact name match, then attempts partial match.
    Returns instrument_token and Zerodha's format of exchange:tradingsymbol.
    """
    company_name_lower = company_name.lower()
    found_instrument = None

    # Try exact match for tradingsymbol or name
    for instrument in all_instruments:
        if instrument.get('tradingsymbol', '').lower() == company_name_lower:
            found_instrument = instrument
            break
        if instrument.get('name', '').lower() == company_name_lower:
            found_instrument = instrument
            break

    # If not found by exact match, try partial match (might return multiple, pick first good one)
    # This is a heuristic and might not always be accurate.
    if not found_instrument:
        for instrument in all_instruments:
            # Check if company name is a substring of instrument name or tradingsymbol
            if company_name_lower in instrument.get('name', '').lower() or \
               company_name_lower in instrument.get('tradingsymbol', '').lower():
                found_instrument = instrument
                logging.warning(f"Partial match found for '{company_name}': {instrument.get('tradingsymbol')} ({instrument.get('name')}). Consider refining company names for exact matches or adding ticker symbols to Excel.")
                break # Take the first partial match, or implement a more robust selection

    if found_instrument:
        return found_instrument.get('instrument_token'), f"{found_instrument.get('exchange')}:{found_instrument.get('tradingsymbol')}"
    return None, None

def manage_watchlists(kite, companies_data):
    """
    Manages Zerodha watchlists based on the provided company data.
    Adds SIP companies to watchlists named after their sectors.
    """
    logging.info("Fetching all available instruments from Zerodha...")
    try:
        # Fetch instruments for NSE and BSE
        nse_instruments = kite.instruments('NSE')
        bse_instruments = kite.instruments('BSE')
        all_instruments = nse_instruments + bse_instruments
        logging.info(f"Fetched {len(nse_instruments)} NSE instruments and {len(bse_instruments)} BSE instruments.")
    except Exception as e:
        logging.error(f"Error fetching instruments: {e}")
        return

    # Group SIP companies by sector
    sip_companies_by_sector = {}
    for _, row in companies_data.iterrows():
        investment_type = str(row['Investment Type']).strip().upper()
        # Only consider 'SIP' or 'BETWEEN SIP AND ONE-TIME' as SIP
        if investment_type == 'SIP' or investment_type == 'BETWEEN SIP AND ONE-TIME':
            company_name = row['Company Name'].strip()
            sector = row['Sector'].strip()
            if sector not in sip_companies_by_sector:
                sip_companies_by_sector[sector] = []
            sip_companies_by_sector[sector].append(company_name)

    if not sip_companies_by_sector:
        logging.info("No SIP companies found in the provided data to add to watchlists based on 'SIP' or 'between SIP and ONE-TIME' investment types.")
        return

    logging.info(f"Found SIP companies grouped by sector: {list(sip_companies_by_sector.keys())}")

    # Get current watchlists and their content
    try:
        user_watchlists = kite.retrieve_watchlist()
        current_watchlist_info = {}
        for wl in user_watchlists:
            current_watchlist_info[wl['watchlist_name']] = {
                'id': wl['watchlist_id'],
                'scrips': {item['tradingsymbol'] for item in wl['instruments']}
            }
        logging.info("Successfully retrieved current user watchlists.")
    except Exception as e:
        logging.error(f"Error retrieving user watchlists: {e}")
        return

    # Iterate through sectors and add to watchlists
    for sector, company_names in sip_companies_by_sector.items():
        # Create a clean watchlist name, max 25 chars for Zerodha
        watchlist_name = f"SIP_{sector.replace(' ', '_').replace('&', 'AND')}"
        if len(watchlist_name) > 25:
            watchlist_name = watchlist_name[:25] # Trim to max length

        logging.info(f"Processing watchlist: '{watchlist_name}' for sector: '{sector}'")

        watchlist_id = current_watchlist_info.get(watchlist_name, {}).get('id')
        current_scrips_in_watchlist = current_watchlist_info.get(watchlist_name, {}).get('scrips', set())

        scrips_to_add_to_api = [] # List to hold instrument_token for API call
        scrips_added_count = len(current_scrips_in_watchlist) # Count existing scrips

        for company_name in company_names:
            instrument_token, tradingsymbol_with_exchange = get_instrument_token(kite, company_name, all_instruments)

            if instrument_token and tradingsymbol_with_exchange:
                # Extract just the tradingsymbol for comparison with current_scrips_in_watchlist
                # Zerodha's retrieve_watchlist returns just tradingsymbol, not exchange:tradingsymbol
                tradingsymbol_only = tradingsymbol_with_exchange.split(':')[1]

                if tradingsymbol_only not in current_scrips_in_watchlist:
                    if scrips_added_count < 50: # Zerodha watchlist limit is 50 scrips
                        scrips_to_add_to_api.append(tradingsymbol_with_exchange)
                        scrips_added_count += 1
                    else:
                        logging.warning(f"Watchlist '{watchlist_name}' is full (50 scrips). Cannot add '{company_name}'.")
                        # If watchlist is full, we stop adding to THIS watchlist and move to the next sector
                        break
                else:
                    logging.info(f"'{company_name}' ({tradingsymbol_only}) is already in watchlist '{watchlist_name}'. Skipping.")
            else:
                logging.warning(f"Could not find instrument for company: '{company_name}'. Please check company name or add ticker to Excel.")

        if scrips_to_add_to_api:
            try:
                if watchlist_id:
                    # Append to existing watchlist
                    logging.info(f"Adding {len(scrips_to_add_to_api)} new scrips to existing watchlist '{watchlist_name}' (ID: {watchlist_id})...")
                    kite.add_to_watchlist(watchlist_id, scrips_to_add_to_api)
                else:
                    # Create new watchlist and add scrips
                    logging.info(f"Creating new watchlist '{watchlist_name}' and adding {len(scrips_to_add_to_api)} scrips...")
                    kite.create_watchlist(watchlist_name, scrips_to_add_to_api)
                logging.info(f"Successfully updated watchlist '{watchlist_name}'.")
            except Exception as e:
                logging.error(f"Error managing watchlist '{watchlist_name}': {e}")
            time.sleep(1) # Small delay to avoid hitting API rate limits

def main():
    kite = get_kite_client()
    if not kite:
        return

    # Load company details from the Excel file
    excel_file = 'Companies_by_Sector_with_Details.xlsx'
    try:
        companies_df = pd.read_excel(excel_file)
        logging.info(f"Successfully loaded data from {excel_file}.")
    except FileNotFoundError:
        logging.error(f"Error: Excel file '{excel_file}' not found. Please ensure it's in the same directory.")
        return
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        return

    manage_watchlists(kite, companies_df)

if __name__ == '__main__':
    main()

