---
layout: post
title:  "Geocoding MNPS School Locations"
date:   2017-08-22 12:00:00
categories: nashville python
comments: true
---

As I mentioned in a previous post, I did some data reporting at MNPS this past summer. One of the fun problems I got to solve one day was how to plot data by school, on a map in Power BI. Here we are going to use a couple of Python tools to make a database of Latitude / Longitude locations for the MNPS schools. 

Our strategy is:
- Curate a list of addresses for each school (which can be found [here]({{"/assets/SchoolCrosswalk_v1.xlsx" | absolute_url }}))
- Query Google Maps for each address
- Map the addresses / coordinates to the existing school crosswalk
- Save it as a new file

### Getting Search Terms
We start our task by getting a list of schools / departments. Conveniently, these are all in the School Crosswalk. 

{% highlight python %}
import pandas as pd

# Let's read in the School Crosswalk as a Python DataFrame using Pandas
crosswalk_file = 'https://github.com/stkbailey/stkbailey.github.io/blob/master/assets/SchoolCrosswalk_v1.xlsx?raw=true'
df = pd.read_excel(crosswalk_file)

# Print out the first three rows
df.head(3)
{% endhighlight %}


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>MNPS Code</th>
      <th>State Code</th>
      <th>TNC</th>
      <th>School Name (TNC)</th>
      <th>School Name (EBS)</th>
      <th>Location Name (Applitrack)</th>
      <th>Tier</th>
      <th>Quadrant</th>
      <th>Cluster</th>
      <th>Special Status</th>
      <th>Cluster.1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>422</td>
      <td>720</td>
      <td>720</td>
      <td>The Academy at Hickory Hollow</td>
      <td>MNPS TheAcademy-Hickory Hollow</td>
      <td>The Academy at Hickory Hollow</td>
      <td>High</td>
      <td>Southeast</td>
      <td>Cane Ridge</td>
      <td>Non-Zoned</td>
      <td>Cane Ridge</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>7005</td>
      <td>7005</td>
      <td>Cambridge Early Learning Center</td>
      <td>MNPS Cambridge Early Learning</td>
      <td>Cambridge Early Learning Center</td>
      <td>Early Learning Centers</td>
      <td>Southeast</td>
      <td>Cane Ridge</td>
      <td>Non-Zoned</td>
      <td>Cane Ridge</td>
    </tr>
    <tr>
      <th>2</th>
      <td>480</td>
      <td>740</td>
      <td>740</td>
      <td>Johnson Alternative Learning Center</td>
      <td>MNPS Johnson ALC</td>
      <td>Johnson Alternative Learning Center</td>
      <td>High</td>
      <td>Southeast</td>
      <td>Glencliff</td>
      <td>Non-Zoned</td>
      <td>Glencliff</td>
    </tr>
  </tbody>
</table>
</div>




We can also treat each row as its own collection of information:
{% highlight python %}
df.iloc[0]

    MNPS Code                                                422
    State Code                                               720
    TNC                                                      720
    School Name (TNC)              The Academy at Hickory Hollow
    School Name (EBS)             MNPS TheAcademy-Hickory Hollow
    Location Name (Applitrack)     The Academy at Hickory Hollow
    Tier                                                    High
    Quadrant                                           Southeast
    Cluster                                           Cane Ridge
    Special Status                                     Non-Zoned
    Cluster.1                                         Cane Ridge
    Name: 0, dtype: object
{% endhighlight %}


We can now pull individual parts of the df to create a list of search terms we want to use with Google.


{% highlight python %}
print('The first five schools in the Crosswalk...')
print(df['School Name (TNC)'].head(5))

    The first five schools in the Crosswalk...
    0          The Academy at Hickory Hollow
    1        Cambridge Early Learning Center
    2    Johnson Alternative Learning Center
    3     Casa Azafran Early Learning Center
    4         Metro Nashville Virtual School
    Name: School Name (TNC), dtype: object
{% endhighlight %}


But as anyone who has used Google maps knows, if you just use a name, the top search result might end up in Wyoming. So, we actually want to give Google more information than just the school. Let's tell it we're in Nashville.


{% highlight python %}
schools_with_city = df['School Name (TNC)'].apply(lambda x: '{} Nashville TN USA'.format(x))

print('The first five schools, with "Nashville TN" appended...')
print(schools_with_city.head(5))

    The first five schools, with "Nashville TN" appended...
    0       The Academy at Hickory Hollow Nashville TN USA
    1     Cambridge Early Learning Center Nashville TN USA
    2    Johnson Alternative Learning Center Nashville ...
    3    Casa Azafran Early Learning Center Nashville T...
    4      Metro Nashville Virtual School Nashville TN USA
    Name: School Name (TNC), dtype: object
{% endhighlight %}
    

### Talking to Google Maps

We are going to query Google Maps through it's API. Basically, we are searching for a set of keywords - just like if we were searching through the Google Maps app - and then we are going to collect the response in a Python object. Then, we can drill down on that object to get the information we are interested in.


{% highlight python %}
import requests

search_string = 'metro nashville board of education'.replace(' ', '+')
response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(search_string))

response_from_google = response.json()
{% endhighlight %}


{% highlight python %}
from pprint import pprint

# Let's print out Google's response
pprint(response_from_google)

    {'results': [{'address_components': [{'long_name': '2601',
                                          'short_name': '2601',
                                          'types': ['street_number']},
                                         {'long_name': 'Bransford Avenue',
                                          'short_name': 'Bransford Ave',
                                          'types': ['route']},
                                         {'long_name': 'South Nashville',
                                          'short_name': 'South Nashville',
                                          'types': ['neighborhood', 'political']},
                                         {'long_name': 'Nashville',
                                          'short_name': 'Nashville',
                                          'types': ['locality', 'political']},
                                         {'long_name': 'Davidson County',
                                          'short_name': 'Davidson County',
                                          'types': ['administrative_area_level_2',
                                                    'political']},
                                         {'long_name': 'Tennessee',
                                          'short_name': 'TN',
                                          'types': ['administrative_area_level_1',
                                                    'political']},
                                         {'long_name': 'United States',
                                          'short_name': 'US',
                                          'types': ['country', 'political']},
                                         {'long_name': '37204',
                                          'short_name': '37204',
                                          'types': ['postal_code']},
                                         {'long_name': '2811',
                                          'short_name': '2811',
                                          'types': ['postal_code_suffix']}],
                  'formatted_address': '2601 Bransford Ave, Nashville, TN 37204, '
                                       'USA',
                  'geometry': {'location': {'lat': 36.1209504, 'lng': -86.7670156},
                               'location_type': 'ROOFTOP',
                               'viewport': {'northeast': {'lat': 36.1222993802915,
                                                          'lng': -86.7656666197085},
                                            'southwest': {'lat': 36.1196014197085,
                                                          'lng': -86.7683645802915}}},
                  'place_id': 'ChIJxXnGqsRlZIgR6BS97uArY0A',
                  'types': ['establishment', 'point_of_interest', 'school']}],
     'status': 'OK'}
{% endhighlight %}


Now, let's drill in on the data we want, then print out the results.
{% highlight python %}
address = response_from_google['results'][0]['formatted_address']
latitude = response_from_google['results'][0]['geometry']['location']['lat']
longitude = response_from_google['results'][0]['geometry']['location']['lng']

print('For the search string, "', search_string.replace('+', ' '), '", we received...')
print('  Full address: ', address)
print('  Latitude: ', latitude)
print('  Longitude: ', longitude)

    For the search string, " metro nashville board of education ", we received...
      Full address:  2601 Bransford Ave, Nashville, TN 37204, USA
      Latitude:  36.1209504
      Longitude:  -86.7670156
{% endhighlight %}
    

### Scaling up

Now that we know exactly where the data is and how to get it, we need to efficiently get it for each school. We're going to define a function that will take in a search string and return a Pandas series with the Full Address, Latitude and Longitude. 

{% highlight python %}
def getCoords(search_string):
    '''Takes a search term, queries Google and returns the geocoordinates.'''
    index_name = search_string.replace(' Nashville TN USA', '')
    try:
        query = search_string.replace(' ', '+')
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(query))
        response_from_google = response.json()
        \
        address = response_from_google['results'][0]['formatted_address']
        latitude = response_from_google['results'][0]['geometry']['location']['lat']
        longitude = response_from_google['results'][0]['geometry']['location']['lng']
        \
        return pd.Series(name=index_name, \
                         data={'Address': address, 'Latitude': latitude, 'Longitude': longitude})
    except:
        return 'Error'
    
# Now, let's try it out on our central office
print(getCoords('Metro Nashville Board of Education'))

    Address      2601 Bransford Ave, Nashville, TN 37204, USA
    Latitude                                           36.121
    Longitude                                         -86.767
    Name: Metro Nashville Board of Education, dtype: object
{% endhighlight %}
    
It's time to do this for all the schools. We will initialize a new DataFrame and fill it up with data as we get it.

{% highlight python %}
geodf = pd.DataFrame()

for school in schools_with_city:
    data = getCoords(school)
    if type(data) == pd.core.series.Series:
        geodf = geodf.append(data)
        
# Now, let's look at the first ten schools!
geodf.sort_index().head(10)
{% endhighlight %}

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Address</th>
      <th>Latitude</th>
      <th>Longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>The Academy at Hickory Hollow</th>
      <td>5248 Hickory Hollow Pkwy, Antioch, TN 37013, USA</td>
      <td>36.049437</td>
      <td>-86.656720</td>
    </tr>
    <tr>
      <th>Cambridge Early Learning Center</th>
      <td>2325 Hickory Highlands Dr, Antioch, TN 37013, USA</td>
      <td>36.060347</td>
      <td>-86.641187</td>
    </tr>
    <tr>
      <th>Johnson Alternative Learning Center</th>
      <td>1908 Grand Ave, Nashville, TN 37212, USA</td>
      <td>36.147498</td>
      <td>-86.797322</td>
    </tr>
    <tr>
      <th>Metro Nashville Virtual School</th>
      <td>4805 Park Ave, Nashville, TN 37209, USA</td>
      <td>36.150418</td>
      <td>-86.845427</td>
    </tr>
    <tr>
      <th>Glendale Elementary</th>
      <td>800 Thompson Ave, Nashville, TN 37204, USA</td>
      <td>36.095469</td>
      <td>-86.784982</td>
    </tr>
    <tr>
      <th>Harris-Hillman Special Education</th>
      <td>1706 26th Ave, Nashville, TN 37212, USA</td>
      <td>36.137252</td>
      <td>-86.806969</td>
    </tr>
    <tr>
      <th>Cora Howe School</th>
      <td>1928 Greenwood Ave, Nashville, TN 37206, USA</td>
      <td>36.188658</td>
      <td>-86.734767</td>
    </tr>
    <tr>
      <th>Murrell School</th>
      <td>1450 14th Ave S, Nashville, TN 37212, USA</td>
      <td>36.137524</td>
      <td>-86.790181</td>
    </tr>
    <tr>
      <th>W. A. Bass Adult Program</th>
      <td>5200 Delaware Ave, Nashville, TN 37209, USA</td>
      <td>36.154441</td>
      <td>-86.850964</td>
    </tr>
    <tr>
      <th>Middle College High</th>
      <td>120 White Bridge Rd, Nashville, TN 37209, USA</td>
      <td>36.135047</td>
      <td>-86.856507</td>
    </tr>
  </tbody>
</table>
</div>


### Combining with the School Crosswalk

Now that we have a dataframe with the GIS information, we need to re-combine it with the original dataframe. Checking out an entry will show that the new fields are present.

{% highlight python %}
new_crosswalk = df.join(geodf, on='School Name (TNC)')

new_crosswalk.iloc[0]

    MNPS Code                                                                  422
    State Code                                                                 720
    TNC                                                                        720
    School Name (TNC)                                The Academy at Hickory Hollow
    School Name (EBS)                               MNPS TheAcademy-Hickory Hollow
    Location Name (Applitrack)                       The Academy at Hickory Hollow
    Tier                                                                      High
    Quadrant                                                             Southeast
    Cluster                                                             Cane Ridge
    Special Status                                                       Non-Zoned
    Cluster.1                                                           Cane Ridge
    Address                       5248 Hickory Hollow Pkwy, Antioch, TN 37013, USA
    Latitude                                                               36.0494
    Longitude                                                             -86.6567
    Name: 0, dtype: object
{% endhighlight %}



Perfect! If we want, we can now split off other information. To get the city, for example, we want the second comma-separated element in the address.

{% highlight python %}
new_crosswalk.Address.iloc[0:3].apply(lambda x: x.split(',')[1])

    0       Antioch
    1       Antioch
    2     Nashville
    Name: Address, dtype: object
{% endhighlight %} 