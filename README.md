# ECoG Finger Control

A project for controlling robotic fingers movements using electrocorticography (ECoG) brain-computer interface signals.

## Overview

This project implements signal processing and machine learning pipelines to decode motor intentions from ECoG recordings and translate them into fingers control commands.

## Features

- ECoG signal preprocessing and filtering
- Feature extraction from brain signals
- Real-time decoding algorithm
- Robotic fingers interface

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) for environment management
- ~~[dvc](https://dvc.org) for data version control~~ (skip and manual setup for currently small dataset)


## Installation

1. env setup
```bash
git clone <repository-url>
cd practice-ecog-finger-control
uv sync
```

2. download dataset 4 from [here](https://www.bbci.de/competition/iv/download/index.html) and unzip under `data/` folder

## Data sources

- BCI Competition IV Dataset 4: https://www.bbci.de/competition/iv/index.html

## License

MIT License