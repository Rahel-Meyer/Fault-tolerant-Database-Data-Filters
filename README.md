# Prefix Filter Experiment

## Overview
This project implements an experiment to evaluate the performance of a prefix filter using two input data distributions. The user can choose between calculating a confusion matrix or statistical values based on the generated data.

## Note on Publication
This code was developed as part of my Bachelor's thesis.

## Features
- Calculate confusion matrix based on user-defined parameters.
- Compute statistical values including precision, recall, and F1-score.
- Option to use majority-based optimization for improved performance.
- Supports both realistic and uniform character distributions.

## Installation
Clone this repository
https://github.com/Rahel-Meyer/Fault-tolerant-Database-Data-Filters.git


## Usage
To run the experiment, execute the following command in your terminal:

python main.py

User Input Prompts:

Choose an option:<br>
    Enter 1 to calculate the confusion matrix.<br>
    Enter 2 to calculate statistical values.<br>
Decide whether to use majority-based optimization (enter y or n).<br>
Input parameters:<br>
    Length of input (n)<br>
    Number of characters per prefix (k)<br>
    If using optimization, enter duplicates per character (d).<br>
    Specify the character distribution type (realistic or uniform).<br>




## Results Interpretation
After running the program, you will receive output that includes either a confusion matrix or statistical metrics such as precision, recall, and F1-score based on your selection.