import random, time, requests, json, html
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# TODO 
# Speed up processing time
# Better UI
# Do not parse airports where flights are not offered
# Multi-processing ? 

# Global Variables
destination_count = 0
destinations_avail = {}

destinations = {
    'ANU': 'Antigua and Barbuda', 
    'NAS': 'Bahamas', 
    'BZE': 'Belize', 
    'LIR': 'Costa Rica', 
    'SJO': 'San José', 
    'PUJ': 'Punta Cana, DR', 
    'SDQ': 'Santo Domingo, DR', 
    'SAL': 'El Salvador', 
    'GUA': 'Guatemala', 
    'KIN': 'Jamaica', 
    'MBJ': 'St. James', 
    'SJD': 'Los Cabos, MX', 
    'GDL': 'Guadalajara, MX', 
    'PVR': 'Puerto Vallarta, MX', 
    'MTY': 'Monetrrey, MX', 
    'CUN': 'Cancun, MX', 
    'CZM': 'Cozumel, MX', 
    'SXM': 'St. Maarten', 
    'PHX': 'Phoenix', 
    'XNA': 'Arkansas', 
    'LIT': 'Little Rock, AR', 
    'OAK': 'Oakland', 
    'ONT': 'Ontario', 
    'SNA': 'Orange County', 
    'SMF': 'Sacramento', 
    'SAN': 'San Diego', 
    'SFO': 'San Francisco', 
    'DEN': 'Colorado', 
    'BDL': 'Connecticut', 
    'FLL': 'Fort Lauderdale, FL', 
    'RSW': 'Fort Myers, FL', 
    'JAX': 'Jacksonville, FL', 
    'MIA': 'Miami, FL', 
    'MCO': 'Orlando, FL', 
    'PNS': 'Pensacola, FL', 
    'SRQ': 'Sarasota, FL', 
    'TPA': 'Tampa, FL', 
    'PBI': 'West Palm Beach, FL', 
    'ATL': 'Atlanta, Georgia', 
    'SAV': 'Savannah, Georgia', 
    'BMI': 'Illinois', 
    'MDW': 'Chicago', 
    'IND': 'Indiana', 
    'CID': 'Cedar rapids, Iowa', 
    'DSM': 'Des Moines, Iowa', 
    'CVG': 'Kentucky', 
    'MSY': 'Louisiana', 
    'PWM': 'Maine', 
    'BWI': 'Maryland', 
    'BOS': 'Massachusetts', 
    'DTW': 'Michigan', 
    'GRR': 'Grand Rapids, MI', 
    'MSP': 'Minnesota', 
    'MCI': 'Missouri', 
    'STL': 'St. Louis', 
    'MSO': 'Montana', 
    'OMA': 'Nebraska', 
    'LAS': 'Las Vegas', 
    'TTN': 'New Jersey', 
    'BUF': 'New York', 
    'ISP': 'Long Island/Islip', 
    'SWF': 'Newburgh', 
    'LGA': 'New York City', 
    'SYR': 'Syracuse', 
    'CLT': 'North Carolina', 
    'RDU': 'Raleigh, NC', 
    'FAR': 'North Dakota', 
    'CLE': 'Ohio', 
    'CMH': 'Columbus', 
    'OKC': 'Oklahoma', 
    'PDX': 'Oregon', 
    'MDT': 'Pennsylvania', 
    'PHL': 'Philadelphia', 
    'PIT': 'Pittsburgh', 
    'BQN': 'Aguadilla, Puerto Rico', 
    'PSE': 'Ponce, Puerto Rico', 
    'SJU': 'San Juan, Puerto Rico', 
    'CHS': 'Charleston, South Carolina', 
    'MYR': 'Myrtle Beach, SC', 
    'TYS': 'Tennessee', 
    'MEM': 'Memphis', 
    'BNA': 'Nashville', 
    'AUS': 'Austin, Texas', 
    'DFW': 'Dallas/Fort Worth', 
    'ELP': 'El Paso', 
    'IAH': 'Houston', 
    'SAT': 'San Antonio', 
    'STT': 'U.S. Virgin Islands', 
    'SLC': 'Utah', 
    'DCA': 'Virginia', 
    'ORF': 'Norfolk', 
    'SEA': 'Washington', 
    'GRB': 'Wisconsin', 
    'MSN': 'Madison', 
    'MKE': 'Milwaukee'}

def get_flight_html(origin, destinations, date, session):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    ]
    f = open("destinations.txt", "a")
    f.write("Origin: " + origin + "\n")
    for dest in destinations.keys():
        # Choose a random User-Agent header
        header = {
            "User-Agent": random.choice(user_agents)
        }
        # Mimic human-like behavior by adding delays between requests
        delay = random.uniform(2, 5)  # Random delay between 2 to 5 seconds
        time.sleep(delay)
        url = f"https://booking.flyfrontier.com/Flight/InternalSelect?o1={origin}&d1={dest}&dd1={date}&ADT=1&mon=true&promo="
        response = session.get(url, headers=header)
        if (response.status_code == 200):
            decoded_data = extract_html(response)
            if (decoded_data != 'NoneType'):
                extract_json(decoded_data, origin, dest, date)
                f.write(dest + ",")
        else:
            print(f"Problem accessing URL: code {response.status_code}\n url = " + url)
            break
    f.close()
        
def extract_json(flight_data, origin, dest, date):
    # Extract the flights with isGoWildFareEnabled as true
    try:
        flights = flight_data['journeys'][0]['flights']
    except (TypeError, KeyError):
        return
    if (flights == None):
        return
    go_wild_count = 0

    for flight in flights:
        if flight["isGoWildFareEnabled"]:
            if (go_wild_count == 0):
                print(f"\n{origin} to {dest}: {destinations[dest]} available:")
            go_wild_count+=1
            info = flight['legs'][0]
            print(f"flight {go_wild_count}. {flight['stopsText']}")
            print(f"\tDate: {info['departureDate'][5:10]}")
            print(f"\tDepart: {info['departureDateFormatted']}")
            print(f"\tTotal flight time: {flight['duration']}")
            print(f"Price: ${flight['goWildFare']}")
            # if go wild seats value is provided
            if flight['goWildFareSeatsRemaining'] is not None:
                print(f"Go Wild: {flight['goWildFareSeatsRemaining']}\n")
    if (go_wild_count != 0):
        destinations_avail[dest] = destinations.get(dest)
        print(f"{origin} to {dest}: {go_wild_count} Go Wild flights available for {date.replace('%20', ' ')}")
    else:
        print(f"No flights from {origin} to {dest}")
    return

def extract_html(response):
    # Parse the HTML source using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all <script> tags with type="text/javascript" and extract their contents
    scripts = soup.find("script", type="text/javascript")
    decoded_data = html.unescape(scripts.text)
    decoded_data = decoded_data[decoded_data.index('{'):decoded_data.index(';')-1]
    return json.loads(decoded_data)

def print_dests(origin):
    print(f"\n{len(destinations_avail)} destinations found from {origin}:")
    for dest, name in destinations_avail.items():
        print(f"{dest}: {name}")

def main():
    global destinations
    origin = input("Origin IATA airport code: ").upper()
    input_dates = input("Show flights for:\n\tToday: 1\n\tTommorrow: 2\n\tBoth: 3\n\tTo Exit: 0\n")
    today = datetime.today()    
    session = requests.Session()

    if input_dates in ['1','3']:
        # Todays date in URL format
        travel_today = today.strftime("%b-%d,-%Y").replace("-", "%20")
        print("\nFlights for today:")
        get_flight_html(origin, destinations, travel_today, session)
        print_dests(origin)

    if input_dates in ['2','3']:
        # Tomorrows date in URL
        tmrw = today + timedelta(days=1)
        travel_tmrw = tmrw.strftime("%b-%d,-%Y").replace("-", "%20")
        print("\nFlights for tommorrow:")
        get_flight_html(origin, destinations, travel_tmrw, session)
        print_dests(origin)

    if input_dates == '0':
        return
    else:
        print("Retry")
        main()

if __name__ == "__main__":
    main()
