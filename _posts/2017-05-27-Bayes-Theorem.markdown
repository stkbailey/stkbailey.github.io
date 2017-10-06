---
layout: post
title:  "Penny U: A Brief Overview of Bayes"
date:   2017-05-27 12:00:00
categories: statistics data-science pennyu
---

Yesterday, several of us met with John Berryman and Chris Fonnesbeck to discuss the basics of Bayesian analysis. We mostly discussed Bayes theorem and its differences from frequentist statistics. Some highlights were:

**The theorem**: Bayes theorem allows you to directly estimate the probability of a hypothesis being true, given a certain set of data.  
**Formula**: Here's a link to Bayes formula, which John "derived" for us: [Bayes Theorem on Brilliant.com](https://brilliant.org/wiki/bayes-theorem)  
**Example**: At the bottom of this email, I share an example that we worked through (basically). It deals with computing the probability of having a certain disease (D+), given a positive test result (T+), based on a sample of 1000 people (S). 
**The benefits**   
One of the nice benefits of Bayesian analysis is that it can answer questions in a more natural way than frequentist statistics can, in some cases. In our example, we can derive (and interpret) the probability that a person who tests positive will also have the disease. From a frequentist perspective, we could only discuss this probability in a more general, distribution-oriented way, e.g. by saying that the chances are about 0.005 that a person has both the disease and tests positive. (Disclaimer: Not sure I'm actually getting this explanation correct here.). 
Also, Bayesian analysis can sometimes provide computational advantages; i.e. some models are more easily estimable using Bayes than other methods.

Other resources noted were: 
- Gelman's Bayesian analysis book: https://www.amazon.com/Bayesian-Analysis-Chapman-Statistical-Science/dp/1439840954 
- Martin's book (I think): https://www.amazon.com/Bayesian-Analysis-Python-Osvaldo-Martin/dp/1785883801/ref=sr_1_4?s=books&ie=UTF8&qid=1493302986&sr=1-4&keywords=bayesian+analysis 
  
{% highlight ruby %}
# Computing the probability of having a certain disease (D+), given a positive test result (T+), based on a sample of 1000 people (S)
# In this data, the test is very sensitive but not specific

# required probabilities
N(D+) = 5
N(T+) = 20
N(D+,T+) = 5 
N(S) = 1000

# required probabilities
P(D+) = N(D+)/N(S) = 5/1000 = .005
P(T+) = N(T+)/N(S) = 20/1000 = .02
P(T+|D+) = N(D+,T+)/N(D+) = 5/5 = 1.0

# applying bayes theorem
P(D+|T+) = P(T+|D+)*P(T+)/P(D+) = 1.0*0.005/0.02 = 0.25
# So, given a positive test result, there is still only a 0.25 chance of being disease-positive

#double check by calculating it directly
P(D+|T+) = N(D+,T+)/N(T+) = 5/20 = 0.25
{% endhighlight %}

Big thanks to Chris, John and everyone else for an awesome lunch!