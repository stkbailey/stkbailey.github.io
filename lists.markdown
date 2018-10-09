---
layout: page
title: Lists
permalink: /lists/
---

Lists are sets of ideas that together make something better than individually. I have never had a great place to keep these logged -- until now. 

<h3 class="post-title">Latest List</h3>

<ul class="post-list">
{% for post in site.lists limit: 1 %}
  <li>
    <div style="padding: 0 0 0 0; margin: 0 0 0 0">
      <span class="post-meta" style="padding: 0 0 0 0; margin: 0 0 0 0">{{ post.date | date: "%b %-d, %Y" }}</span>
      <h2 style="padding: 0 0 0 0; margin: 0 0 0 0"><a class="post-link" href="{{ post.url | prepend: site.baseurl }}" style="padding: 0 0;">{{ post.title }} from {{ post.source }}</a></h2>
      <span class="post-excerpt" style="padding: 0 0 0 0; margin: 0 0 0 0">{{ post.content | markdownify | strip_html }}</span>
    </div>
  </li>
{% endfor %}
</ul>


<h3 class="post-title">List of Lists</h3>

<ul class="post-page-list">
{% for post in site.lists %}
  {% if post.url %}
  <li>
    <span class="post-page-meta"> • </span><a class="post-page-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
  </li>
  {% endif %}
{% endfor %}
</ul>

<p class="rss-subscribe">subscribe <a href="{{ "/feed.xml" | prepend: site.baseurl }}">via RSS</a></p>