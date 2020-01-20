# iot-sense-pod
docker build -t tekn0ir/iot-sense-pod:latest ./docker
docker push tekn0ir/iot-sense-pod:latest


## Send message to sense pod
```bash
export DEVICE_ID=raspberrypi4
export PROJECT_ID=teknoir-poc
export REGION=us-central1
export REGISTRY_ID=teknoir-iot-registry-poc
gcloud iot devices commands send \
    --command-file=message.json \
    --region=$REGION  \
    --registry=$REGISTRY_ID \
    --device=$DEVICE_ID \
    --subfolder=iot-sense-pod
```
