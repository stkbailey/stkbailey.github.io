---
layout: page
title: Posts
permalink: /posts/
---

<ul class="post-page-list">
{% for post in posts %}
  <li>
    <span class="post-page-meta">{{ post.date | date: "%b %-d, %Y"  }} • </span><a class="post-page-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
  </li>
{% endfor %}
</ul>

<ul>
{% for category in site.categories %}
  <li><a name="{{ category | first }}">{{ category | first }} ({{ category | last | size }} posts)</a>
    <ul class="post-page-list">
    {% for posts in category %}
      {% for post in posts %}
 	  <li>
	    <span class="post-page-meta">{{ post.date | date: "%b %-d, %Y"  }} • </span><a class="post-page-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
	  </li>
      {% endfor %}
    {% endfor %}
    </ul>
  </li> 
{% endfor %}
</ul>
<p class="rss-subscribe">subscribe <a href="{{ "/feed.xml" | prepend: site.baseurl }}">via RSS</a></p>