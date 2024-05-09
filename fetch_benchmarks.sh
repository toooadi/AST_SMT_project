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