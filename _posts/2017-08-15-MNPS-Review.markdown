---
layout: post
title:  "Visualizing MNPS Vacancies"
date:   2017-08-15 12:00:00
categories: data-science power-bi
---

This summer, I had the pleasure of completing a brief stint as a Data Analyst at Metro Nashville Public Schools. I got to work with a great group of people, including Sharon Pertiller and Amber Tyus in the Human Resources department, and to learn a new tool: [Microsoft Power BI](https://powerbi.microsoft.com/en-us/).

MNPS has pockets of excellent data work happening all over the place -- most notably in their [Data Warehouse](http://nashvillecitypaper.com/content/city-news/metro-schools-data-warehouse-plays-key-role-principals-teachers-students). A lot of the data in the Human Resources department, however, is not integrated into the Data Warehouse, which means that analysts who want to ask those questions -- for example, what the current workforce looks like, how many open positions there are currently, or retrospective teacher retention data -- need to tap into these systems separately.

During the summer, one of the most pressing questions is: who do we need to hire? This is not a trivial question, since many weeks and many conversations can happen between when 1) a principal identifies the need for a position and reports it to HR, and 2) a candidate is identified, hired and onboarded. 

Using Power BI, I built a report that combines data from [Applitrack](https://www.frontlineeducation.com/Home) and the internal onboarding system so that key stakeholders, from HR directors to school principals, could get a look at the current status of job openings across the district with the touch of a button. I spent a great deal of time building out the internal logic using Power BI's Query Editor so that future analysts only need to point the report to the appropriate raw data, and the report will refresh automatically. (I didn't have time to try to setup data streaming from the Applitrack website.)

I got permission to publish the report and source files (with randomized data). Take a look at it below -- left-click on charts to re-slice data and right-click to drill-down. It's an oddly satisfying experience. 

<iframe width="800" height="600" src="https://app.powerbi.com/view?r=eyJrIjoiZWVhMmIxMjUtOGM1Yi00MzQ4LWE4M2UtMzVlODA4N2NkNTVmIiwidCI6ImM2ODI4MjU3LTY0MTAtNDA3ZS1iNTU3LWI1ZGM3MjExZGU1NSIsImMiOjN9" frameborder="0" allowFullScreen="true"></iframe>  

In a later post, I'll detail how I obtained GIS coordinates for each of the schools -- it was a fun morning project that enabled some nice visualizations. 
