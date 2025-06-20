#!/bin/bash

# Set the LD_LIBRARY_PATH to include the cudnn libraries
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/cwichering/src/extern/vibe/.venv/lib/python3.10/site-packages/nvidia/cudnn/lib:/home/cwichering/src/extern/vibe/.venv/lib/python3.10/site-packages/ctranslate2.libs

# Create symbolic links for the missing libraries
mkdir -p /tmp/cudnn_links

# Create links for libcudnn_ops.so
ln -sf /home/cwichering/src/extern/vibe/.venv/lib/python3.10/site-packages/nvidia/cudnn/lib/libcudnn_ops_infer.so.8 /tmp/cudnn_links/libcudnn_ops.so.9
ln -sf /home/cwichering/src/extern/vibe/.venv/lib/python3.10/site-packages/nvidia/cudnn/lib/libcudnn_ops_infer.so.8 /tmp/cudnn_links/libcudnn_ops.so.9.1
ln -sf /home/cwichering/src/extern/vibe/.venv/lib/python3.10/site-packages/nvidia/cudnn/lib/libcudnn_ops_infer.so.8 /tmp/cudnn_links/libcudnn_ops.so.9.1.0

# Create links for libcudnn_cnn.so
ln -sf /home/cwichering/src/extern/vibe/.venv/lib/python3.10/site-packages/nvidia/cudnn/lib/libcudnn_cnn_infer.so.8 /tmp/cudnn_links/libcudnn_cnn.so
ln -sf /home/cwichering/src/extern/vibe/.venv/lib/python3.10/site-packages/nvidia/cudnn/lib/libcudnn_cnn_infer.so.8 /tmp/cudnn_links/libcudnn_cnn.so.9
ln -sf /home/cwichering/src/extern/vibe/.venv/lib/python3.10/site-packages/nvidia/cudnn/lib/libcudnn_cnn_infer.so.8 /tmp/cudnn_links/libcudnn_cnn.so.9.1
ln -sf /home/cwichering/src/extern/vibe/.venv/lib/python3.10/site-packages/nvidia/cudnn/lib/libcudnn_cnn_infer.so.8 /tmp/cudnn_links/libcudnn_cnn.so.9.1.0

# Create links for libcudnn_graph.so
ln -sf /home/cwichering/src/extern/vibe/.venv/lib/python3.10/site-packages/nvidia/cudnn/lib/libcudnn.so.8 /tmp/cudnn_links/libcudnn_graph.so
ln -sf /home/cwichering/src/extern/vibe/.venv/lib/python3.10/site-packages/nvidia/cudnn/lib/libcudnn.so.8 /tmp/cudnn_links/libcudnn_graph.so.9
ln -sf /home/cwichering/src/extern/vibe/.venv/lib/python3.10/site-packages/nvidia/cudnn/lib/libcudnn.so.8 /tmp/cudnn_links/libcudnn_graph.so.9.1
ln -sf /home/cwichering/src/extern/vibe/.venv/lib/python3.10/site-packages/nvidia/cudnn/lib/libcudnn.so.8 /tmp/cudnn_links/libcudnn_graph.so.9.1.0

# Create base libcudnn links as well
ln -sf /home/cwichering/src/extern/vibe/.venv/lib/python3.10/site-packages/nvidia/cudnn/lib/libcudnn.so.8 /tmp/cudnn_links/libcudnn.so.9
ln -sf /home/cwichering/src/extern/vibe/.venv/lib/python3.10/site-packages/nvidia/cudnn/lib/libcudnn.so.8 /tmp/cudnn_links/libcudnn.so.9.1
ln -sf /home/cwichering/src/extern/vibe/.venv/lib/python3.10/site-packages/nvidia/cudnn/lib/libcudnn.so.8 /tmp/cudnn_links/libcudnn.so.9.1.0

# Add the links directory to LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/tmp/cudnn_links

# Run the application with uv
uv run main.py
