# Pong

One of the core goals is I want a vision based agent to take visual input
and react with a machine instruction. As it turns out, games are the easiest way
to create this environment. As my first experiment, want to accomplish the following

* Create a Python Pong Game
* Create an AI to accepts a visual stream and emits a stream of actions

In the past I have created OpenAI gyms and messed around with StableBaselines and I may use that again
here but for now, I am just exploring this space without anything in mind.

## Setup and breakdown

As a baseline to setup, create a conda env

```bash
conda create -n pong-experiment python=3.11
conda activate pong-experiment
conda install -c conda-forge pygame
pip install gym stable-baselines3 shimmy opencv-python
```

## Environment Assumptions

This experiment was created with the following specs.

```text
OS: Ubuntu 22.04.03 LTS
RAM: 128 GB
CPU: Ryzen 5950X (16 core)
GPU: Nvidia 3090
```

Most experiments will not require this level of hardware, but should any compatability questions arise, this is included
