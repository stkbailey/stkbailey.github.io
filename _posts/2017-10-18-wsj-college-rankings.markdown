---
layout: post
title:  "Geo-diving into the WSJ College Rankings"
date:   2017-10-18 05:38:00
categories: data-science power-bi
comments: true
---

How many top colleges are in your state? That was one of the questions I had after reading this year's [THE/Wall Street Journal's 2018 college rankings](https://www.timeshighereducation.com/rankings/united-states/2018#!/page/0/length/25/sort_by/rank/sort_order/asc/cols/stats). Since I'm in the middle of writing a few manuscripts for my dissertation and needed a "break" (i.e. diversion), I decided to answer it.

<iframe width="750" height="500" src="https://app.powerbi.com/view?r=eyJrIjoiYWM3MmYzODktNmMwNi00NjQ3LWFlY2QtY2I3MWMxN2JiY2NkIiwidCI6ImJhNWE3ZjM5LWUzYmUtNGFiMy1iNDUwLTY3ZmE4MGZhZWNhZCIsImMiOjN9" frameborder="0" allowFullScreen="true"></iframe>

Here are some of the most interesting insights:
- The Northeast has the most colleges in the Top 100 (46 of them!) but nearly 100% are private.
- Massachussets, California and New York make up about 30% of the Top 100. Ohio and Pennsylvania are an additional 15%.
- As you go down the rankings, the starting salary to loan default rate decreases dramatically.
- Going to a public or private school doesn't make a huge difference on salary -- unless you are in the Northeast or Mountain division, where going to private school will be worth $6-8k (median difference across schools).

#### Methodology
The rankings  explore four key areas. A full description of the methodology is available on [the report's website](https://www.timeshighereducation.com/the-wall-street-journal-times-higher-education-college-rankings-2017-table-information).

- Resources: Does the college have the capacity to effectively deliver teaching? The Resource area represents 30 per cent of the overall ranking.
- Engagement: Does the college effectively engage with its students? Most of the data in this area is gathered through the THE US Student Survey. The Engagement area represents 20 per cent of the overall ranking. 
- Outcomes: Does the college generate good and appropriate outputs? Does it add value to the students who attend? The Outcomes area represents 40 per cent of the overall ranking. 
- Environment: Is the college providing a learning environment for all students? Does it make efforts to attract a diverse student body and faculty? The Environment area represents 10 per cent of the overall ranking. 

To get the data, I downloaded the PDFs of the tables from the WSJ site and then used an OCR application to convert it to text. It didn't get all of the data -- there are about 25 schools I'm currently missing, but it worked for most. I then mapped the names/location to the geocoordinates and census regions to break out the data by area.

You can also view the report on [Power BI Service](https://app.powerbi.com/view?r=eyJrIjoiYWM3MmYzODktNmMwNi00NjQ3LWFlY2QtY2I3MWMxN2JiY2NkIiwidCI6ImJhNWE3ZjM5LWUzYmUtNGFiMy1iNDUwLTY3ZmE4MGZhZWNhZCIsImMiOjN9). Data is housed in a [Github repo](https://github.com/stkbailey/WSJ_CollegeRankings2018).
