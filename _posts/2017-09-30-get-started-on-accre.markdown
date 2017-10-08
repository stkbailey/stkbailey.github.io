---
layout: post
title:  "Neuroimaging on ACCRE"
date:   2017-09-30 13:46:40
categories: ebrl, vanderbilt
comment: true
---

# Setting up ACCRE for Neuroimaging

So you want to do neuroimaging research on Vanderbilt's Advanced Computing Cluster for Research and Engineering? This quick-start guide should help you set up your *.bashrc* and other supporting files. It will also explain some of the particularities of working on the cluster.

### tldr

First, run the code found in the ["sample_setup.txt" file]({{ "/assets/sample_setup.txt" | absolute_url }}) to set up your Python environment and DAX tools for interfacing with XNAT. Then, copy the contents of *[this ".bashrc" file]({{ "/assets/sample_bashrc.txt" | absolute_url }})* to yours in `~/.bashrc`.  

### 1. Get to know your ~/.bashrc

ACCRE uses the [Bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)) shell and command language by default. There are plenty of [books](http://shop.oreilly.com/product/9780596009656.do) and [resources](http://www.bash.academy/) out there to help familiarize yourself with the language. To get started, though, you just need to learn the very basics: `ls`, `cd`, `cp`, `mkdir`, `rm`.

Every time you log onto ACCRE, you "start fresh", meaning anything you did last time - loading software, setting variables, activating Python - is forgotten. This can get annoying if you do the same thing every time you log in. 

Here is where your `~/.bashrc` ("BASH Run Commands") file comes into play. Every time you open up a shell, this file gets run. So if you want the shell to say hello to you every time you log in, you could just add `echo Good Morning, Creator` somewhere in that file. 

Throughout this tutorial, I'll tell you to add commands to your `.bashrc`. To do this, type `nano ~/.bashrc` to open up the `nano` text editor. Copy the text and press `ctrl+x` to close. NExt time you log in, the commands will be run automatically.


### 2. Load and configure relevant software

ACCRE uses [Lmod](http://www.accre.vanderbilt.edu/?page_id=3358) for managing software modules within their shared computing environment. What that means is that ACCRE staff have installed many of your favorite neuroimaging tools directly onto the cluster -- you just have to load them up when you want to use them using `module load PACKAGE_NAME`.

There are are a lot of packages (use `module spider` to list them), and sometimes multiple packages need to be loaded at the same time to function correctly. Below is an example `module load` command. That set of packages is then saved as a "default" set of packages.

{% highlight python %}
# Load neuroimaging-related packages
module load GCC/5.4.0-2.26 \
	OpenMPI/1.10.3 \
	Anaconda3 \
	FSL/5.0.10 \
	FreeSurfer/5.3.0-centos6_x86_64 \
	MATLAB \
	git/2.12.2

# Save current module list as "default" set
module save default

# Now, to reload these packages, type `module restore default`
{% endhighlight %}

#### Freesurfer

If you want to use Freesurfer, you need to set the `SUBJECTS_DIR` environment variable after loading Freesurfer. To do that, add a line like the following to your `.bashrc`. 

{% highlight python %}
# Set Freesurfer subjects directory 
export SUBJECTS_DIR=~/freesurfer-subjects
{% endhighlight %}

#### Matlab

Matlab use requires an ACCRE license which can be purchased on an annual basis. Because Matlab can be graphics-heavy, I prefer to work directly in the terminal by starting Matlab with the `-nosplash` and `-nodesktop` flags. 

{% highlight python %}
# Set alias to start Matlab in terminal (just type `mat` to launch)
alias mat="matlab -nosplash -nodesktop "
{% endhighlight %}

### 3. Set up a Conda environment for Python

[Anaconda](https://www.anaconda.com/download/) is an excellent way to create an manage virtual Python environments, and it's ACCRE's preferred method. Among other things, it allows users to install custom packages, Python distributions, etc., without messing with the "core" Python that serves all of ACCRE.  

{% highlight python %}
module load Anaconda3

# Create a Python 2 environment
conda create -y --name=py2 python=2.7

# Create a Python 3 environment
conda create -y --name=py3 python=3.6
{% endhighlight %}

To load "py2" environment, type `source activate py2`. Note that you will have to do this *every time you log on to the cluster*, or you can include it in your ~/.bashrc so it activates the environment automatically on startup. To detach an environment, type `source deactivate` -- you can then load a new environment if you wish.  

To install new packages into your Conda environment, type `conda install PACKAGE_NAME_1 PACKAGE_NAME_2 ...`.  Note that for some research software, you may need to add additional "repositories" (or use `pip install`) to manage packages. These additional commands are often found in the documentation.  

### 4. Set up DAX tools for working with XNAT

[DAX (Distributed Automation for XNAT](https://github.com/VUIIS/dax) is a set of tools that will help you interface with XNAT data. It's managed by VUIIS, and although you probably won't need to use much of the toolbox, you might need `Xnatdownload`. 

#### Setting it all up
{% highlight python %}
# One-time install of DAX into your Python environment
source activate py2 	
pip install -y dax

# One-time setup of ~/.dax_settings.ini
dax_setup
{% endhighlight %}

The program will prompt you to enter your XNAT host (`http://xnat.vanderbilt.edu:8080/xnat`) and login information. For the rest of the questions, you can simply type "no" to select the defaults. 


#### Using Xnatdownload

Xnatdownload will connect to XNAT, log-in with your credentials and access whichever files/resources you ask for. To download data, you need to have some or all of the following information.

- XNAT project
- Subject ID
- Session ID
- Scan Type
- Scan Resource Type (e.g. NIFTI)

A typical call to one of our lab's projects would look something like this: `Xnatdownload -p CUTTING --subj LD4001_v1 --sess 207943 -s all --rs NIFTI -d ~./xnat_data`  

For further information, see its documentation by typing simply `Xnatdownload`. 

### 5. Source the CUTTING lab version of AFNI, if you wanna

If you're interested in using AFNI, you (currently) have to set up your own copy of the binaries on the cluster. Luckily, there are a few that are floating around in publicly accessible spaces -- I believe that `/scratch/cutting/software/afni` is one of them. Simply add this directory to your path, and then try typing any of the AFNI commands (`afni` comes to mind...)!

{% highlight python %}
# Add AFNI to path
export PATH=/scratch/cutting/software/afni/:$PATH
{% endhighlight %}