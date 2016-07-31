import ratebeer
import string
import unicodecsv as csv
import re
from io import BytesIO

def strip_parens(beer):
    p = re.compile(r'\([^)]*\)')
    return re.sub(p, '', beer)

def strip_brewery_name(brewery_name, beer_name):
    brewery_word_list = brewery_name.split()
    for word in brewery_word_list:
        beer_name = beer_name.replace(word, "")
    return beer_name.strip()

def brewery_name_field(brewery):
    val = getattr(brewery, 'name', 'RateBeer does not have this field filled out for this brewery')
    return val


categories = []
categories.append("0-9")
for letter in string.ascii_uppercase:
    categories.append(letter)

unique_beer_words = []

rb = ratebeer.RateBeer()

mapping = open('mapping.csv','w')
kv = csv.writer(mapping, quoting=csv.QUOTE_MINIMAL)
kv.writerow( ('beer_name','url','brewery_name') )

with open("eng.user_words",'w') as f:
    for category in categories:
        brewery_list = rb.brewers_by_alpha(category)
        for brewery in brewery_list:
            try:
                brewery_name = strip_parens(brewery.name)
                brewery_name = brewery_name.strip()
                brewery_words = brewery_name.split(" ")
                for word in brewery_words:
                    if word not in unique_beer_words:
                        f.writelines(word.encode('utf8') + "\n")
                        unique_beer_words.append(word)
                beer_list = brewery.get_beers()
                for beer in beer_list:
                    try:
                        # get rid of parens
                        beer_name = strip_parens(beer.name)
                        # if it contains a / only use what's to the right of it
                        beer_name = beer_name.rsplit('/', 1)[-1]
                        #leading and trailing spaces
                        beer_name = beer_name.strip()
                        # if the beer has fewer than three words when the
                        # brewery name is removed and there is no dash character,
                        # use the full name otherwise use the beer name
                        # without the brewery
                        beer_without_brewery = strip_brewery_name(brewery_name, beer_name)
                        beer_without_brewery_word_count = beer_without_brewery.split(" ")
                        if (len(beer_without_brewery_word_count) > 2) and ("-" not in beer_without_brewery):
                            beer_name = beer_without_brewery
                        beer_words = beer_name.split(" ")
                        for word in beer_words:
                            # ignore weird garbage characters in the name
                            if len(word) > 1:
                                if word not in unique_beer_words:
                                    f.writelines(word.encode('utf8') + "\n")
                                    unique_beer_words.append(word)
                        kv.writerow( (beer_name.encode('utf8'),beer.url,brewery_name.encode('utf8')) )
                    except Exception, e:
                        print str(e)
                        pass
            except Exception:
              pass
mapping.close()
