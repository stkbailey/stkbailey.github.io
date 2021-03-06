---
layout: post
title:  "Printing 3D Brains at Vanderbilt"
date:   2017-10-09 1:47:00
categories: vanderbilt 
comments: true
---

Every time we scan a kid as part of our study, we print them a picture of their brain. They love it - and who wouldn't? A few years ago, I had the realization that we didn't need to stop with paper -- we could 3D-print the whole thing!

There are a [few great resources](http://www.instructables.com/id/3D-print-your-own-brain/) out there for doing this, but I wanted to simplify the process and write out some code for mesh-ifying brains so that our lab can continue to do this in perpetuity. Luckily, the hardest part -- actually printing the brains -- can be outsourced to [VU Medical Center](http://www.library.vanderbilt.edu/biomedical/technology/3d-printing.php) (or [other places](https://www.shapeways.com/)).

There are a few other tutorials out there for doing this. This tutorial is specifically for Vanderbilt users who want to run the cortical reconstruction on ACCRE.

#### What you need
- An ACCRE account
- Python environment with DAX tools (if downloading from XNAT)
- A T1-weighted brain image

### 1. Download image from XNAT

The first thing we have to do is get an image file for use with Freesurfer. This should be T1-weighted image, meaning that white matter is bright and gray matter is dark. 

{% highlight bash %}
Xnatdownload -p PROJECT_NAME --subj SUBJECT_NAME --sess all --scantype SCAN_NAME --rs NIFTI 
{% endhighlight %}

If you already have the image data on ACCRE, you can just put it in a location accessible by the cluster (e.g., your home directory).

### 2. Scripting a Freesurfer reconstruction w/ edge decimation

Freesurfer will "trace" the gray and white matter boundaries to create a 3D reconstruction of the brain surface.  The process can take a while but is easy to submit to the ACCRE cluster. 

One issue, however, is that Freesurfer surface files contain more than 100,000 vertices. Since 3D-printers generate movement files that track how to build the surface by going from point-to-point, feeding in a full-resolution surface file could cause it to break. To remedy this, we are going to reduce the number of edges in each surface file so that it can be more easily printed.

{% highlight bash %}
# Setup Freesurfer and SUBJECTS_DIR
module load FreeSurfer
export SUBJECTS_DIR=~/freesurfer-subjects

# Run Freesurfer
recon-all -i PATH_TO_SCAN -s SUBJECT_NAME -all

# Collapse edges and save to "mesh" folder
for HEMI in lh rh; do 
    mris_decimate ${SUBJECTS_DIR}/SUBJECT_NAME/surf/$HEMI.pial -d 0.15 ${SUBJECTS_DIR}/SUBJECT_NAME/surf/$HEMI.d15.stl
done
mris_convert --combinesurfs ${SUBJECTS_DIR}/SUBJECT_NAME/surf/lh.d15.pial ${SUBJECTS_DIR}/SUBJECT_NAME/surf/rh.d15.pial ${SUBJECTS_DIR}/SUBJECT_NAME/2h.d15.stl
{% endhighlight %}

![Freesurfer traces around the white matter and pial surfaces.]({{"/assets/freesurfer_3d/freesurfer_parc.PNG" | absolute_url }})

### 3. Wrap script for SLURM

Now, we just need to submit the job to the cluster via `SLURM`. We create a text file with a few flags denoting how much time and resources we want to allocate, then we'll add in the Freesurfer commands  below. We submit it by entering `sbatch <text_file>`. 

Here's what the header will look like. 

{% highlight bash %}
#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=16G
#SBATCH --time=0-24:00:00
#SBATCH --output={fs}/slurm/{sid}_out.txt
#SBATCH --error={fs}/slurm/{sid}_err.txt
#SBATCH --job-name=fs_{sid}

# Put commands for executing job below this line
{% endhighlight %}

### 4. Enlist the robots!

Finally, we put it all together into a [single function]({{"/assets/print_brain.py" | absolute_url }}) to make the prints. The key variabiles here are `subj_id`, the `scratch_dir` for Freesurfer output, and the input `image_path`. 

Downloading from XNAT is optional -- if you already have the data, simply input the `image_path` and it will ignore that section. 

A successful run will output a SLURM submission note such as:

{% highlight python %}
submit_brain_for_printing(subj_id='test_subject', 
                          fs_subj_dir='~/freesurfer-subjects', 
                          image_path=PATH_TO_SCAN)
        
        Submitted batch job 19715313
{% endhighlight %}

You can follow up on the job status by using `scontrol` and other commands like `squeue -u bailesk1`. 

![Freesurfer outputs a mesh on top of the surface, which can be 3D printed.]({{"/assets/freesurfer_3d/mesh_hires.PNG" | absolute_url }})


### 5. Outsource the printing and reap the rewards

Finally, you will have a couple of mesh files in your `${fs_subj_dir}/mesh` folder. You can pull these onto your local machine then email VUMC to get your prints. Cost goes up as a function of printing time and material required, so be aware the a full size brain could cost in excess of $30. But can you truly put a price on the fanciest paper weight you'll ever own?

