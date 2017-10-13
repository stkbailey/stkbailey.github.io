---
layout: post
title:  "Data Science Perspective w/ Damian Mingle"
date:   2017-10-12 10:05:00
categories: data-science penny-university
comments: true
---

Several of us in the "Data Nerds" meetup recently chatted with [Damian Mingle](https://www.linkedin.com/in/damianrmingle/), Chief Data Scientist at [Intermedix](https://www.intermedix.com/). He told us the story of his career -- how he went from building predictive real estate algorithms to being a scrappy, Excel-using Kaggle competitor to leading a 16+ person data science team at Intermedix that improves health outcomes for hunderds of thousands of patients. 

We drank knowledge from a fire hose for an hour, but I've jotted down a few of my favorite bits of advice from the discussion. Enjoy!

#### "Think creatively - but also carefully - about your features."
Intermedix has models that assess the probability for a patient to get [*sepsis*](http://www.mayoclinic.org/diseases-conditions/sepsis/symptoms-causes/dxc-20169787), a condition that is hard to predict and can lead to premature death. Damien discussed how his team starts with 6 variables from basic claims data -- billing information -- then combines it with social, epidemiologic, demographic and other variables to create a 2200+ length feature vector for each patient. Their models have gotten up to an AUC of 0.93 or so -- far better than the "business-as-usual" performance.

With 2200 variables, it might seem that the team is throwing in the "kitchen sink". But actually, the model does not use any information from a patient's Electronic Medical Record despite having access to it. The idea is that, if pulling out the "kitchen sink" requires getting permission from the homeowner, the county, the federal government and the construction of new storage facilities, security protocols, etc., etc. -- the extra bit of accuracy it provides might not be worth it. So deciding what NOT to include can be as important as what to include. 

What's in that feature vector? We didn't talk about all of them, but Damien did reveal one: the "distance from bathroom toilet to bathroom sink" in your house. Let's just say there could be a relationship between getting a life-threatening disease and whether toilet water splashes on your toothbrush...

#### "Flip retrospective questions on their head." 
Most companies have analytics teams that can do a post-mortem on their data: "How many widgets did we sell in the last 60 days?" Far fewer people are comfortable with the prospective version: "How many widgets do we expect to sell in the next 60 days?" This is a cozy and fruitful space for data scientists to live in.


#### "Predictive models have instincts, too."
Many people have a lack of appreciation for the "from the gut" nature of what a predictive model does. People understand that a doctor might have a "hunch" as to what a patient's problem is with only a glance and a small bit of information. When it comes to ML, though, people tend to think there is always a clear, precise reason for a given decision -- although it might be better described as a quantitative instinct. 

Similarly, data scientists should be prepared to communicate to stakeholders that some features -- even hot new ideas -- might not be useful for the model, despite the fact that Time magazine just published an article about it.

#### "Believe more in what you think you can do than what you can do." 
In short, be confident in yourself! Analytical folks are often hesitant to be wrong in front of peers. Especially in team settings, where it's about getting results and not inflating egos -- I'm looking at you, academia -- putting out a "dumb" idea might spur a productive conversation that wouldn't otherwise have happened. When you hold your ideas back, the team and product suffers. 

#### "We can't all be Supergirl." 
Referencing the hit CW show all data scientists *must* watch, Damien concluded with reassuring advice: it's okay to not know everything. Even though the executives pushing for the new data science division want you to have laser vision, super strength, super speed, invulnerability and a tight leotard -- it is sometimes enough to be there, solving business problems and mining whatever value you can with the existing systems and your particular strengths.  

---

Thanks a lot, Damien, for the great chat -- and John for organizing, despite being on the verge of second-fatherhood. Another wonderful Data Nerds meetup!