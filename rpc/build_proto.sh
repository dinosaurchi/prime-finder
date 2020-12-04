# Python
python -m grpc_tools.protoc -I ./protobuf --grpc_python_out ./python --python_out ./python ./protobuf/**/**/*.proto
find ./python -type d -exec touch {}/__init__.py \;