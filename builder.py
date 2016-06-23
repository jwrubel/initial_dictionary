import ratebeer
import string
import unicodecsv as csv
from io import BytesIO

def strip_brewery_name(brewery_name, beer_name):
    brewery_word_list = brewery_name.split()
    for word in brewery_word_list:
        beer_name = beer_name.replace(word, "")
    return beer_name.strip()

def brewery_name_field(brewery):
    val = getattr(brewery, 'name', 'RateBeer does not have this field filled out for this brewery')
    return val

def beer_description_field(beer):
    val = getattr(beer, 'description', 'no description is available')
    return val

categories = []
categories.append("0-9")
for letter in string.ascii_uppercase:
    categories.append(letter)

unique_beer_names = []

rb = ratebeer.RateBeer()

mapping = open('mapping.csv','w')
kv = csv.writer(mapping, quoting=csv.QUOTE_MINIMAL)
kv.writerow( ('beer name','url','description','full name') )

with open("eng.user_words",'w') as f:
    for category in categories:
        brewery_list = rb.brewers_by_alpha(category)
        for brewery in brewery_list:
            f.writelines(brewery.name.encode('utf8') + "\n")
            beer_list = brewery.get_beers()
            for beer in beer_list:
                try:
                    #index the beer name without the bewery
                    beer_name_without_brewery = strip_brewery_name(brewery.name, beer.name)
                    if beer_name_without_brewery not in unique_beer_names:
                        f.writelines(beer_name_without_brewery.encode('utf8') + "\n")
                        unique_beer_names.append(beer_name_without_brewery)
                    kv.writerow( (beer_name_without_brewery.encode('utf8'),beer.url,beer_description_field(beer).encode('utf8'),brewery_name_field(brewery).encode('utf8')) )
                except Exception: 
                  pass
mapping.close()
