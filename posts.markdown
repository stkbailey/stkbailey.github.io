---
layout: page
title: Posts
permalink: /posts/
---

{% for category in site.categories %}
  <span class="post-page-header">{{ category | first }}</span>
  <ul class="post-page-list">
  {% for posts in category %}
    {% for post in posts %}
      {% if post.url %}
      <li>
        <span class="post-page-meta">{{ post.date | date: "%b %-d, %Y"  }} • </span><a class="post-page-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
      </li>
      {% endif %}
    {% endfor %}
  {% endfor %}
  </ul>
{% endfor %}
<p class="rss-subscribe">subscribe <a href="{{ "/feed.xml" | prepend: site.baseurl }}">via RSS</a></p>