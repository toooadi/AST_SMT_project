#!/bin/bash

# Step 1: Download the relevant benchmarks
relevant_benchmarks=(
    "LIA"
    "QF_LIA"
    "QF_LRA"
    "QF_NIA"
)

mkdir -p benchmarks
for str in ${relevant_benchmarks[@]}; do
    wget -qO- --show-progress "https://zenodo.org/records/11061097/files/${str}.tar.zst?download=1" | tar -x --zstd -C "./benchmarks"
done

# Step 2: Clone the specified GitHub repository
git clone https://github.com/testsmt/semantic-fusion-seeds.git semantic-fusion-seeds

# Step 3: Remove the .git directory to unlink from the GitHub repository
rm -rf semantic-fusion-seeds/.git

echo "semantic-fusion-seeds" >> .gitignore


# Step 4: Remove all folders that are not in the keep list
folders_to_keep=(
  "ALIA"
  "AUFBVDTLIA"
  "AUFDTLIA"
  "AUFLIA"
  "AUFLIRA/unsat"
  "AUFNIRA"
  "BV"
  "FP"
  "LIA"
  "LRA"
  "NRA"
  "QF_ABV"
  "QF_ABVFP"
  "QF_ALIA/unsat"
  "QF_ANIA/sat"
  "QF_AUFLIA"
  "QF_AX"
  "QF_BV"
  "QF_BVFP"
  "QF_FP"
  "QF_LIA"
  "QF_LRA"
  "QF_NRA"

)

# Directory to clean
target_directory="semantic-fusion-seeds"

# List all folders in the target directory
all_folders=$(find "$target_directory" -mindepth 1 -maxdepth 1 -type d)

# Loop through all folders and delete those not in the list to keep
for folder in $all_folders; do
  folder_name=$(basename "$folder") # Get the folder name
  if [[ ! " ${folders_to_keep[@]} " =~ " ${folder_name} " ]]; then
    echo "Deleting folder: $folder"
    rm -rf "$folder"
  fi
done

