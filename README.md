# Frontier-GoWild-Search

# Frontier Airlines GoWild Flight Scraper Destination Finder

This program allows users with Frontier Airlines' GoWild all-you-can-fly pass to quickly check the availability of flights to all different destinations. By scraping Frontier Airlines' website, the program provides information on flights available for the current day or the next day from the specified origin airport.
This program is designed for those with the GoWild pass who embrace the spontinaity of it and want to see all available adventures they can take within the 24-hour booking period. 

## Prerequisites

Before running the program, ensure that you have the following dependencies installed:

- Python 3.x installed on your system
- Required Python packages: `random`, `time`, `requests`, `json`, `html`, `BeautifulSoup`, `datetime`
To install the required dependencies, use the following command:
```
pip install requests beautifulsoup4
```

## Usage

1. Open the terminal or command prompt and navigate to the directory where the program is located.
2. Run the program using the following command:
   ```
   python frontier_flight_scraper.py
   ```
3. Enter the origin airport IATA code when prompted. For example, enter "DEN" for Denver International Airport.
4. Choose the option to show flights for today, tomorrow, both, or to exit.
   - Enter `1` to show flights for today.
   - Enter `2` to show flights for tomorrow.
   - Enter `3` to show flights for both today and tomorrow.
   - Enter `0` to exit the program.
5. The program will scrape Frontier Airlines' website for available flights and display the results.
6. The program will scrape Frontier Airlines' website to retrieve the flight information and display it on the terminal.

7. *The program will generate a file named `destinations.txt` that lists the origin airport and the available destinations.
   (This intended for future development to streamline scraping only for availible destinations)*

Note: The program includes random delays between requests to mimic human-like behavior and avoid being blocked by the website. The delays are between 2 to 5 seconds.

## Limitations

- This program specifically targets Frontier Airlines' website and may not work with other airline websites or travel platforms.
- The program relies on web scraping techniques, which can be affected by changes in the website's structure or layout. If the website structure changes, the program may need to be updated accordingly.
- Frontier Airlines' website may have usage restrictions or rate limiting in place. Running the program too frequently or making too many requests in a short period could lead to IP blocking or other issues. It is recommended to use the program responsibly and respect the website's terms of service.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgements

- This program uses the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library for HTML parsing.
- The flight data is obtained from Frontier Airlines' website.

## Disclaimer

This program is for educational purposes only. Use it responsibly and respect the website's terms of service. The program may become outdated or incompatible with website updates. The developers are not responsible for any misuse or consequences caused by using this program.

If you encounter any issues or have suggestions for improvements, please feel free to contribute or open an issue in the project repository.

I would love further contributions from fellow lovers of travel and innovation. 

This program was mainly an educational personal project for myself. It is inspired and driven by my own impatience and excitment of having the 'all you can fly' oppertunity.

That being said there are many imperfections and areas of improvement to make this program more efficient and user friendly. 

I'm making this repo public so maybe I can help other travelers and learn more from other possible contributors. 

### Happy flying!!!

### Example output:

```
DEN to MKE: Milwaukee available:
flight 1. 1 Stop LAS
        Date: 06-27
        Depart: 10:05 AM
        Total flight time: 9 hrs 35 min
Price: $24.21
flight 2. 1 Stop LAS
        Date: 06-27
        Depart: 12:00 PM
        Total flight time: 7 hrs 40 min
Price: $24.21
flight 3. 1 Stop LAS
        Date: 06-27
        Depart: 5:35 AM
        Total flight time: 14 hrs 5 min
Price: $29.81
flight 4. 1 Stop LAS
        Date: 06-27
        Depart: 7:53 AM
        Total flight time: 11 hrs 47 min
Price: $29.81
DEN to MKE: 4 Go Wild flights available for Jun 27, 2023

52 destinations found from DEN:
NAS: Bahamas
PUJ: Punta Cana, DR
GUA: Guatemala
MBJ: St. James
CUN: Cancun, MX
....
```
