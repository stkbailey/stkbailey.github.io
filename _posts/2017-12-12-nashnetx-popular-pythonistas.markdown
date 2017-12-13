---
layout: post
title:  "NashNetX: Popular Pythonistas"
categories: data-science
date:   2017-12-12 06:45:00
comments: true
---

*This is the third in a series of posts on using NetworkX to analyze Nashville MeetUp data. They are based off a [PyNash talk](https://www.meetup.com/PyNash/events/244713791/) I gave on 11/16, and all data is available on [Github](https://github.com/stkbailey/nashnetx).*

Now, we come to the real thing. Who are the most important Pythonistas in Nashville?

We will follow a similar setup to last time, but with a few minor twists. We will have to translate our (person, event) edges to (person, person) edges using a *bipartite* "projection". We also need to spend a little more time thinking through what implications this has for our measures.

Our plan is to:

1. Load in and subset the MeetUp RSVP data.
2. Create a *member-to-member* graph from the *member-to-event* data.
3. Use "degree" and "betweenness centrality" to determine member importance.

### 1. Load in and subset the MeetUp RSVP data.

First, we load our packages and full datasets.

{% highlight python %}
import pandas as pd
import numpy as np

# Read in metadata
members = pd.read_csv('data/members.csv', index_col='member_id')
groups = pd.read_csv('data/groups.csv', index_col='group_id')
events = pd.read_csv('data/events.csv', index_col='event_id')

# Read in edge data
rsvps = pd.read_csv('data/rsvps.csv')
{% endhighlight %}

The group_id for PyNash is **11625832**, so we can limit our analysis to only those events in that list. 


{% highlight python %}
# Get PyNash events
pynash_id = 11625832
pynash_event_ids = events.loc[events.group_urlname == 'PyNash'].index.tolist()

# Get list of unique member_ids attending a PyNash event
pynash_rsvps = rsvps.loc[rsvps.event_id.isin(pynash_event_ids)]
pynash_member_ids = pynash_rsvps['member_id'].unique().tolist()

print('There are {} PyNash events.'.format(len(pynash_event_ids)))
print('There are {} PyNash attendees.'.format(len(pynash_member_ids)))
{% endhighlight %}

> There are 46 PyNash events.
> There are 526 PyNash attendees.
    

#### Build the graph with NetworkX


{% highlight python %}
import networkx as nx

g = nx.from_pandas_dataframe(pynash_rsvps, 
                             source='member_id', 
                             target='event_id')

# Add "Node Type" attribute 
node_type_dict = {n: ('member' if n in pynash_member_ids else 'event') 
                        for n in g.nodes}
nx.set_node_attributes(g, node_type_dict, 'node_type')
{% endhighlight %}

#### Plot the PyNash graph


{% highlight python %}
import matplotlib.pyplot as plt
from utils import setup_graph_plot

fig, ax = setup_graph_plot(dpi=200)

pos = nx.spring_layout(g)
colors = ['xkcd:muted green' if g.nodes[n]['node_type'] == 'member'
              else 'xkcd:bright red' for n in g.nodes]
nx.draw_networkx_nodes(g, pos, node_color=colors, node_size=5,
                       with_labels=False)
nx.draw_networkx_edges(g, pos, alpha=0.05)

# Draw a legend
handles = [plt.Line2D(range(1), range(1), color="white", marker='o', markerfacecolor="xkcd:muted green"), 
           plt.Line2D(range(1), range(1), color="white", marker='o', markerfacecolor="xkcd:bright red")]
plt.legend(handles, ['Members', 'Events'], frameon=False)

plt.show()
{% endhighlight %}


![png]({{"/assets/nashnetx/pynash-1.png" | absolute_url }})



### 2. Create a *member-to-member* graph from the *member-to-event* data.

We have all the data we need - we simply need to project it into the correct format. There are a few functions in `nx.bipartite` that can help us do this. 

But let's recall what is special about a bipartite graph:

1. There are two distinct sets of nodes. 
    - There are connections *between* sets.
    - Therea are no connections *within* sets. 
2. This data is common when you have "affiliation" data where you have one type of data that is a person and another type that is a thing.

We can test for bipartite-ness in NetworkX. We can also pull out the sets automatically.


{% highlight python %}
nx.is_bipartite(g)
{% endhighlight %}




>    True




{% highlight python %}
member_nodes, event_nodes = nx.bipartite.sets(g)
print('There are {} members and {} events.'.format(len(member_nodes), len(event_nodes)))
{% endhighlight %}

>    There are 526 members and 46 events.
    

To get the projected graphs, we use the `weight_projected_graph` function. This will create a member graph with the following properties:

- Nodes are member_ids.
- Edges are the number of shared events between two members.


{% highlight python %}
gm = nx.bipartite.weighted_projected_graph(B=g, nodes=member_nodes, ratio=False)

# You can do the same for events
ge = nx.bipartite.weighted_projected_graph(g, event_nodes, False)
{% endhighlight %}

### 3. Use "degree" and "betweenness centrality" to determine importance.

Finally, we are going to measure different aspects of our graph. Most


{% highlight python %}
# Initialize df
df_members = pd.DataFrame(index=gm.nodes)

# Add graph measures
df_members['num_events'] = pd.Series(dict(g.degree)) #"DegreeView" must be converted to dict
df_members['degree'] = pd.Series(dict(gm.degree))
df_members['centrality'] = pd.Series(nx.betweenness_centrality(gm))

# Sample output
df_members.head()
{% endhighlight %}




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>num_events</th>
      <th>degree</th>
      <th>centrality</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>58462212</th>
      <td>1</td>
      <td>75</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>214085642</th>
      <td>1</td>
      <td>70</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>197928971</th>
      <td>2</td>
      <td>82</td>
      <td>0.000169</td>
    </tr>
    <tr>
      <th>66609162</th>
      <td>1</td>
      <td>65</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>2069</th>
      <td>4</td>
      <td>52</td>
      <td>0.001035</td>
    </tr>
  </tbody>
</table>
</div>




{% highlight python %}
import seaborn as sns

sns.pairplot(data=df_members, diag_kind='kde')
plt.suptitle('Distributions and Correlations \nBetween Graph Theory Measures', 
             y=1.05, fontsize=18)

plt.show()
{% endhighlight %}


![png]({{"/assets/nashnetx/pynash-2.png" | absolute_url }})


A few things become apparent within the PyNash graph:

1. Degree is strongly correlated with number of events attended.
2. Centrality increases exponentially relative to degree.
3. Centrality is more skewed than the other metrics -- there are only a few highly central people.

But who is are they???


{% highlight python %}
top_ten = df_members.sort_values(by='centrality', ascending=False).head(10).join(members)
top_ten[['name', 'city', 'num_events', 'degree', 'centrality']]
{% endhighlight %}




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>city</th>
      <th>num_events</th>
      <th>degree</th>
      <th>centrality</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>121334792</th>
      <td>Greg Back</td>
      <td>Hendersonville</td>
      <td>27</td>
      <td>403</td>
      <td>0.055124</td>
    </tr>
    <tr>
      <th>57907252</th>
      <td>Chad Upjohn</td>
      <td>Nashville</td>
      <td>25</td>
      <td>459</td>
      <td>0.053080</td>
    </tr>
    <tr>
      <th>30123762</th>
      <td>Jason Myers</td>
      <td>Nashville</td>
      <td>25</td>
      <td>237</td>
      <td>0.040602</td>
    </tr>
    <tr>
      <th>2896514</th>
      <td>Trey Brooks</td>
      <td>Nashville</td>
      <td>15</td>
      <td>331</td>
      <td>0.037175</td>
    </tr>
    <tr>
      <th>184547023</th>
      <td>Chris Jarvis</td>
      <td>Nashville</td>
      <td>19</td>
      <td>347</td>
      <td>0.031768</td>
    </tr>
    <tr>
      <th>12140530</th>
      <td>Bill Israel</td>
      <td>Nashville</td>
      <td>16</td>
      <td>378</td>
      <td>0.028138</td>
    </tr>
    <tr>
      <th>202882025</th>
      <td>Michael mead</td>
      <td>Nashville</td>
      <td>16</td>
      <td>396</td>
      <td>0.027081</td>
    </tr>
    <tr>
      <th>13606604</th>
      <td>Alex Simonian</td>
      <td>Nashville</td>
      <td>15</td>
      <td>343</td>
      <td>0.021315</td>
    </tr>
    <tr>
      <th>126309962</th>
      <td>Aliya Gifford</td>
      <td>Nashville</td>
      <td>15</td>
      <td>348</td>
      <td>0.020821</td>
    </tr>
    <tr>
      <th>4393825</th>
      <td>Chris Fonnesbeck</td>
      <td>Nashville</td>
      <td>13</td>
      <td>316</td>
      <td>0.019495</td>
    </tr>
  </tbody>
</table>
</div>



One revealing thing comes out: Jason Myers has a degree that is almost 100 less than everyone else in the top ten. Yet he is number 3 on the list! How can this be?

The answer lies in PyNash's event offerings, which break into two categories: 

- PyNash Lunch - attended by a small number of regulars 
- PyNash Talks - attended by a large number of regulars and newbies

Let's take a look at the attendance records for Jason Myers and Chad Upjohn:


{% highlight python %}
print('**PyNash Attendance for Jason Myers**')
print(pynash_rsvps.loc[pynash_rsvps.member_id==30123762]
     .set_index('event_id')
     .join(events).name
     .value_counts() )

print('\n')
print('**PyNash Attendance for Chad Upjohn**')
print(pynash_rsvps.loc[pynash_rsvps.member_id==57907252]
     .set_index('event_id')
     .join(events).name
     .value_counts() )
{% endhighlight %}

>    **PyNash Attendance for Jason Myers**  
>    PyNash Lunch!                                                                    23  
>    PyNash: Virtualenv/Virtualenvwrapper(Bill Israel), Code Analysis(Jason Myers)     1  
>    You and I and the PyNash API                                                      1  
>    Name: name, dtype: int64   
>    
> 
> **PyNash Attendance for Chad Upjohn**  
>    PyNash Lunch!                                                                    5  
>    Logging beyond /dev/null -- ELK Stack for Log Visualization and Analysis         1  
>    A Beginners Guide to Supervised Machine Learning with scikit-learn               1  
>    A Brief Introduction to Concurrency and Coroutines in Python 3.5                 1  
>    Intro to Profiling in Python                                                     1  
>    An October Two-fer: Refactoring, Extra Code Included / PDFs Against Humanity     1  
>    Interactive Python Environments: IPython, Jupyter, and Beaker, Oh My!            1  
>    A Gentle, Pythonic Introduction to Operating Systems                             1  
>    PyNash: Virtualenv/Virtualenvwrapper(Bill Israel), Code Analysis(Jason Myers)    1  
>    PyNash x Penny U: An Evening of Learning                                         1  
>    Capacity and Stability Patterns                                                  1  
>    An Introduction to Django Channels                                               1  
>    Ü is for Üńîçřdé: Solving the Mystery and a TBD                                  1  
>    Test Driving Pytest                                                              1  
>    ?A Quick Sip from the Flask Microframework                                       1  
>    Creating Better Beer Through Data Science                                        1  
>    You and I and the PyNash API                                                     1  
>    datetime in Python: What Time is it Anyway?                                      1  
>    PyNash Fishbowl                                                                  1  
>    Elasticsearch in an Evening                                                      1  
>    Getting Started with Data Science using Python                                  1  
>    Name: name, dtype: int64  
   

The reason for Jason's uncharacteristically high centrality is that he has RSVPed to nearly all the lunches, while others have gone to higher "degree-granting" events. Consequently, Jason is deeply embedded within the social fabric of the graph (many links to the most important people), despite not having as broad of a reach himself.

#### Draw Member Graph

To conclude, let's take a quick look at the member graph to drive home the fact that PyNash is held together by a small group of highly connected individuals. First, we take a look at the graph representation.


{% highlight python %}
import matplotlib as mpl
from utils import setup_graph_plot

fig, ax = setup_graph_plot(figsize=(5,5), dpi=150)

member_pos = nx.spring_layout(gm, k=1)

# Create a centrality-weighted colormap for the nodes
from matplotlib import colors
norm = colors.Normalize(vmin=-0.2, vmax=df_members.centrality.max())

nx.draw_networkx_nodes(gm, member_pos, alpha=1, 
                       node_size=[1000*x for x in df_members.centrality],
                       node_color=[norm(x) for x in df_members.centrality], 
                       cmap=plt.cm.Reds)
nx.draw_networkx_edges(gm, member_pos, alpha=0.008)

plt.title('PyNash Members, Emphasizing Centrality')

plt.show()
{% endhighlight %}


![png]({{"/assets/nashnetx/pynash-3.png" | absolute_url }})


Next, let's check out the adjacency matrix, which can sometimes make edge patterns clearer. Let's sort by centrality to see what sorts of patterns we can make out in the edge relationships.

As you go further down and right, individuals have a much higher number of edges. In fact, the last ten or fifteen rows/columns are connected to almost every other member in the graph -- these are our top Pythonistas. 


{% highlight python %}
fig, ax = setup_graph_plot(dpi=150)

node_order = df_members.sort_values(by='centrality').index
adjmat_weighted = nx.to_numpy_array(gm, nodelist=node_order)
adjmat_binary = weighted_adjmat > 0

ax.imshow(adjmat_binary, cmap='hot')

plt.title('Adjacency Matrix for PyNash,\nSorted by Centrality')
plt.show()
{% endhighlight %}

![png]({{"/assets/nashnetx/pynash-4.png" | absolute_url }})
