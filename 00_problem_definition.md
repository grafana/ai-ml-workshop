## Task

An incident is declared. We want to be able to quickly surface relevant information to help the responders.

Exercise: how might you approach this problem?

## Problem Framing

We can tackle this problem is many different ways. How do we decide how to approach this problem?

Ask two questions:
- What data do we need?
- Is it feasible to gather and label the data?


1. Suggest root cause by looking at telemetry data (logs, metrics, and traces)

What data do we need?
- telemetry data mapped to root causes

Is it feasible to gather and label the data?
- telemetry data is messy, we might need to look at potentially thousands of timeseries metrics, logs, and traces
- root cause is hard to diagnose, we might only have a handful of good examples for every system we manage

While it is possible to create this dataset, it's difficult to ensure quality and high enough volume to capture the complexity


2. Suggest existing dashboards/panels based on incident data

What data do we need?
- incident timeline + text data, relevant dashboards/panels

Is it feasible to gather and label the data?
- Grafana Incident allows adding relevant dashboards/panels to the timeline

We do have the data readily available, but it can be somewhat difficult to validate whether or not the recommended dashboard is actually relevant


3. Extract key information from incident data and search for dashboards via the search API

What data do we need?
- incident data and information of interest

Is it feasible to gather and label the data?
- We have incident data available and know the few things we may be interested in