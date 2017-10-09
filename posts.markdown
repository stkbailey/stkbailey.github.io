---
layout: page
title: Posts
permalink: /posts/
---

<ul class="post-page-list">
{% for post in site.posts %}
  <li>
    <span class="post-page-meta">{{ post.date | date: "%b %-d, %Y"  }} • </span><a class="post-page-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
  </li>
{% endfor %}
</ul>

<p class="rss-subscribe">subscribe <a href="{{ "/feed.xml" | prepend: site.baseurl }}">via RSS</a></p>