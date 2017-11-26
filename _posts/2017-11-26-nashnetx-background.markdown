---
layout: post
title:  "NashNetX: Background & Motivation"
categories: data-science
date:   2017-11-26 06:00:00
comments: true
---

Who are the kings and queens of the Nashville MeetUp scene? 

That's the question we want to answer today. And to do that, we're going to use a branch of mathematics called **Graph Theory** and **[NetworkX](https://networkx.github.io/)**, an excellent Python package for network analysis. 

In this post, we discuss:

1. What is a graph?
2. Types of graphs
3. Modeling Nashville's MeetUp scene

### 1. What's a graph?

Graphs are mathematical structures used to model pairwise relations between objects. A graph in this context is made up of **nodes** connected by **edges**. 

Graphs were first used by Leonhard Euler, a Swiss mathematician, to solve the *Seven Bridges of Konigsberg* problem. The problem was simple: Konigsberg had four land masses connected by seven bridges. Was it possible to traverse every bridge once?

![The seven bridges of Konigsberg]({{ "../assets/nashnetx/konigsberg_land.jpg" | absolute_url }}  =250x250)

However, the answer could not be solved through traditional means, so Euler decided to invent a whole new branch of mathematics. Euler reasoned thus:

1. We do not care about the properties of the land or bridges, only that they are connected.
2. To enter/exit a land mass, one must traverse two bridges connected to the land mass. Therefore, a land mass must have either 2 or 4 or 6 (or 8...) bridges to be able to enter AND exit it.
3. The first and last land masses may have 1 bridge each. (But if the start has one bridge, the end MUST also have one.)
4. Therefore, every land mass must have an even number of bridges, or two land masses may have an odd number of bridges. 

![The seven edges of Konigsberg]({{ "/assets/nashnetx/konigsberg_graph.png" | absolute_url }})

So, the answer is no, the seven bridges are not traversible. But Euler's reasoning about how *relationships* between things may be conceived of mathematically has stuck. Graph theory is now a popular analytical approach in all kinds of domains, including technology, social networks and the human brain! 

### 2. Types of graphs

There are many types of graphs. The most simple one is *undirected* and *unweighted*: each node has a binary relationship with every other node, like in the bridge problem. Some other properties include:

- **Undirected**: A graph with undirected edges means there is no directionality between two nodes. Examples: most streets/bridges, power grid, social networks.
- **Directed**: Directed edges indicate that the connection between two nodes is asymmetric: there is a source and target for the connection. Examples: sending/recieving e-mail, internet links, imports/exports between countries.
- **Unweighted**: An edge is either present or not, and all edges are the same. Examples: Facebook "friends", contacts in a phone.
- **Weighted**: Some edges are weighted more highly than others, allowing the edge to be more important in graph measures. Examples: An eight-lane highway vs. a two lane road, commonality of interests (5 interests vs. 2 interests.

Additionally, there are different classes of graphs, including:

- **Bipartite**: Bipartite graphs have two "sets" of nodes that are not connected within themselves - only between, giving them useful properties, such as the ability to "project" graphs onto one set or the other. Examples: Sports fans are connected to sports teams (but not to each other), people have interests (but not direct connections to each other).
- **MultiGraph**: A multigraph has higher dimensionality, allowing a node to be connected in one dimension but not another. Examples: A person has a work relationship but not a social relationship with their manager.
- **Disconnected**: Disconnected graphs have multiple component graphs that are not connected to each other, meaning that "information" cannot pass between them. Disconnected graphs are common in real applications and also useful for identifying nodes that are important for tying together the graph. 


### 3. Modeling Nashville's MeetUp scene

To construct our MeetUp network, we first have to decide the best way to model our problem. A few options are:

- Members connected by shared events attendance.
- Members connected by shared group membership.
- Members connected by shared interests.
- Groups connected by shared membership (or event attendance).
- Events connected by shared attendance (i.e., does each event attract the same crowd or new crowds?)

For this project, we'll proceed with option one: *members connect by shared event attendance*. The bare minimum data we will need, therefore, is data in the form of (*Meetup Member ID*, *MeetUp Event ID*), where each instance represents a person RSVPing "yes" to an event.

Additional information will also be useful, however -- grouping events by "Group" and labeling members by name will enrich our understanding of the structures of the graph and make measures more useful. 

In the next post, we'll talk about how to get this data and get started with MeetUp!
