# Top Percent Resume Selector

## Overview

The Top Percent Resume Selector is a Python script designed to analyze and compare job descriptions with a set of resumes in PDF format. It calculates the cosine similarity between a provided job description and each resume, and then selects the top-performing resumes based on a user-defined threshold. The selected resumes are moved to a "top_qualified" folder, streamlining the hiring process.

## Features

- **Cosine Similarity Calculation:** Utilizes spaCy, scikit-learn, and PyMuPDF to preprocess text and calculate cosine similarity between job descriptions and resumes.

- **Top Percent Selection:** Allows users to specify a threshold to select the top percentage of resumes based on their similarity scores.

- **Automated File Handling:** Moves the selected resumes to a "top_qualified" folder, providing an organized view of the most promising candidates.

## Requirements

- Python 3.x
- spaCy
- scikit-learn
- PyMuPDF

## Installation

Install the required Python packages using the following command:

```bash
pip install spacy scikit-learn pymupdf
