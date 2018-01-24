---
layout: post
title:  "Accessing XNAT through Python"
date:   2017-12-31 12:00:00
categories: vanderbilt
comments: true
---

If your MR data is stored in XNAT, chances are you'll want to access and edit it. One way you can do this is using XNAT's REST API. If you're a Python user, though, you can also use some useful tools in the [DAX (Distributed Automated tools for XNAT)](https://github.com/VUIIS/dax) and [PyXNAT](https://github.com/pyxnat/pyxnat) packages.

In this tutorial, we're going to cover some basics of summarizing and editing metadata on XNAT. We will cover:

1. Connecting to XNAT
2. Downloading subject/session/scan data
3. Updating object attributes

### 1. Connecting to XNAT

PyXNAT establishes a connection to your XNAT server and stores it in an XNAT interface object, which you can work with to sub-select data. DAX has wrappers for PyXNAT which provide very easy ways to access your data.  

{% highlight python %}
from dax import XnatUtils

xnat = XnatUtils.get_interface(host='https://xnat.vanderbilt.edu/xnat/', user='bailesk1', pwd=your_xnat_password)
{% endhighlight %}

By default, the `get_interface` function will look for the user's `dax_settings.ini` file and populate with the discovered user name, password and XNAT URL. You can setup this file running `dax_setup` from the command line (see [my previous post]( assets/... | {{ site | absolute_url }})). 

### 2. Downloading subject/session/scan data

Using the REST server or `pyxnat` to query the database directly can be difficult for newbies like myself. Fortunately, DAX has several methods that can return the data with the most common fields populated.

{% highlight python %}
subjects = XnatUtils.list_subjects(xnat, projectid='CUTTING')
sessions = XnatUtils.list_sessions(xnat, projectid='CUTTING')
scans = XnatUtils.list_project_scans(xnat, projectid='CUTTING')
{% endhighlight %}

`list_subjects()`, `list_sessions()`, etc. return a list of dictionaries. If you are intereste in writing this to a CSV or Excel file, one of the easiest ways is to coerce it into a Pandas dataframe, then write it to the disk (or further manipulate it). 

{% highlight python %}
import pandas as pd
df_scans = pd.DataFrame(scans)
df_scans.to_csv('/path/to/myfile/scans.csv', index=None)
{% endhighlight %}

### 3. Updating object attributes

To edit data, we have to select the object using the `interface.select` method. There are a couple ways to do it, but let's use the most "Pythonic" one:

{% highlight python %}
scan = xnat.select.project('CUTTING').subject('LM1207_vG').experiment('207123').scan('101')
fields_to_get = ['xnat:imageScanData/type', 'xnat:imageScanData/description']
scan.attrs.get(fields_to_get[0])	# one field
scan.attrs.mget(fields_to_get)		# multiple fields
{% endhighlight %}

You can find the whole list of attributes [online here](https://wiki.xnat.org/docs16/4-developer-documentation/using-the-xnat-rest-api/xnat-rest-xml-path-shortcuts). To set attributes, simply change `get` to `set` and add a new value:

{% highlight python %}
scan.attrs.set('xnat:imageScanData/type', 't1_improved3d')
{% endhighlight %}

Combining these methods with `for` loops and filtering allows you to easily change many fields across your database:

{% highlight python %}
for ii, scandata in df_scans.loc[df_scans.scan_label == '101'].iterrows():
	scan = xnat.select.project('CUTTING')
				.subject(scandata.subject_label)
				.experiment(scandata.session_label)
				.scan(scandata.scan_label)
	scan.attrs.set('xnat:imageScanData/type', 'first_scan')
{% endhighlight %}

