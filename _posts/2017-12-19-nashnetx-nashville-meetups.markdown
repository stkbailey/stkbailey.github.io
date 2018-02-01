---
layout: post
title:  "NashNetX: Nashville's Web of Networkers"
categories: data-science nashville
date:   2017-12-19 06:45:00
comments: true
---

*This is the third in a series of posts on using NetworkX to analyze Nashville MeetUp data. They are based off a [PyNash talk](https://www.meetup.com/PyNash/events/244713791/) I gave on 11/16, and all data is available on [Github](https://github.com/stkbailey/nashnetx).*

Analyzing one MeetUp is straightforward, and we don't realize many of the benefits of graph theory measures. Now, let's look at a more complex network: the entire Nashville MeetUp scene. 

We'll still focus on our Pythonistas, but instead of looking at who holds PyNash together ("the glue guys / girls"), we'll look at who connects PyNash to the rest of Nashville.

1. Load in and tailor the MeetUp RSVP data.
2. Create a *member-to-member* graph from the *member-to-group* data.
3. Use network metrics to determine member importance.
4. Visualize Nashville MeetUp communities.

But before we get into the real meat... let me give you a taste of where we're going -- the MeetUp relationship graph:

![png]({{"/assets/nashnetx/nashmeet-2.png" | absolute_url }})

Here, each node represents a MeetUp group, and edges represent shared memberships. The location is based off of edge weights - so groups that share a lot of members cluster more closely together. Now - let's build it!

### 1. Load in and tailor the MeetUp RSVP data.


{% highlight python %}
import pandas as pd
import numpy as np
import networkx as nx

# Read in metadata
members = pd.read_csv('data/members.csv', index_col='member_id')
groups = pd.read_csv('data/groups.csv', index_col='group_id')
events = pd.read_csv('data/events.csv', index_col='event_id')

# Read in edge data
rsvps = pd.read_csv('data/rsvps.csv')

# Identify PyNash members 
pynash_events = events.loc[events.group_urlname == 'PyNash'].index
pynash_member_ids = rsvps.loc[rsvps.event_id.isin(pynash_events), 'member_id'].unique()
{% endhighlight %}


{% highlight python %}
print("There are {} unique members and {} unique events.".format(len(rsvps.member_id.unique()), 
                                                                 len(rsvps.event_id.unique())))
{% endhighlight %}

    There are 24631 unique members and 19031 unique events.
    

We want to be a little more particular about how we create this graph, because we have a much larger amount of data than previously. We are also likely less interested in *event attendance* than we are in *group membership*, so let's make a few changes.

- Group RSVPs by MeetUp group
    - Edges will be the number of events attended in a group.
- Threshold membership at at least 2 events to get rid of people who are brand new


{% highlight python %}
# Map event_id --> group_urlname --> group_id
eid2gurl = events.group_urlname.to_dict()
gurl2gid = {v: k for k, v in groups.group_urlname.to_dict().items()}
eid2gid = {k: gurl2gid[v] for k, v in eid2gurl.items()}
rsvps['group_id'] = [eid2gid[x] for x in rsvps.event_id]

# Group by group and threshold
rsvps_group = (rsvps.groupby(['member_id', 'group_id']).size()
                   .reset_index().rename(columns={0: 'weight'}) )
rsvps_group['membership'] = rsvps_group.weight > 1

n_filt, n_keep = rsvps_group.membership.value_counts().values
print('{} members had only attended one event in a group. \n{} members are returning visitors.'.format(n_filt, n_keep))
{% endhighlight %}

>    27588 members had only attended one event in a group. 
>    17995 members are returning visitors.  


{% highlight python %}
# Build Nashville MeetUp graph
g = nx.from_pandas_dataframe(rsvps_group.loc[rsvps_group.membership==True], 
                             'member_id', 'group_id', ['weight'])
node_type_dict = {n: ('member' if n in members.index else 'group') 
                        for n in g.nodes}
nx.set_node_attributes(g, node_type_dict, 'node_type')

# Print summary of nodes
print('The graph has...')
print('{} members'.format(len([n for n in g.nodes if g.nodes[n]['node_type'] == 'member'])))
print('{} groups'.format(len([n for n in g.nodes if g.nodes[n]['node_type'] == 'group'])))
{% endhighlight %}

>    The graph has...
>    11500 members
>    517 groups   

### 2. Create a *member-to-member* graph from the *member-to-group* data.

##### Connected components
One issue we must watch out for is a disconnected graph, where not all nodes are connected. This might happen, for example, if a MeetUp group was a small, special-interest group that did not attract new people. 

NetworkX has some function to handle this situation. First, we can test for connectivity.


{% highlight python %}
nx.is_connected(g)
{% endhighlight %}

>    False



We need to accommodate this somehow. Let's see if there are just a few disconnected nodes.


{% highlight python %}
components = nx.connected_components(g)
components = sorted(list(components), key=len)
component_lengths = [len(x) for x in components]
{% endhighlight %}


{% highlight python %}
print('There are {} connected component graphs.'.format(len(components)))
print('The three largest have {}, {} and {} edges.'.format(component_lengths[-3], component_lengths[-2], component_lengths[-1]))
{% endhighlight %}

    There are 58 connected component graphs.
    The three largest have 13, 15 and 11828 edges.
    

You can see that the vast majority of the graph is connected, with many smaller disconnected fragments. We'll just take the top component and go on our way.


{% highlight python %}
g = nx.subgraph(g, components[-1])
{% endhighlight %}

##### Project bipartite graph

Just as in our bipartite example, we need to project the (member, group) graph to a (member, member) graph. We can get the subset of member_nodes using `nx.bipartite.sets` and then use `weighted_projected_graph` to create the member-member connections.


{% highlight python %}
assert nx.is_bipartite(g) == True

member_nodes, group_nodes = nx.bipartite.sets(g)
gm = nx.bipartite.weighted_projected_graph(g, member_nodes, ratio=False)
{% endhighlight %}

Excellent! We now have a graph with member-to-member connections, where edges represent shared group membership. These people are likely to have run into each other before, or at least to be interested in the same types of things. 

### 3. Use network metrics to determine member importance.


We're going to look at just a few measures:

- **Degree**: the number of individuals a person shares in a group with. This will be higher for people who are part of big groups.
- **Clustering**: the amount of "triangling" in the graph, or the likelihood a person's connections will be connections. High clustering is common in "sub-communities". For example, two people interested in tech are more likely to know each other than one person interested in tech and another in real estate.
- **Centrality**: the relative importance of an individual in "connecting" the network. High centrality means that a person can connect people from different communities in the network. 


{% highlight python %}
def get_graph_measures(centrality_subset_ratio=0.25):
    # Initialize our dataframe
    df = pd.DataFrame(index=gm.nodes)
    df['in_pynash'] = [True if n in pynash_member_ids 
                                   else False for n in gm.nodes]

    # Add in "group" degree from the original graph
    df['num_groups'] = pd.Series(dict(nx.degree(g, member_nodes)))

    # Get member-graph measures
    df['degree'] = pd.Series(dict(nx.degree(gm)))
    df['clustering'] = pd.Series(nx.clustering(gm))

    # Centrality, especially betweenness centrality, is an intensive calculation
    subset_size = np.floor(centrality_subset_ratio * len(g.nodes)).astype(int)
    centrality = nx.betweenness_centrality(gm, k=subset_size, weight='weight')
    df['centrality'] = pd.Series(centrality)

    # Save the member information, since it takes so long to calculate
    df.to_csv('data/nashville_graph_data.csv', encoding='utf8')
    
    return df

overwrite = False
if overwrite == True:
    df_members = get_graph_measures(0.25)
if overwrite == False:
    df_members = pd.read_csv('data/nashville_graph_data.csv', index_col='member_id')

{% endhighlight %}

The pair-plot from the Seaborn library is a great way to visualize multiple variables at once. Let's use it to look at our complete graph.


{% highlight python %}
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
      <th>in_pynash</th>
      <th>num_groups</th>
      <th>degree</th>
      <th>clustering</th>
      <th>centrality</th>
    </tr>
    <tr>
      <th>member_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>198737924</th>
      <td>False</td>
      <td>1</td>
      <td>28</td>
      <td>1.0</td>
      <td>2.144237e-07</td>
    </tr>
    <tr>
      <th>73498632</th>
      <td>False</td>
      <td>1</td>
      <td>88</td>
      <td>1.0</td>
      <td>2.038330e-09</td>
    </tr>
    <tr>
      <th>182943766</th>
      <td>False</td>
      <td>1</td>
      <td>52</td>
      <td>1.0</td>
      <td>4.053242e-08</td>
    </tr>
    <tr>
      <th>216072216</th>
      <td>False</td>
      <td>1</td>
      <td>137</td>
      <td>1.0</td>
      <td>1.851321e-07</td>
    </tr>
    <tr>
      <th>183566364</th>
      <td>False</td>
      <td>1</td>
      <td>88</td>
      <td>1.0</td>
      <td>2.222098e-07</td>
    </tr>
  </tbody>
</table>
</div>




{% highlight python %}
import matplotlib.pyplot as plt
import seaborn as sns 

sns.pairplot(df_members, vars=['num_groups', 'degree', 'clustering', 'centrality'],
             diag_kind='kde')

plt.show()
{% endhighlight %}

![png]({{"/assets/nashnetx/nashmeet-1.png" | absolute_url }})


We can see that, as in PyNash, there are a few highly central people across Nashville, and that these people also tend to have a very high degree. However, the relationship is a little weaker: there are many people with a very high degree that have limited centrality, because they are not connecting "disparate" people - only people who are already connected.

Let's take a look at how our PyNash folk fare.


{% highlight python %}
def print_group_report(member_id,  num_groups=5):
    '''Prints a brief report of a members group affiliations.'''
    gdict = {targ: attr['weight'] for src,targ,attr in g.edges(member_id, data=True)}
    gdf = (pd.DataFrame.from_dict(gdict, orient='index')
               .rename(columns={0: 'events_attended'})
               .join(groups).sort_values(by='events_attended', ascending=False) )

    gdf[['group_name', 'events_attended']]
    
    report_str = '{} ({}) is a member of {} groups.\n'.format(members.loc[member_id, 'name'], member_id, gdf.shape[0])
    report_str += 'Their top attendance rates are:\n'
    max_groups = num_groups if (gdf.shape[0] >= num_groups) else gdf.shape[0]
    for ind, s in gdf.iloc[0:max_groups].iterrows():
        report_str += '- {}: {}\n'.format(s.group_name, s.events_attended)
        
    print(report_str)
{% endhighlight %}


{% highlight python %}
pynash_top_ten = (df_members.loc[df_members.in_pynash==True]
                    .sort_values(by='centrality', ascending=False)
                    .join(members['name']).iloc[0:5]
                    [['name', 'num_groups', 'degree', 'clustering', 'centrality']] )
pynash_top_ten
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
      <th>num_groups</th>
      <th>degree</th>
      <th>clustering</th>
      <th>centrality</th>
    </tr>
    <tr>
      <th>member_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>197928971</th>
      <td>Ted</td>
      <td>12</td>
      <td>1620</td>
      <td>0.143080</td>
      <td>0.015200</td>
    </tr>
    <tr>
      <th>175300482</th>
      <td>Rav</td>
      <td>14</td>
      <td>1556</td>
      <td>0.159742</td>
      <td>0.014787</td>
    </tr>
    <tr>
      <th>221191725</th>
      <td>Omar Ali</td>
      <td>12</td>
      <td>1893</td>
      <td>0.161997</td>
      <td>0.011639</td>
    </tr>
    <tr>
      <th>43237102</th>
      <td>Hameed Gifford</td>
      <td>6</td>
      <td>1167</td>
      <td>0.289286</td>
      <td>0.007896</td>
    </tr>
    <tr>
      <th>187254868</th>
      <td>Andrew Clement</td>
      <td>9</td>
      <td>1568</td>
      <td>0.219833</td>
      <td>0.007346</td>
    </tr>
  </tbody>
</table>
</div>



Nice! Among our attendees are some very connected people. Look at how these highly connected people are a part of different groups, not just "tech" groups. Rav, for example, attends UX, film-making and songwriting MeetUps.


{% highlight python %}
print_group_report(175300482, 8)
{% endhighlight %}

    Rav (175300482) is a member of 14 groups.
    Their top attendance rates are:
    - Nashville UX: 10
    - Nashville Filmmakers: 7
    - Nashville Product Meetup: 7
    - Design Thinking Nashville: 6
    - The Nashville Songwriters Meetup Group: 3
    - WordPress Nashville: 3
    - 20s in Nashville: 3
    - The Nashville Singer, Musician and Songwriter Meetup Group: 2
    
    

What about in all of Nashville? Who are you most likely to know?


{% highlight python %}
nash_top_ten = (df_members.sort_values(by='centrality', ascending=False)
                    .join(members['name']).iloc[0:5]
                    [['name', 'degree', 'clustering', 'centrality']] )
nash_top_ten
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
      <th>degree</th>
      <th>clustering</th>
      <th>centrality</th>
    </tr>
    <tr>
      <th>member_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3949436</th>
      <td>Pablo</td>
      <td>1377</td>
      <td>0.134299</td>
      <td>0.019059</td>
    </tr>
    <tr>
      <th>8539046</th>
      <td>Shalini</td>
      <td>1911</td>
      <td>0.116845</td>
      <td>0.018181</td>
    </tr>
    <tr>
      <th>5900662</th>
      <td>Matt Kenigson</td>
      <td>1811</td>
      <td>0.121181</td>
      <td>0.016951</td>
    </tr>
    <tr>
      <th>197928971</th>
      <td>Ted</td>
      <td>1620</td>
      <td>0.143080</td>
      <td>0.015200</td>
    </tr>
    <tr>
      <th>175300482</th>
      <td>Rav</td>
      <td>1556</td>
      <td>0.159742</td>
      <td>0.014787</td>
    </tr>
  </tbody>
</table>
</div>




{% highlight python %}
print_group_report(3949436, 8)
{% endhighlight %}

    Pablo (3949436) is a member of 16 groups.
    Their top attendance rates are:
    - Eat Love Nash: 9
    - Nashvegans!: 6
    - 20&UP Tennis: Nashville: 6
    - Nashville Spanish Meetup: 5
    - Spiritual Psychology and Consciousness Group: 5
    - Nashville Pilgrimage Hiking & Walking Meetup Group: 5
    - The Joy of Dining Out with Friends Meetup: 4
    - Nashville Tennis Meetup: 4
    
    

### 4. Visualize Nashville MeetUp communities.

We've been talking a lot about individuals, but let's give the groups some love. Which ones tie the Nashville social scene together? 

To do this, we project the bipartite graph onto the group nodes, then calculate our network measures.


{% highlight python %}
gg = nx.bipartite.weighted_projected_graph(g, group_nodes, ratio=False)

# Create groups dataframe
df_groups = pd.DataFrame(index=gg.nodes)
df_groups['num_members'] = pd.Series(dict(nx.degree(g, group_nodes)))
df_groups['degree'] = pd.Series(dict(nx.degree(gg)))
df_groups['clustering'] = pd.Series(nx.clustering(gg))
df_groups['centrality'] = pd.Series(nx.betweenness_centrality(gg, weight='weight'))

df_groups = df_groups.join(groups[['group_name', 'category_name']])
{% endhighlight %}

Let's list out the top groups in terms of centrality - groups that have members drawn from all over the Nashville social scene - and clustering - groups that have a membership shared by many other groups. 


{% highlight python %}
ten_most_central = (df_groups.sort_values(by='centrality', ascending=False)
                        .iloc[0:10] )
print('The ten most inter-connected groups are: ')
for gid, s in ten_most_central.iterrows():
    print('- {} ({})'.format(s.group_name, s.category_name))
{% endhighlight %}

    The ten most inter-connected groups are: 
    - Stepping Out Social Dance Meetup (Dancing)
    - What the Pho! (Food & Drink)
    - Middle TN 40+ singles (Singles)
    - Eat Love Nash (Socializing)
    - Nashville Networking Business Luncheon (Career & Business)
    - Nashville Hiking Meetup (Outdoors & Adventure)
    - 20s in Nashville (Socializing)
    - Sunday Assembly Nashville (Religion & Beliefs)
    - Nashville Online Entrepreneurs (Career & Business)
    - Tennessee Hiking Group (Outdoors & Adventure)
    


{% highlight python %}
ten_most_clustered = (df_groups.loc[df_groups.num_members>20]  # threshold by number of members
                          .sort_values(by='clustering', ascending=False)
                          .iloc[0:10] )
print('The ten most clustered groups are: ')
for gid, s in ten_most_clustered.iterrows():
    print('- {} ({})'.format(s.group_name, s.category_name))
{% endhighlight %}

    The ten most clustered groups are: 
    - R-Ladies Nashville (Career & Business)
    - Nashville Software Automation Professionals (Tech)
    - Nashville API Developers (Tech)
    - freeCodeCamp Nashville (Tech)
    - The Nashville TENNISseans (Sports & Recreation)
    - Nashville Dungeon Delvers (Games)
    - Music City Drinking Buddies (Socializing)
    - Nashville CocoaHeads (Tech)
    - State & Local Government Developers Network (Tech)
    - Nashville Spiritual Experiences Group (New Age & Spirituality)
    

Very interesting! The most central groups are oriented around recreational activities - the outdoors, eating, dancing. The clustered groups, on the other hand, are oriented around hobbies that are more specialized - lots of technology, dungeons & dragons, and of course, drinking.

#### Visualizing communities

To wrap up this analysis, let's plot another graph, but this time let's color groups by categories to see if any trends show up.


{% highlight python %}
from utils import setup_graph_plot

fig, ax = setup_graph_plot(dpi=300)

# Set colors for the graph based on Category name
categories = df_groups.category_name.unique().tolist()
palette = sns.color_palette('hls', len(categories))
color_dict = {}
for ii, cat in enumerate(categories):
    color_dict[cat] = palette[ii]        

# Reduce size of graph
gg_small = gg.subgraph([n for n in gg.nodes if gg.degree[n] > 2])
pos = nx.kamada_kawai_layout(gg_small, scale=1)

# Draw nodes category by category so that legend works easily
for cat in categories:
    node_set = df_groups.loc[df_groups.category_name==cat].index.tolist()
    node_set = [n for n in node_set if n in gg_small.nodes]
    sizes = [500 * df_groups.loc[n, 'centrality'] for n in node_set]
    nx.draw_networkx_nodes(gg_small, pos, nodelist=node_set, node_size=sizes, 
                           node_color=color_dict[cat], label=cat)
# Draw edges
nx.draw_networkx_edges(gg_small, pos, 
                       edgelist=[(s,t) for s,t,d in gg_small.edges(data=True) if d['weight'] > 1],
                       edge_color='xkcd:gray', alpha=0.05)

# Reduce the window width (get rid of nodes on the edges)
w = 0.75
ax.set_xlim([-w, w])
ax.set_ylim([-w, w])

plt.legend(loc='lower center', fontsize=3, mode='expand', ncol=5)

plt.show()
{% endhighlight %}

![png]({{"/assets/nashnetx/nashmeet-2.png" | absolute_url }})


You can see that the Tech groups cluster together quite strongly, as do the "career and business" and "pets and animals" groups. The "singles" group is right at the center of the graph - it crosses all boundaries - as are the "outdoors and adventure" and "socializing" groups.

Thanks for joining me on this journey through Nashville MeetUp data. Ping me if you're interested in doing more!
