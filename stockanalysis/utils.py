from bs4 import BeautifulSoup
import requests

def scrape_stock_data(symbol, exchange):
    
    # Dictionary to hold stock data
    stock_data = {
        "current_price": None,
        "previous_close": None,
        "open_price": None,
        "price_change": None,
        "percentage_changed":None,
        "fifty_two_week_range": None,
        "market_cap": None,
        "pe_ratio": None
        # You can add more fields here as needed
    }

    if exchange in ['NASDAQ', 'NSE']:
        # Properly format the URL with an f-string
        url = f"https://finance.yahoo.com/quote/{symbol}"
    
        
        response = requests.get(url)
        
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all elements with the "fin-streamer" tag
            all_fin_streamers = soup.find_all("fin-streamer")

            # Mapping of data-field attributes to dictionary keys
            field_mapping = {
                "regularMarketPrice": "current_price",
                "regularMarketPreviousClose": "previous_close",
                "regularMarketOpen": "open_price",
                "regularMarketChange": "price_change",
                "regularMarketChangePercent": "percentage_changed",
                "fiftyTwoWeekRange":"fifty_two_week_range",
                "marketCap": "market_cap",
                "trailingPE": "pe_ratio"
                # Add more field mappings here if needed
            }

            # Iterate through all fin-streamer elements
            for fin_streamer in all_fin_streamers:
                try:
                    # Get the field type from the data-field attribute
                    field_type = fin_streamer.get("data-field")
                    data_symbol = fin_streamer.get("data-symbol")
                    
                    # Check if the data-symbol matches the provided symbol
                    if data_symbol == symbol and field_type in field_mapping:
                        # Update the corresponding value in stock_data
                        stock_data[field_mapping[field_type]] = fin_streamer.get('data-value')
                except (TypeError, KeyError, AttributeError) as e:
                    # Handle and log specific errors for this field but continue processing others
                    print(f"Error processing {field_type} for symbol {symbol}: {e}")
                    
        else:
            print(f"Failed to retrieve data from {url}, Status code: {response.status_code}")
            
        # print(stock_data)
        return stock_data
    
    elif exchange == 'NGX':
        # URL for NGX Exchange
        url = "https://ngxgroup.com/exchange/data/equities-price-list/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the table containing the stock data
            table = soup.find("table", {"id": "latestdiclosuresEquities"})
            if table:
                rows = table.find("tbody").find_all("tr")
                
                for row in rows:
                    # The first <td> contains the company symbol, we need to match it
                    company_symbol = row.find("td").get_text(strip=True)
                    
                    if company_symbol == symbol:
                        # Extract relevant data from the columns
                        columns = row.find_all("td")
                        stock_data["previous_close"] = columns[1].get_text(strip=True)
                        stock_data["open_price"] = columns[2].get_text(strip=True)
                        stock_data["current_price"] = columns[5].get_text(strip=True)
                        break
            else:
                print("Could not find the table in the NGX page.")
        else:
            print(f"Failed to retrieve data from {url}, Status code: {response.status_code}")

    return stock_data



# scrape_stock_data('TATAMOTORS.NS', 'NSE')

# # Example call for NGX
# scrape_stock_data('ACCESSCORP', 'NGX')