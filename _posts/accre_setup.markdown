October 2, 2017

# Setting up ACCRE for Neuroimaging

So you want to do neuroimaging research on Vanderbilt's Advanced Computing Cluster for Research and Engineering? This quick-start guide should help you set up your *.bashrc* and other supporting files. It will also explain some of the particularities of working on the cluster.

### tldr

Copy the contents of this `.bashrc` file to yours in `~/.bashrc`.  

### 1. Set up your ~/.bashrc

ACCRE uses the BASH scripting language by default. There are books written on 


### Load relevant software

```
module load GCC/5.4.0-2.26 \
	OpenMPI/1.10.3 \
	FSL/5.0.10 \
	git/2.12.2 \
	FreeSurfer/5.3.0-centos6_x86_64 \
	Anaconda3 \
	MATLAB
```

```
# Save current module list as "default" set
module save default

# Clear modules
module purge

# Reload modules
module load default
```

```
# Set Freesurfer subjects directory 
export SUBJECTS_DIR=~/freesurfer-subjects
```

```
# Set alias to start Matlab in terminal (or you can use Octave)
alias mat="matlab -nosplash -nodesktop "
```

### Set up a Conda environment for Python

[Anaconda](https://www.anaconda.com/download/) is an excellent way to create an manage virtual Python environments, and it's ACCRE's preferred method. Among other things, it allows users to install custom packages, Python distributions, etc., without messing with the "core" Python that serves all of ACCRE.  

```
module load Anaconda3

# Create a Python 2 environment
conda create -y --name=py2 python=2.7

# Create a Python 3 environment
conda create -y --name=py3 python=3.6

```

To load "py2" environment, type `source activate py2`. Note that you will have to do this *every time you log on to the cluster*, or you can include it in your ~/.bashrc so it activates the environment automatically on startup. To detach an environment, type `source deactivate` -- you can then load a new environment if you wish.  

To install new packages into your Conda environment, type `conda install PACKAGE_NAME_1 PACKAGE_NAME_2 ...`.  Note that for some research software, you may need to add additional "repositories" (or use `pip install`) to manage packages. These additional commands are often found in the documentation.  

### Set up DAX tools for working with XNAT

```
# One-time install of DAX
source activate py2 	# or other Python 2 env
pip install -y dax
```

```
# Export XNAT variables
. ~/.xnat_profile
```

```
# Add XNAT Variables to Global Environment (for DAX tools)
export XNAT_HOST=http://xnat.vanderbilt.edu:8080/xnat
export XNAT_USER=YOUR_XNAT_USER_NAME
export XNAT_PASS=YOUR_XNAT_PASSWORD
```


### Using Jupyter Notebook for Pythonic (or R-tastic...?) data analysis

`jupyter notebook --no-browser --ip='*' --port=9999`


### Source the CUTTING lab version of AFNI, if you wanna

```
# Add AFNI to path
export PATH=/scratch/cutting/software/afni/:$PATH
```