#!/usr/bin/env bash

# TO RUN THIS SCRIPT:
# - you need to have the right to publish in the targeted repo
# - you need to check the path...they are relative

OUTPUT_DIR='output_datasets/.'
PUBLIC_DATASET_REPO='../datasets'

# copy files
cp -R $OUTPUT_DIR/daily-reports $PUBLIC_DATASET_REPO

# move to the repo
cd $PUBLIC_DATASET_REPO

# print the timestamp (needed for the frontend)
now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo $now > last_update.txt

# push to github
#git add .
#git commit -m "update $now"
#git push
