# TravelWorldSpunky

To make a trip more memorable, hassle free and enjoyable, it is crucial to know about the local services
and events happening around the travel destination. There is a lot of information available about the
events and local services from different sources such as Yelp, Meetup, Eventbrite, Eventful, Locu etc. If
this information can be merged together, the traveler can take into account both the local events and the
local services when planning his/her day and customized recommendations can be made.
We plan to address few such questions through this project. As a case study, we are limiting our data set
to San Francisco.
1. What are the activity (opening/closing times) dynamics of restaurants in different neighborhoods
of San Francisco ?
2. Given the traveler wants to attend a concert, what are the venues and the available food options
within walking distance (may be, 1 mile) ?
3. Given the traveler wants to attend a concert and prefers certain type of food, select the venue with
the best price and minimum distance combination.

In this project we look at restaurants (local services) and concerts (local events) only. But it is easily
scalable for different types of local services, local events and other travel destinations.

Methods of data acquisition include extracting information from RESTful services and web-scraping; methods ofanalysis include visualizing geographical locations of venues on Google Map and implementing a preliminary algorithm of venue recommendation based on the optimization of distance and price. Up until this moment, information of over 400 restaurants and a handful of concert venues in San Francisco has been collected and stored.

We have found interesting patterns in the operating schedule of restaurants across San Francisco and built a recommendation engine to rank the venues. We believe our ideas can be converted into a successful product. As for our future plans, we plan to acquire data from more data sources and customize the services based on the user preferences.
