---
layout: post
title:  "DSB18: Image processing basics"
date:   2018-02-04 6:00:00
categories: data-science 
comments: true
---

The **2018 Data Science Bowl** is on! The goal of the competition is to identify individual nuclei in microscopy images. The leaderboard is filled with people using U-Nets and other deep learning tools, but I thought I'd start with what I know: image processing techniques. 

This kernel ([runnable on Kaggle](https://www.kaggle.com/stkbailey/teaching-notebook-for-total-imaging-newbies)) will implement classical image techniques and will hopefully serve as a useful primer to people who have never worked with image data before. Ultimately, we will develop a simple pipeline using `scipy` and `numpy` (and a little bit of `scikit-image`) that we can apply to the test images -- in fact, we won't even use the training images except to optimize parameters.


{% highlight python %}
import imageio
im = imageio.imread(str(im_path))
{% endhighlight %}

### Dealing with color

The images in this dataset can be in RGB, RGBA and grayscale format, based on the "modality" in which they are acquired. For color images, there is a third dimension which encodes the "channel" (e.g. Red, Green, Blue). To make things simpler for this first pass, we can coerce all these images into grayscale using the `rgb2gray` function from `scikit-image`.

{% highlight python %}
# Print the image dimensions
print('Original image shape: {}'.format(im.shape))

# Coerce the image into grayscale format (if not already)
from skimage.color import rgb2gray
im_gray = rgb2gray(im)
print('New image shape: {}'.format(im_gray.shape))
{% endhighlight %}

>    Original image shape: (520, 696, 4)
>    New image shape: (520, 696)

![Original and grayscale images]( {{ "assets/dsb2018/basics-1.png" | absolute_url }} )


### Removing background
Perhaps the simplest approach for this problem is to assume that there are two classes in the image: objects of interest and the background. Under this assumption, we would expect the data to fall into a bimodal distribution of intensities. If we found the best separation value, we could "mask" out the background data, then simply count the objects we're left with.

The "dumbest" way we could find the threshold value would be to use a simple descriptive statistic, such as the mean or median. But there are other methods: the "Otsu" method is useful because it models the image as a bimodal distribution and finds the optimal separation value. 


{% highlight python %}
from skimage.filters import threshold_otsu
thresh_val = threshold_otsu(im_gray)
mask = np.where(im_gray > thresh_val, 1, 0)

# Make sure the larger portion of the mask is considered background
if np.sum(mask==0) < np.sum(mask==1):
    mask = np.where(mask, 0, 1)
{% endhighlight %}


![Images]( {{ "assets/dsb2018/basics-2.png" | absolute_url }} )



### Deriving individual masks for each object

For this contest, we need to get a separate mask for each nucleus. One way we can do this is by looking for all objects in the mask that are connected, and assign each of them a number using `ndimage.label`.  Then, we can loop through each `label_id` and add it to an iterable, such as a list.


{% highlight python %}
from scipy import ndimage
labels, nlabels = ndimage.label(mask)

label_arrays = []
for label_num in range(1, nlabels+1):
    label_mask = np.where(labels == label_num, 1, 0)
    label_arrays.append(label_mask)

print('There are {} separate components / objects detected.'.format(nlabels))
{% endhighlight %}

    There are 76 separate components / objects detected.
    
![Images]( {{ "assets/dsb2018/basics-3.png" | absolute_url }} )

A quick glance reveals two problems (in this very simple image): 

- There are a few individual pixels that stand alone (e.g. top-right)
- Some cells are combined into a single mask (e.g., top-middle)
    
Using `ndimage.find_objects`, we can iterate through our masks, zooming in on the individual nuclei found to apply additional processing steps.  `find_objects` returns a list of the coordinate range for each labeled object in your image.


{% highlight python %}
for label_ind, label_coords in enumerate(ndimage.find_objects(labels)):
    cell = im_gray[label_coords]
    
    # Check if the label size is too small
    if np.product(cell.shape) < 10: 
        print('Label {} is too small! Setting to 0.'.format(label_ind))
        mask = np.where(labels==label_ind+1, 0, mask)

### Regenerate the labels
labels, nlabels = ndimage.label(mask)
print('There are now {} separate components / objects detected.'.format(nlabels))
{% endhighlight %}

    Label 4 is too small! Setting to 0.
    Label 5 is too small! Setting to 0.
    Label 7 is too small! Setting to 0.
    ...
    There are now 60 separate components / objects detected.
    


![Images]( {{ "assets/dsb2018/basics-4.png" | absolute_url }} )


Label #2 has the "adjacent cell" problem: the two cells are being considered part of the same object. One thing we can do here is to see whether we can shrink the mask to "open up" the differences between the cells. This is called mask erosion. We can then re-dilate it to to recover the original proportions. 


{% highlight python %}
# Get the object indices, and perform a binary opening procedure
two_cell_indices = ndimage.find_objects(labels)[1]
cell_mask = mask[two_cell_indices]
cell_mask_opened = ndimage.binary_opening(cell_mask, iterations=8)
{% endhighlight %}


![Images]( {{ "assets/dsb2018/basics-5.png" | absolute_url }} )

We can then loop through the labels and create masks for each image -- but this is specific to the competition and has been cut from this post. (See the [Kaggle kernel](https://www.kaggle.com/stkbailey/teaching-notebook-for-total-imaging-newbies) if interested.) Hopefully soon I will have some neural network tutorials to share!
