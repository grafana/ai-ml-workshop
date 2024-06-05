# Deployment

## Serving infra-structure

Gateway API: auth, preprocessing, postprocessing 

Model API: model predictions, scaling, retraining if applicable

Model Store: Storage for model weights (e.g. object storage)

## Post Production Monitoring

Post production monitoring does a couple things:
- check performance in production (online evaluation)
- check to see if the distribution of data has changed
- collect data to further improve the system

1. Checking performance

Explicit: getting feedback directly from user. Unless we can modify the UX of the end product, we might not be able to do this.

Implicit: inferring feedback from user behaviour. E.g. did the user interact with the suggestions surfaced using the labels.

2. Checking for data distribution change

One easy way to measure this might just be keeping track of the distribution and the volume of model predictions.

When the data distribution changes we should be able to observe the distribution and or of model predictions change as well.

3. Data collection and feedback loop

Once we deploy a solution, we need to plan what kind of signal we want to capture.

In this case, we may want to capture all the model predictions and any implicit signals from the user.

In some cases, we are able to get high quality labelled data (AKA ground truth) in production. But the data here will need to be refined and relabeled before we can use them.