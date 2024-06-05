# Context

GenAI allows for the idea of “Zero” shot learning, basically the ability to build a solution without any training data.

This made it easier to get started with building AI/ML solutions.

However, data is still the most important aspect of any AI/ML system.

This workshop hopes to provide some insight into why AI/ML is a data centric problem and that there is no silver bullet that solves any problem.

## Task

An incident is declared. We want to be able to quickly surface relevant information to help the responders.

**Question**: how might you approach this problem?

## Problem Framing

Here are two example framing of this problem:

1. Ideal solution: A fully automatic Root Cause Analysis Agent

This is a hard problem to solve that will take a lot resources to explore and build.

2. Realistic solution: Find and recommend relevant existing resources (e.g. dashboards)

This is a much easier problem, we are simply making recommendation instead of doing diagnosis.

## Models

We will explore 3 different approaches today:
- Regex
- Traditional Deep Learning
- GPT4