---
layout: post
title:  "Accessing REDCap Data from Python"
date:   2017-12-08 16:00:00
categories: vanderbilt
comments: true
---

In this tutorial, I'm going to walk you through getting data from REDCap via the API. We'll walk through it from the bottom to the top, so even if you've never opened up Python before, we've got you covered.

## Setting Up Python

### 1. Download Anaconda

Anaconda is a self-contained Python manager. 

Python can be very tricky to work with, because your computer uses Python for a lot of processes "behind-the-scenes". Since we don't want to mess with or overwrite these files, we want to download Anaconda, a Python "distribution". You can treat it just like you would any other program: you go to the website, download it and install it. Do it now: https://www.anaconda.com/download/

We are going to create our own, self-contained Python playground - otherwise known as an "environment". It will be a totally fresh Python start, and we'll get to download only the packages we want to use. 


### 2. Create a new Python environment in Anaconda.

Start the **Anaconda Prompt** by finding it in the "Start" screen on Windows or using Spotlight on your Mac. Once there, we're going to tell Anaconda to create our first environment. We'll call it *redcap*.

{% highlight python %}
conda create -n redcap python=3.6
{% endhighlight %}
`conda` is how we access Anaconda's functionality for managing Python environments. Here we are asking `conda` to `create` a new environment named `redcap`, and to install Python 3.6 in it.

It will ask for permission to download the first packages from online. When it's done, go to the next step.


### 3. Activate your new environment and download "redcap" and pandas

Once install is complete, we need to add some custom packages to your environment. Start by turning your environment with `source activate redcap` (just `activate redcap` on Windows). Once in, type these two commands: 

{% highlight python %}
conda install pandas jupyter
pip install pycap 
{% endhighlight %}

Here we are asking Anaconda to install `pandas` and `jupyter`, two important libraries for data science / processing. We then ask `pip` to install `pycap`, the library made by Scott Burns for accessing Redcap remotely. 

*Side note: The differences between `conda install` and `pip install` are not important for us here. In general, try to install new packages by using `conda install` first, and if it is not found, try `pip install`.*


### 4. Launch a Jupyter Notebook server and create a new notebook

Once finished, we want to launch a Jupyter Notebook so that we can interactively work with our data. I recommend passing in the `--notebook-dir` flag so that you know exactly which folder you'll be operating in. 

{% highlight python %}
jupyter notebook --notebook-dir="C:\\Users\\Stephen\\Desktop"
{% endhighlight %}

You'll see a "home" screen that shows the files in your directory. In the top-right, click on the "New" button, and under *Notebooks*, select Python 3. This will start a new Jupyter notebook.

Notebooks are a way to both 1) run Python, 2) revise and record your work. A few commands you need to know are: 

- Enter: "Enters" current cell
- Esc: "Exits" current cell
- CTRL + Enter: Runs the current cell
- CTRL + a: Creates a new cell above current one
- CTRL + b: Creates a new cell below current one

Cells are marked as "code" by default. You can change this by clicking on a cell, then going to the drop-down box at the top that says "code" and change it to "Markdown" or another option. 



## Accessing REDCap
### 1. Load *pycap* and connect to the database

We will work with *PyCap* in this way:

1. Connect to a given Redcap project
2. Download attributes into a *Project* object.
3. Export records, fields or files into a pandas DataFrame
4. Save DataFrame into a csv for further manipulation

It's actually very simple. You only need the "API Token" from your Redcap project. This is unique to you and **SHOULD BE HANDLED EXTREMELY CAREFULLY**. Your API token grants access to all of the project data that you have access to, including PII, if it is available to you. It should be treated just like your password and stored in a safe manner.

First, we import the `redcap` package.


{% highlight python %}
import redcap
{% endhighlight %}

Next, we create a `Project` object by passing the Redcap URL and token into the `redcap.Project` function. 


{% highlight python %}
proj = redcap.Project('https://redcap.vanderbilt.edu/api/', your_rc_api_tkn)
{% endhighlight %}

`proj` is a Python object that has its own properties and functions attached to it. We can access these by typing `proj.` and then pressing `tab`. You will see a list of possible actions to take on this object.


{% highlight python %}
proj
{% endhighlight %}

    <redcap.project.Project at 0x22d1f233ac8>




{% highlight python %}
proj.forms[0:10]
{% endhighlight %}


    ('prepost_scanner_task_questions',
     'genetics',
     'gates_macginite',
     'eprime',
     'wmtb',
     'behavioral_data_screening',
     'completion_data',
     'contact_info',
     'test_of_morph_structure',
     'scale_for_early_mathematics_anxiety_sema')




{% highlight python %}
proj.field_names[0:10]
{% endhighlight %}


    ['rc3_participant_id',
     'rc3_doa_45c',
     'rc3_first_name',
     'rc3_last_name',
     'rc3_dob',
     'rc3_parentname_first',
     'rc3_parentname_last',
     'rc3_telephone_1',
     'rc3_telephone_2',
     'rc3_email']


{% highlight python %}
proj.field_labels[0:10]
{% endhighlight %}


    ['Participant ID',
     'Date of Acquisition',
     'First Name',
     'Last Name',
     'Date of birth',
     'Parent First Name',
     'Parent Last Name',
     'Phone number',
     'Second phone number',
     'E-mail']



### 2. Export some or all of the records in your project

Now, we want to pull data from the project. Think of `proj` as a blueprint of the underlying data: it isn't until we `export_records()` that we have a table of data. 

We can select either all of the records (which is the default) or only some of the records by specifying different flags in the `export_records` function. Let's just export the "Woodcock Johnson" form first.


{% highlight python %}
df_wj = proj.export_records(forms=['wjiv'], format='df')
{% endhighlight %}


{% highlight python %}
print('There are {} rows and {} columns.'.format(\*df_wj.shape))
{% endhighlight %}

    There are 478 rows and 69 columns.
    


{% highlight python %}
df_wj.columns
{% endhighlight %}




    Index(['rc3_wj_visit', 'rc3_wj_lwid_raw_age', 'rc3_wj_lwid_w_age',
           'rc3_wj_lwid_ss_age', 'rc3_wj_lwid_pile_age', 'rc3_wj_wa_raw_age',
           'rc3_wj_wa_w_age', 'rc3_wj_wa_ss_age', 'rc3_wj_wa_pile_age',
           'rc3_wj_pc_raw_age', 'rc3_wj_pc_w_age', 'rc3_wj_pc_ss_age',
           'rc3_wj_pc_pile_age', 'rc3_wj_calc_raw_age', 'rc3_wj_calc_w_age',
           'rc3_wj_calc_ss_age', 'rc3_wj_calc_pile_age', 'rc3_wj_appprob_raw_age',
           'rc3_wj_appprob_w_age', 'rc3_wj_appprob_ss_age',
           'rc3_wj_appprob_pile_age', 'rc3_wj_oc_raw_age', 'rc3_wj_oc_w_age',
           'rc3_wj_oc_ss_age', 'rc3_wj_oc_pile_age', 'rc3_wj_re_w_age',
           'rc3_wj_re_ss_age', 'rc3_wj_re_pile_age', 'rc3_wj_br_w_age',
           'rc3_wj_br_ss_age', 'rc3_wj_br_pile_age', 'rc3_wj_bm_w_age',
           'rc3_wj_bm_ss_age', 'rc3_wj_bm_pile_age', 'rc3_wj_lwid_raw_grade',
           'rc3_wj_lwid_w_grade', 'rc3_wj_lwid_ss_grade', 'rc3_wj_lwid_pile_grade',
           'rc3_wj_wa_raw_grade', 'rc3_wj_wa_w_grade', 'rc3_wj_wa_ss_grade',
           'rc3_wj_wa_pile_grade', 'rc3_wj_pc_raw_grade', 'rc3_wj_pc_w_grade',
           'rc3_wj_pc_ss_grade', 'rc3_wj_pc_pile_grade', 'rc3_wj_calc_raw_grade',
           'rc3_wj_calc_w_grade', 'rc3_wj_calc_ss_grade', 'rc3_wj_calc_pile_grade',
           'rc3_wj_appprob_raw_grade', 'rc3_wj_appprob_w_grade',
           'rc3_wj_appprob_ss_grade', 'rc3_wj_appprob_pile_grade',
           'rc3_wj_oc_raw_grade', 'rc3_wj_oc_w_grade', 'rc3_wj_oc_ss_grade',
           'rc3_wj_oc_pile_grade', 'rc3_wj_re_w_grade', 'rc3_wj_re_ss_grade',
           'rc3_wj_re_pile_grade', 'rc3_wj_br_w_grade', 'rc3_wj_br_ss_grade',
           'rc3_wj_br_pile_grade', 'rc3_wj_bm_w_grade', 'rc3_wj_bm_ss_grade',
           'rc3_wj_bm_pile_grade', 'rc3_wj_comment', 'wjiv_complete'],
          dtype='object')



This time, let's pull out just a single subject's data.


{% highlight python %}
df_singlesubj = proj.export_records(records=['RC3001'], format='df')
{% endhighlight %}


{% highlight python %}
print('There are {} rows and {} columns.'.format(\*df_singlesubj.shape))
{% endhighlight %}


    There are 3 rows and 1477 columns.
    

That's a lot of columns! We are unlikely to ever want to access all of this data. We'll talk about filtering in a minute. For now, let's go ahead and download all of the data -- we'll tell `export_records` that we want no special filtering for forms, fields, events, etc. (Or we could just not type them out at all.)


{% highlight python %}
df_all = proj.export_records(records=None, fields=None, events=None,  format='df')
{% endhighlight %}


{% highlight python %}
print('There are {} rows and {} columns.'.format(\*df_all.shape))
{% endhighlight %}

    There are 478 rows and 1477 columns.
    

### 3. Trim the data 

Knowledge of Python **lists** and **list comprehensions** can be extremely useful for curating datasets. 

In a pinch, you can simply write out the names of the columns or subjects you want, like this: `keep_these_columns = ['rc3_wmtb_list_ss', 'rc3_parent_wj_br_ss', 'rc3_dkefs_sort_cc_ss']`. 


{% highlight python %}
cols_to_keep = [c for c in df_all if 'ctopp' in c]
print(cols_to_keep)
{% endhighlight %}

    ['rc3_ctopp_el_raw', 'rc3_ctopp_el_ss', 'rc3_ctopp_bw_raw', 'rc3_ctopp_bw_ss', 'rc3_ctopp_md_raw', 'rc3_ctopp_md_ss', 'rc3_ctopp_rdn_raw', 'rc3_ctopp_rdn_ss', 'rc3_ctopp_rln_raw', 'rc3_ctopp_rln_ss', 'rc3_ctopp_ran_com', 'rc3_ctopp_ran_pile', 'rc3_ctopp_comment']
    


{% highlight python %}
subjs_to_keep = [(subj, visit) for subj, visit in df_all.index if 'visit_1' in visit]
print(subjs_to_keep[0:5])
{% endhighlight %}

    [('RC3001', 'visit_1_arm_1'), ('RC3002', 'visit_1_arm_1'), ('RC3003', 'visit_1_arm_1'), ('RC3004', 'visit_1_arm_1'), ('RC3005', 'visit_1_arm_1')]
    


{% highlight python %}
df_trimmed = df_all.loc[subjs_to_keep, cols_to_keep]
df_trimmed.head(20)
{% endhighlight %}




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>rc3_ctopp_el_raw</th>
      <th>rc3_ctopp_el_ss</th>
      <th>rc3_ctopp_bw_raw</th>
      <th>rc3_ctopp_bw_ss</th>
      <th>rc3_ctopp_md_raw</th>
      <th>rc3_ctopp_md_ss</th>
      <th>rc3_ctopp_rdn_raw</th>
      <th>rc3_ctopp_rdn_ss</th>
      <th>rc3_ctopp_rln_raw</th>
      <th>rc3_ctopp_rln_ss</th>
      <th>rc3_ctopp_ran_com</th>
      <th>rc3_ctopp_ran_pile</th>
      <th>rc3_ctopp_comment</th>
    </tr>
    <tr>
      <th>rc3_participant_id</th>
      <th>redcap_event_name</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>RC3001</th>
      <th>visit_1_arm_1</th>
      <td>23.0</td>
      <td>12.0</td>
      <td>27.0</td>
      <td>16.0</td>
      <td>16.0</td>
      <td>11.0</td>
      <td>20.0</td>
      <td>12.0</td>
      <td>26.0</td>
      <td>11.0</td>
      <td>110.0</td>
      <td>75.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3002</th>
      <th>visit_1_arm_1</th>
      <td>29.0</td>
      <td>14.0</td>
      <td>26.0</td>
      <td>14.0</td>
      <td>20.0</td>
      <td>14.0</td>
      <td>19.0</td>
      <td>11.0</td>
      <td>18.0</td>
      <td>12.0</td>
      <td>110.0</td>
      <td>75.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3003</th>
      <th>visit_1_arm_1</th>
      <td>24.0</td>
      <td>12.0</td>
      <td>24.0</td>
      <td>12.0</td>
      <td>17.0</td>
      <td>11.0</td>
      <td>25.0</td>
      <td>9.0</td>
      <td>30.0</td>
      <td>9.0</td>
      <td>95.0</td>
      <td>37.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3004</th>
      <th>visit_1_arm_1</th>
      <td>29.0</td>
      <td>14.0</td>
      <td>25.0</td>
      <td>13.0</td>
      <td>18.0</td>
      <td>12.0</td>
      <td>18.0</td>
      <td>12.0</td>
      <td>22.0</td>
      <td>10.0</td>
      <td>107.0</td>
      <td>68.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3005</th>
      <th>visit_1_arm_1</th>
      <td>25.0</td>
      <td>12.0</td>
      <td>21.0</td>
      <td>10.0</td>
      <td>15.0</td>
      <td>9.0</td>
      <td>15.0</td>
      <td>14.0</td>
      <td>16.0</td>
      <td>12.0</td>
      <td>119.0</td>
      <td>90.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3006</th>
      <th>visit_1_arm_1</th>
      <td>15.0</td>
      <td>8.0</td>
      <td>22.0</td>
      <td>10.0</td>
      <td>16.0</td>
      <td>10.0</td>
      <td>30.0</td>
      <td>8.0</td>
      <td>28.0</td>
      <td>9.0</td>
      <td>92.0</td>
      <td>30.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3007</th>
      <th>visit_1_arm_1</th>
      <td>30.0</td>
      <td>15.0</td>
      <td>20.0</td>
      <td>9.0</td>
      <td>17.0</td>
      <td>11.0</td>
      <td>25.0</td>
      <td>9.0</td>
      <td>32.0</td>
      <td>9.0</td>
      <td>95.0</td>
      <td>37.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3008</th>
      <th>visit_1_arm_1</th>
      <td>16.0</td>
      <td>9.0</td>
      <td>26.0</td>
      <td>14.0</td>
      <td>18.0</td>
      <td>12.0</td>
      <td>20.0</td>
      <td>11.0</td>
      <td>29.0</td>
      <td>9.0</td>
      <td>101.0</td>
      <td>53.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3009</th>
      <th>visit_1_arm_1</th>
      <td>25.0</td>
      <td>11.0</td>
      <td>24.0</td>
      <td>11.0</td>
      <td>16.0</td>
      <td>10.0</td>
      <td>20.0</td>
      <td>10.0</td>
      <td>21.0</td>
      <td>10.0</td>
      <td>101.0</td>
      <td>53.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3010</th>
      <th>visit_1_arm_1</th>
      <td>17.0</td>
      <td>9.0</td>
      <td>25.0</td>
      <td>13.0</td>
      <td>17.0</td>
      <td>11.0</td>
      <td>19.0</td>
      <td>11.0</td>
      <td>29.0</td>
      <td>9.0</td>
      <td>101.0</td>
      <td>53.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3011</th>
      <th>visit_1_arm_1</th>
      <td>13.0</td>
      <td>8.0</td>
      <td>24.0</td>
      <td>12.0</td>
      <td>13.0</td>
      <td>7.0</td>
      <td>19.0</td>
      <td>11.0</td>
      <td>21.0</td>
      <td>11.0</td>
      <td>107.0</td>
      <td>68.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3012</th>
      <th>visit_1_arm_1</th>
      <td>27.0</td>
      <td>13.0</td>
      <td>23.0</td>
      <td>11.0</td>
      <td>16.0</td>
      <td>10.0</td>
      <td>39.0</td>
      <td>7.0</td>
      <td>35.0</td>
      <td>8.0</td>
      <td>85.0</td>
      <td>16.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3013</th>
      <th>visit_1_arm_1</th>
      <td>23.0</td>
      <td>11.0</td>
      <td>17.0</td>
      <td>8.0</td>
      <td>15.0</td>
      <td>9.0</td>
      <td>21.0</td>
      <td>11.0</td>
      <td>30.0</td>
      <td>9.0</td>
      <td>101.0</td>
      <td>53.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3014</th>
      <th>visit_1_arm_1</th>
      <td>18.0</td>
      <td>9.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>17.0</td>
      <td>11.0</td>
      <td>25.0</td>
      <td>9.0</td>
      <td>35.0</td>
      <td>8.0</td>
      <td>92.0</td>
      <td>30.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3015</th>
      <th>visit_1_arm_1</th>
      <td>16.0</td>
      <td>10.0</td>
      <td>23.0</td>
      <td>12.0</td>
      <td>15.0</td>
      <td>10.0</td>
      <td>24.0</td>
      <td>10.0</td>
      <td>31.0</td>
      <td>10.0</td>
      <td>101.0</td>
      <td>53.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3016</th>
      <th>visit_1_arm_1</th>
      <td>22.0</td>
      <td>10.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>9.0</td>
      <td>24.0</td>
      <td>8.0</td>
      <td>20.0</td>
      <td>10.0</td>
      <td>95.0</td>
      <td>37.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3017</th>
      <th>visit_1_arm_1</th>
      <td>29.0</td>
      <td>13.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>21.0</td>
      <td>15.0</td>
      <td>23.0</td>
      <td>9.0</td>
      <td>17.0</td>
      <td>12.0</td>
      <td>104.0</td>
      <td>61.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3018</th>
      <th>visit_1_arm_1</th>
      <td>14.0</td>
      <td>6.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>8.0</td>
      <td>26.0</td>
      <td>7.0</td>
      <td>24.0</td>
      <td>8.0</td>
      <td>85.0</td>
      <td>16.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3019</th>
      <th>visit_1_arm_1</th>
      <td>31.0</td>
      <td>14.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>16.0</td>
      <td>10.0</td>
      <td>15.0</td>
      <td>13.0</td>
      <td>15.0</td>
      <td>13.0</td>
      <td>119.0</td>
      <td>90.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>RC3020</th>
      <th>visit_1_arm_1</th>
      <td>14.0</td>
      <td>7.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>17.0</td>
      <td>11.0</td>
      <td>19.0</td>
      <td>10.0</td>
      <td>19.0</td>
      <td>11.0</td>
      <td>104.0</td>
      <td>61.0</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



### 4. Save to a "csv" file

Saved the easiest part for last: write the table to a "comma-separated values" file using `df.to_csv(filename)`. Go ahead and pass in `encoding='utf-8'` so that when you open your data on a Windows or Mac, it all looks the same.


{% highlight python %}
df_trimmed.to_csv('trimmed_rc3_data.csv', encoding='utf-8')
{% endhighlight %}