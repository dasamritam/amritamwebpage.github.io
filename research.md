---
layout: archive
title: "Research"
permalink: /research/
author_profile: true
---


My research is about *developing control theory on the basis of physics-driven as well as data-intensive methods that guarentee safe, efficient and cost-effective operations of complex multi-physical systems.* 
{: style="text-align: justify;"}

* In multi-physical systems, more than one phase of matter interact with each other and simultaneously obey physical laws from different disciplines of physics and chemistry. Many physical quantities may vary over time as well as space.
{: style="text-align: justify;"}
* Controlling such a system is *very hard* without making some prior approximations. However, approximation deteriorates model quality, hence, the performance of a model-based controller. A key focus of my research is to rectify this issue. 
{: style="text-align: justify;"}
* Compared to typical engineering systems, *brain-inspired* devices, such as neuromorphic chips, are quite different. Instead of 1s and 0s, they communicate via spikes. Conventional control theory is unsuitable for such a device since generating spikes requires two feedback-control loops of opposite signs. My research provides methods and tools to design such control systems for modulating spikes over space and time.
{: style="text-align: justify;"}

<nbsp>

{% include base_path %}

{% assign ordered_pages = site.research | sort:"order_number" %}

{% for post in ordered_pages %}
  {% include archive-single.html type="grid" %}
{% endfor %}