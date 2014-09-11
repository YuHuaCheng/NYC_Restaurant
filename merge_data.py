import json

polygons = json.loads(open('data/nyc-zip-code.json').read())

# This is where we will store the merged data
merged = {
  'type': 'FeatureCollection', 
  'features': []
}

cuisines = {'african': {'file': 'African'}, 'american': {'file': 'American'}, 'asian-fusion': {'file': 'Asian Fusion'}, 'australian': {'file': 'Australian'},'bakery': {'file': 'Bakery'},
  'cafe': {'file': 'Cafe'},'chinese': {'file': 'Chinese'},'eastern_european': {'file': 'Eastern European'},'english': {'file': 'English'},'french': {'file': 'French'},'german': {'file': 'German'},'ice_cream': {'file': 'Ice Cream, Gelato, Yogurt, Ices'},'indian': {'file': 'Indian'},'irish': {'file': 'Irish'},
  'italian': {'file': 'Italian'},'japanese': {'file': 'Japanese'},'jewish': {'file': 'Jewish_Kosher'},'korean': {'file': 'Korean'},'latin_american': {'file': 'Latin American'},'mediterranean': {'file': 'Mediterranean'},'mexican': {'file': 'Mexican'},'middle_eastern': {'file': 'Middle Eastern'},'pizza': {'file': 'Pizza'},
  'portuguese': {'file': 'Portuguese'},'russian': {'file': 'Russian'},'salad': {'file': 'Salads'},'sandwiches': {'file': 'Sandwiches'},'scandinavian': {'file': 'Scandinavian'},'seafood': {'file': 'Seafood'},'soups': {'file': 'Soups'},'southeastern_asian': {'file': 'Southeastern Asian'},'spanish': {'file': 'Spanish'},
  'vegetarian': {'file': 'Vegetarian'}}

for polygon in polygons['features']:
  # Use all data from zip-code file.
  feature = polygon
  
  # Extract zip code
  zip_code = feature['properties']['postalCode']

  # Initialize cuisines
  feature['properties']['cuisines'] = {}

  for cuisine in cuisines: 
    ## <(") Load restaurant data
    filename = 'data/' + cuisines[cuisine]['file'] + '.json'
    cuisine_data = json.loads(open(filename).read())

    # Initialize attributes
    avg_rating = avg_price = avg_grade = num_restaurants = 0

    ## <(") Get restaruant data for zip_code
    if zip_code in cuisine_data:
      num_restaurants = cuisine_data[zip_code][0]
      avg_rating = cuisine_data[zip_code][1]
      avg_price = cuisine_data[zip_code][2]
      avg_grade = cuisine_data[zip_code][3]

    # Insert restaurant properties
    feature['properties']['cuisines'][cuisine] = {'filtered': True}
    feature['properties']['cuisines'][cuisine]['avgRating'] = avg_rating
    feature['properties']['cuisines'][cuisine]['avgPrice'] = avg_price
    feature['properties']['cuisines'][cuisine]['avgGrade'] = avg_grade
    feature['properties']['cuisines'][cuisine]['numRestaurants'] = num_restaurants

  # Add merged feature into dataset
  merged['features'].append(feature)

# Output to file
prefix = 'var nycdata = '
suffix = ';'

with open('data/data.geojson', 'w') as ofile:
  ofile.write(prefix + json.dumps(merged) + suffix)
