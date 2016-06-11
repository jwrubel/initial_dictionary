import ratebeer
import string


def strip_brewery_name(brewery_name, beer_name):
    brewery_word_list = brewery_name.split()
    for word in brewery_word_list:
        beer_name = beer_name.replace(word, "")
    return beer_name.strip()

categories = []
categories.append("0-9")
for letter in string.ascii_uppercase:
    categories.append(letter)

rb = ratebeer.RateBeer()

with open("eng.user_words",'w') as f:
    for category in categories:
        brewery_list = rb.brewers_by_alpha(category)
        for brewery in brewery_list:
            f.writelines(brewery.name.encode('utf8') + "\n")
            beer_list = brewery.get_beers()
            for beer in beer_list:
                #index the beer name without the bewery too
                beer_name_without_brewery = strip_brewery_name(brewery.name, beer.name)
                f.writelines(beer.name.encode('utf8') + "\n")
                f.writelines(beer_name_without_brewery.encode('utf8') + "\n")
