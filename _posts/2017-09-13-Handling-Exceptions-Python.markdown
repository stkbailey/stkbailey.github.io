---
layout: post
title:  "Handling Exceptions in Python w/ John Still"
date:   2017-09-13 12:00:40
categories: python penny-university
comments: true
---

A  few weeks ago, I had an extremely helpful conversation with John Still about exception handling in Python, and how to build useful tests for your functions. I was a beginner in this area, and we covered a lot of ground, so I'm going to bullet point some of my major take-aways.

The `try` function can be followed by three statements: `except`, `else` and `finally`. `Except` is used to put in code that handles certain errors in a particular way; `else` is used to execute code when no errors occured, and which does not need to be protected by the try block; `finally` is used for cleaning up files / workspace regardless of whether an error was thrown.

I always thought of the `try...except` clause as a way to hide my errors and get my code to run no matter what. John said this is a bad idea :-) That's because if you simply bypass all the errors, no useful error messages "filter up" and tell you what specifically is wrong

To that end, John recommended that I try to explicitly name my anticipated exceptions and handle them individually. So, instead of typing:

{% highlight ruby %}
for x in set_of_values:
  try:
     my_function(x)
  except:
     pass
{% endhighlight %}

I would write:

{% highlight ruby %}
for x in set_of_values:
   try:
      my_function(x)
   except ValueError as exc:
      raise ValueError('{} is not an integer'.format(x) from exc
   except SomeOtherErrror as exc:
       raise SomeThirdErrror('{} the function doesn't work.'.format(x)) from exc
{% endhighlight %}

In our discussion of unit testing, I learned that the `assert` statement is at the heart of testing, and there are several libraries (pytest, e.g.) out there that can help run and monitor testing. Furthermore, we discussed how testing is an important, not secondary, part of your code if it's going to be used by anyone else, and you should think creatively about how to write good tests.

Finally, John gave me a couple of really great resources that helped me understand Python's data structure a little more generally.
- Video: Ned Batchelder - [Getting Started Testing](https://www.youtube.com/watch?v=FxSsnHeWQBY)
- Video: Ned Batchelder - [Facts & Myths about Python](https://www.youtube.com/watch?v=_AEJHKGk9ns)
- Book: [Fluent Python](http://1.droppdf.com/files/X06AR/fluent-python-2015-.pdf) by Luciano Ramalho

Thanks, John, for the great chat!