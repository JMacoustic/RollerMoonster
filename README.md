# Crawling Snake Model
![Demo GIF](report/demo_gif.gif)

This is a hierarchical snake model implemented using pyglet, by Mechanical Engineering undergraduate student in SNU, as a homework project. Camera codes and basic skeletons are referenced from [SNU_ComputerGraphics](https://github.com/SNU-IntelligentMotionLab/SNU_ComputerGraphics_).

## Requirements

This code uses [Pyglet](https://github.com/pyglet/pyglet) which is a cross-platform windowing library under Python 3.8+. 
Supported platforms are:

* Windows 7 or later
* Mac OS X 10.3 or later
* Linux

## Installation

First, download miniconda(recommended) or anaconda.
- **[Download Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install)**
- [Download Anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

Second, clone repository.

    git clone https://github.com/JMacoustic/CrawlingSnake.git

Finally, go into the cloned repo and create environment.
    
    cd path/to/cloned/repo/
    conda env create -f environment.yml

## Run

Now, simply activate conda environment and run the code.

    conda activate snake_env
    python main.py

## How to play

1. Keyboard controls. You can press multiple buttons together. Some will work, some won't. Test it out!
    - key 1: start moving. sorry but you cannot change direction
    - key 2: stop moving.
    - key 3: raise head.
    - key 4: attack!! you cannot attack if the head is not raised yet.
    - key 5: lower head.

2. Mouse controls.
    - Grab-and-Drag: change the view by trackball viewer. It should be intuitive.
    - Scroll: zoom in and out.
