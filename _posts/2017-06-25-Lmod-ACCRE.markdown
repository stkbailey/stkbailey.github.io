---
layout: post
title:  "A Quick-Start to Lmod"
date:   2017-06-25 12:00:00
categories: vanderbilt
comments: true
---

I took some time to watch the [ACCRE team’s Pizza & Programming presentation](https://www.youtube.com/watch?v=La92_3hcw-k&index=4&list=PL8Q6Imidwz82Lk37fjv0ImSqsOjTwuKsZ) on the rollout of Lmod package manager, and wanted to provide a high-level summary and cookbook for what typical neuroimaging users will need to know.

Reason for the switch: Lmod offers a better way for the ACCRE team to build and manage packages than setpkgs which is 17 years old. Blah, blah, blah, it doesn’t really matter to us, except it should prevent some annoying errors that we’re not likely to have encountered.

Key commands: Access Lmod functions by typing ‘module’ followed by a command. Here are the key commands:

-	`module` – list lmod functions
-	`module avail` – list “core” modules / packages
-	`module spider` – list all modules / packages
-	`module load <module_name1> <module_name2> …` -- loads module(s) into your environment
-	`module save <name>` -- saves the current set of modules as a group which can be loaded later
-	`module restore <name>` -- reloads set of modules

What you should do: basically, you just need to…
1.	Make a list of the packages you load with `setpkgs` in your bashrc
2.	In one line, create an lmod statement that loads your desired modules.
a.	You might also need to load some things like “GCC” to get all modules to load
3.	Save your current environment with a name
4.	Put a `module restore` statement in your bashrc and comment out your “setpkgs” statements

Example: I loaded a set of modules with this command and saved it as a set:
{% highlight ruby %}
module load  GCC/5.4.0-2.26 Anaconda3/4.3.1 FreeSurfer/5.3.0-centos6_x86_64  MATLAB/2017a  ImageMagick/7.0.3-1  git/2.12.2
module save default

# Then, I put the following in my bashrc and got rid of about 7 setpkgs commands.
echo "module restore default" >> ~/.bashrc
{% endhighlight %}

However, there was no FSL module in Lmod. (“module spider fsl” gets nothing.) So, I kept that `setpkgs -a fsl_5.0.9` command in there.

Let me know if you have questions and I can help you out.
