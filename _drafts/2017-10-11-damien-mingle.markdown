---
layout: post
title:  "Data Science Quotables w/ Damien Mingle"
categories: data-science penny-university
comments: true
---

date:   2017-10-11 12:00:00

The "Data Nerds" meetup got a chance to chat with Damien Mingle, Chief Data Scientist at Intermedix. He has had a long careerDamien's first decade in the field was based on Excel

Below are some of my favorite "sayings" from the meeting.

#### "Believe more in what you think you can do than what you can do." 
In short, be confident! Put your ideas out for others to chew on. Especially in team settings, where it's about getting results and not inflating egos -- I'm looking at you, academia -- putting out a "dumb" idea might spur a productive conversation that wouldn't otherwise have happened. When you hold your ideas back, the team and product suffers.

#### "Flip retrospective questions on their head." 
Most companies have analytics teams that can do a post-mortem on their data: "How many widgets did we sell in the last 60 days?" Far fewer people are comfortable with the prospective version: "How many widgets do we expect to sell in the next 60 days?" This is a cozy and fruitful space for data scientists to live in.

#### "Get creative with your features."
Intermedix has models for predicting [*sepsis*](http://www.mayoclinic.org/diseases-conditions/sepsis/symptoms-causes/dxc-20169787), a condition that is hard to predict and can lead to premature death. The natural first place to look for answers would be in a patient's Electronic Medical Record -- but this comes with a raft of access and security issues. Damien discussed how his team starts with 6 variables from basic claims data -- billing information -- then combines it with social, epidemiologic, demographic and other variables to create a 2200+ length feature vector for each patient. Their models have gotten up to an AUC of 0.93 or so -- all without tapping into EMR databases. 

What's in that feature vector? We didn't talk about all of them, but Damien did reveal one: the "distance from bathroom toilet to bathroom sink" in your house. Let's just say there could be a relationship between getting a life-threatening disease and whether toilet water splashes on your toothbrush.    

#### "Predictive models have instincts, too."
Many people have a lack of appreciation for the "from the gut" nature of what a predictive model does. Doctors understand that when a patient comes in and tells their story, they might have a strong hunch as to what the problem is, even though they don't have all the information yet. This is similar to what an ML model does, but people tend to think they are more rational, more "theoretical". Data scientists should be prepared to communicate that some features -- even hot new ideas -- might not be useful for the model, despite the fact that Time magazine just published an article about it.

#### "We can't all be Supergirl." 
Referencing the hit CW show all data scientists *must* watch, Damien concluded with reassuring advice: it's okay to not know everything. Even though the executives pushing for the new data science division want you to have laser vision, super strength, super speed, invulnerability and a tight leotard -- it is sometimes enough to be there, solving business problems and mining whatever value you can with the existing systems and your particular strengths.  

Thanks a lot, Damien, for the great chat -- and John for organizing, despite being on the verge of second-fatherhood. Another wonderful Data Nerds meetup!