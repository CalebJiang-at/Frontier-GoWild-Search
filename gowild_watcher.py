import random, time, requests, json, html
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import argparse
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = None
    msg['To'] = None

    # Credentials
    username = None
    password = None

    if (username == None or password == None):
        print("Please enter your email credentials in gowild_watcher.py")
        return

    # The actual mail send
    server = smtplib.SMTP('smtppro.zoho.com:587')
    server.starttls()
    server.login(username, password)
    server.send_message(msg)
    server.quit()

def get_flight_html(origin, destination, date, session, cjs):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    ]

    header = {"User-Agent": random.choice(user_agents),}
    delay = random.uniform(2, 5)  # Random delay between 2 to 5 seconds
    time.sleep(delay)
    url = f"https://booking.flyfrontier.com/Flight/InternalSelect?o1={origin}&d1={destination}&dd1={date}&ADT=1&mon=true&promo="
    response = session.get(url, headers=header)
    if (response.status_code == 200):
        decoded_data = extract_html(response)
        if (decoded_data != 'NoneType'):
            return extract_json(decoded_data, origin, destination, date)
    else:
        print(f"Problem accessing URL: code {response.status_code}\n url = " + url)
    
    return 0

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
                print(f"\n{origin} to {dest} available:")
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
            body = f"flight {go_wild_count}.\n{flight['stopsText']}\nDate: {info['departureDate'][5:10]}\nDepart: {info['departureDateFormatted']}\nTotal flight time: {flight['duration']}\nPrice: ${flight['goWildFare']}"
            send_email(f"{origin} to {dest}: {go_wild_count} Go Wild flights available for {date.replace('%20', ' ')}", body)
            
            
    if (go_wild_count != 0):
        print(f"{origin} to {dest}: {go_wild_count} Go Wild flights available for {date.replace('%20', ' ')}")
    else:
        print(f"No flights from {origin} to {dest}")
    return go_wild_count

def extract_html(response):
    # Parse the HTML source using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all <script> tags with type="text/javascript" and extract their contents
    scripts = soup.find("script", type="text/javascript")
    decoded_data = html.unescape(scripts.text)
    decoded_data = decoded_data[decoded_data.index('{'):decoded_data.index(';')-1]
    return json.loads(decoded_data)

def main():
    parser = argparse.ArgumentParser(description='Watch for flight availability.')
    parser.add_argument('-o', '--origin', type=str, required=True, help='Origin IATA airport code.')
    parser.add_argument('-d', '--destination', type=str, required=True, help='Destination IATA airport code.')
    parser.add_argument('-t', '--dates', type=str, required=True, help='watch flights for:\n\tToday: 1\n\tTommorrow: 2\n\tBoth: 3')
    
    args = parser.parse_args()
    
    origin = args.origin.upper()
    destination = args.destination.upper()
    input_dates = args.dates

    # Create a session to store cookies
    session = requests.Session()
    cjs = requests.cookies.RequestsCookieJar()
    session.cookies = cjs

    # Get the current date
    today = datetime.today()
    travel_today = today.strftime("%b-%d,-%Y").replace("-", "%20")
    tmrw = today + timedelta(days=1)
    travel_tmrw = tmrw.strftime("%b-%d,-%Y").replace("-", "%20")

    total_count = 0

    if input_dates in ['1','3']:
        print('searching for today')
        total_count += get_flight_html(origin, destination, travel_today, session, cjs)
    if input_dates in ['2','3']:
        print('searching for tommorrow')
        total_count += get_flight_html(origin, destination, travel_tmrw, session, cjs)

    if total_count == 0:
        print('no flights found, retrying in 5 minutes')
        time.sleep(300)
        main()

if __name__ == "__main__":
    main()