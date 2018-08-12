def submit_brain_for_printing(subj_id, scratch_dir='/scratch/bailesk1', image_path=None, 
                              decimation_level=0.15, anat_scan_type=None):
    '''Takes a T1-weighted image and submits a cluster job which runs Freesurfer recon-all, 
        then post-processes the surface files for 3D-printing.'''

    import os
    
    # Check for existence of data folders
    fs_subj_dir='{}/freesurfer-subjects'.format(scratch_dir)
    if not os.path.exists(fs_subj_dir):
        os.mkdir(fs_subj_dir)
    for folder in ['tmp', 'mesh', 'slurm']:
        if not os.path.exists('{}/{}'.format(fs_subj_dir, folder)):
            os.mkdir('{}/{}'.format(fs_subj_dir, folder))

    # Download data from Xnat, if no image_path is provided
    if not image_path:
        image_path = '{}/tmp/{}_raw.nii.gz'.format(fs_subj_dir, subj_id)
        dl_cmd = """
# Download the image
Xnatdownload -p CUTTING --subj {sid} --sess all --scantype {st} --rs NIFTI -d {scr}
DLPATH=`find {scr}/*/{sid}/*/*{st}*/ -type f -name "*.nii.gz"`
cp $DLPATH {ip}""".format(sid=subj_id, st=anat_scan_type, scr=scratch_dir, ip=image_path)
        print(os.popen(dl_cmd).read())

    # Write out Freesurfer Command
    fs_cmd = '''
# Setup Freesurfer and SUBJECTS_DIR
module load FreeSurfer
export SUBJECTS_DIR={fs}


# Run Freesurfer
recon-all -i {ip} -s {sid} -all

# Collapse edges and save to "mesh" folder
for HEMI in lh rh; do 
    mris_decimate {fs}/{sid}/surf/$HEMI.pial -d {d} {fs}/{sid}/surf/$HEMI.d{dp}.pial
    mris_convert {fs}/{sid}/surf/$HEMI.d{dp}.pial {fs}/mesh/{sid}_$HEMI.d{dp}.stl
done
mris_convert --combinesurfs {fs}/{sid}/surf/lh.d{dp}.pial {fs}/{sid}/surf/rh.d{dp}.pial \
    {fs}/mesh/{sid}_2h.d{dp}.stl 
'''.format(fs=fs_subj_dir, sid=subj_id, ip=image_path,
               d='{}'.format(decimation_level), dp='{}'.format(int(decimation_level*100))) 


    # Create SLURM Wrapper
    sbatch_path = '{}/slurm/{}_submit.txt'.format(fs_subj_dir, subj_id)
    sbatch_cmd = """#!/bin/bash

    #SBATCH --nodes=1
    #SBATCH --ntasks=1
    #SBATCH --mem-per-cpu=16G
    #SBATCH --time=0-24:00:00
    #SBATCH --output={fs}/slurm/{sid}_out.txt
    #SBATCH --error={fs}/slurm/{sid}_err.txt
    #SBATCH --job-name=fs_{sid}

    # Put commands for executing job below this line
    {script}
    """.format(fs=fs_subj_dir, sid=subj_id, script=fs_cmd)

    # Write and Run the Batch
    with open(sbatch_path, 'w') as f:
        f.write(sbatch_cmd)    
    slurm_out = os.popen('sbatch {}'.format(sbatch_path)).read()
    
    return slurm_out