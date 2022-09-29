import flask
from flask_restful import Resource, reqparse
from bs4 import BeautifulSoup
import requests
from models.rightmove import RightmoveModel

location_code = {'location': 'empty'}

# RightMoveCriteria - property criteria one request
class Rightmove(Resource):
    
    def get_arguments(self):
        """ parse request arguments """
        parser = reqparse.RequestParser()  # only allow location changes, no name changes allowed
        parser.add_argument('name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('location', type=str,
                            help='This field cannot be left blank')
        return parser.parse_args()

    def get(self):
        """ returns rightmove location code """
        args = self.get_arguments()
        rm_item = RightmoveModel.find_by_name(args['name'])
        if rm_item:
            return rm_item.json()
        return {"error message": f"item '{args['name']}' not found"}, 404
        
    def post(self):
        """ create rightmove db entry """
        args = self.get_arguments()

        if RightmoveModel.find_by_name(args['name']):
            return {"error message": f"an item with name '{args['name']}' already exists."}, 400
        rm_item = RightmoveModel(args['name'], args['location'])

        try:
            rm_item.save_to_db()
        except:
            return {"error message": f"error occurred inserting the entry '{args['name']}'."}, 500
        return rm_item.json(), 201

    def delete(self):
        """ delete rightmove db entry """
        args = self.get_arguments()

        rm_item = RightmoveModel.find_by_name(args['name'])
        if rm_item:
            rm_item.delete_from_db()

            return {"message": f"item '{args['name']}' has been deleted"}

    def put(self):
        """ create or update rightmove db entry """
        args = self.get_arguments()
        rm_item = RightmoveModel.find_by_name(args['name'])

        if rm_item is None:
            rm_item = RightmoveModel(args['name'], args['location'])
        else:
            rm_item.location = args['location']

        rm_item.save_to_db()

        return rm_item.json()


class RightmoveScraper(Resource):

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

            # web address
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
