---
layout: page
title: Lists
permalink: /lists/
---

Lists are sets of ideas that together make something better than individually. I have never had a great place to keep these logged -- until now. Refresh the page to generate a random list, or 

{{% assign random_list = site.lists | sample: 1 %}}

<ul class="post-page-list">
  <li>
    <span class="post-meta" style="padding: 0 0 0 0; margin: 0 0 0 0">{{ random_list.date | date: "%b %-d, %Y" }}</span>
    <h2 style="padding: 0 0 0 0; margin: 0 0 0 0"><a class="post-link" href="{{ random_list.url | prepend: site.baseurl }}" style="padding: 0 0;">{{ random_list.title }} from {{ random_list.source }}</a></h2>
    <span class="post-excerpt" style="padding: 0 0 0 0; margin: 0 0 0 0">{{ random_list.content | markdownify | strip_html }}</span>
  </li>
</ul>
<p class="rss-subscribe">subscribe <a href="{{ "/feed.xml" | prepend: site.baseurl }}">via RSS</a></p>