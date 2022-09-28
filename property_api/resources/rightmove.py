import flask
import flask_restful
from bs4 import BeautifulSoup
import requests

location_code = {'location': 'empty'}

# RightMoveCriteria - property criteria one request
class Location(flask_restful.Resource):
     
    def get(self):
        """ returns rightmove location code """
        global location_code
        return location_code
    
    def post(self):
        """ receive rightmove location code """
        global location_code
        location = flask.request.get_json()
        
        if len(location['location'])==7 and location['location'].isalnum():
            location_code = location
            return {'location': location_code}, 201

        return {'ERROR Request Format': 'location: <alphanum code length 7>'}, 400


class RightmoveScraper(flask_restful.Resource):

    def get(self):
        """ find available properties based on rightmove url attributes, return dict containing available properties and details """
        global location_code
        # initialise index, this tracks the page number we are on. every additional page adds 24 to the index
        index = 0
        apartments_dict = {}

        for pages in range(1, 42):

            # define our user headers
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
            }

            # email address
            rightmove = f"https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%{location_code['location']}&insId={pages}&radius=0.25&minPrice=700&maxPrice=1200&minBedrooms=1&maxBedrooms=2&displayPropertyType=&maxDaysSinceAdded=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare="

            try:
                res = requests.get(rightmove, headers=headers)  # request webpage
            except:
                break

            res.raise_for_status()  # check status
            soup = BeautifulSoup(res.text, "html.parser")
            
            apartments = soup.find_all("div", class_="l-searchResult is-list")  # get the list of apartments

            # get the number of listings
            number_of_listings = soup.find(
                "span", {"class": "searchHeader-resultCount"}
            )
            number_of_listings = number_of_listings.get_text()
            number_of_listings = int(number_of_listings.replace(",", ""))

            for i in range(len(apartments)):
                
                apartment_no = apartments[i]    # tracks which apartment we are on in the page

                # get link
                apartment_info = apartment_no.find("a", class_="propertyCard-link")
                link = "https://www.rightmove.co.uk" + apartment_info.attrs["href"]

                apartments_dict[f"Address{pages}_{i}"] = link
           
            index = index + 24  # count how many listings we have scrapped already

            if index >= number_of_listings:
                break

        return apartments_dict
