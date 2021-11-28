# 05318-project

I built a web fiction recommendation system. My system uses user like and 
dislike ratings to suggest new web fiction to read from the website 
RoyalRoad.com. My system is unique in that it makes suggestions based on the 
text content of fictions, rather than on metadata or other user likes. 
This solves the problem of providing recommendations in environments that have 
few users or user ratings or in environments that do not tag works with 
sufficient metadata for recommendations. My system can be adapted to serve many 
small online communities creating niche text-based works.

## Open-Source Software Used

I performed web scraping with requests, BeautifoulSoup4, and an existing 
RoyalRoad scraper called RoyalRoadLAPI. I wrote my own code with bs4 to scrape
the list of popular fictions I used. I used RoyalRoadLAPI (with modifications 
-- see repo for changes) to get the list of chapter links for each work. I used
my own code to scrape the contents of each chapter.

I used the fuzzy matching package `thefuzz` to build the search engine that 
allows searching fictions by name.

I used the spaCy `en-core-web-lg` model to convert chapters into word vectors.
I then averaged these word vectors and normalized them to create the vector
representations of my chapters.

I built the interface using Flask and Bootstrap.