# 05318-project

## Description

I built a web fiction recommendation system. My system uses user like and 
dislike ratings to suggest new web fiction to read from the website 
RoyalRoad.com. My system is unique in that it makes suggestions based on the 
text content of fictions, rather than on metadata or other user likes. 
This solves the problem of providing recommendations in environments that have 
few users or user ratings or in environments that do not tag works with 
sufficient metadata for recommendations. My system can be adapted to serve many 
small online communities creating niche text-based works.


## Running

To run: the GH repo contains the index and vector files for works. It does not
contain the raw scraped data to avoid infringing on the authors' works. The
`requirements.txt` contains the list of required packages to operate the system.
The entry point is `flask_main.py`.

## Open-Source Software Used

I performed web scraping with requests, BeautifoulSoup4, and an existing 
RoyalRoad scraper called RoyalRoadLAPI.
I wrote my own code (the `RRIndexScraper` class) with bs4 to scrape the list of 
popular fictions I used. I used RoyalRoadLAPI (with modifications -- see repo 
for changes) to get the list of chapter links for each work.
I used my own code (the `RRScraper` class) to scrape the contents of each 
chapter.

I used the fuzzy matching package `thefuzz` to build the search engine that 
allows searching fictions by name.

I used the spaCy `en-core-web-lg` model to convert chapters into word vectors.
I then averaged these word vectors and normalized them to create the vector
representations of my chapters.

I built the interface using Flask and Bootstrap.
The files for the interface are located in the `/templates` directory.

I wrote the rest of the recommendation system by myself in the `/recommender`
directory, including:
 * Creating an index from downloaded works
 * Creating the vectors for downloaded works from spaCy output
 * Creating an easily human-readable form of the index.
 * Computing the composite vector from a set of fictions.
 * Computing similarity scores between composite vectors and all works.
 * Computing dissimilarity scores between composite vectors and all works.
 * Scaling the scores with a polynomial transform to have mean 50.
 * Making a combined ranking with similarity and dissimilarity scores.
 * Using fuzzy text search of lists of titles to provide recommender rankings.
 * Creating a state representation for the user's likes, dislikes, and excludes.
 * Creating a state manager for the Flask interface that processes requests
    and updates UI data accordingly.
 * Building out the UI and Flask endpoints called by user interactions.
 