export PYTHONPATH=$PYTHONPATH:/mloscratch/homes/$GASPAR/path/to/root_of_MultiMeditron
export PYTHONPATH=$PYTHONPATH:/mloscratch/homes/$GASPAR/path/to/End2End/src

# Faster downloads
export HF_HUB_ENABLE_HF_TRANSFER=1

python examples/simple-app/app/main.py indexer index --input-file examples/input-data/book.txt \
    --output-dir temp --cache-dir temp/cache \
    --llm-type multimeditron --llm-model /mloscratch/homes/multimeditron/models/MultiMeditron-Proj-Image-Long/checkpoint-1000/ \
    --embedding-type huggingface --embedding-model sentence-transformers/all-mpnet-base-v2 \


