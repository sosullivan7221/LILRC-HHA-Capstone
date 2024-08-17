# LILRC-HHA-Capstone
Capstone Project for SBU AHI Program: ingesting and standardizing salary survey data from Long Island libraries

## 2024 Google Drive Link

https://drive.google.com/drive/folders/1vc8jQYpzkczLiXFHjTLitzCv0Gz3uMnx

### Project Scope

The Long Island Library Resource Council (LILRC) distributes a survey to all libraries collecting data on salaries for all workers. Public libraries submit a spreadsheet containing salary data on all workers, while private libraries individually report their income. The purpose of this project is to develop a system to collect and aggregate data into a standardized format for review and analysis.

### Objectives

1. Create a Python script to take in raw survey data and convert it into a standardized format.
    - Exampe of standardized format, where each row is equal to a unique site and job title and year: 
        - Column 1: Library Name (string)
        - Column 2: Employee Number (int)
        - Column 2: Job Title (string)
            - Job title selections can include:
                - Director
                - Assistant Director
                - Librarian
                - Assistant Librarian
                - .......
        - Column 3: Part time/Full time (string)
        - Column 4: Salary (int)
        - Column 5: Year (int)

2. Create a pipeline for merging and analyzing data between multiple years.
3. Explore Tableau and Looker Studio as options for data visualization and analysis.**

4. Incorporate geospatial data to visualize trends based on location.
5. Find state/national level salary data to compare with our region-level data.
   

### Notes/Guidelines

1. Public libraries must be able to submit a spreadsheet, individual reporting can be flexible in format (currently using an airtable survey).
2. Survey fields should be open-ended, can be further condensed and constrained in Python aggregation.
3. Nassau libraries submit their own spreadsheet, which may vary significantly from the survey sent by the LILRC.

### Current State

The application is currently deployed using streamlit. Cleaning scripts have been written only for libraries that have submitted in the 2024 survey. Recordings explaining the repository structure and demoing the app are below:

Repository Overview: https://www.loom.com/share/59238720c5104392a4f42a7e29b40b30?sid=8772188e-e508-4827-a3a1-c8dc7a0a3f80

Application Demo: https://www.loom.com/share/9bcaa3d48eb4426193326880cb86ff8f?sid=bb1b39e0-6fdb-449b-a34a-911d4c14b36a

### Future Recommendations

There are a number of features/changes that could be implemented in the future to improbe the applcation:

1. Consolidate the formatted.py and no_box.py scripts into a single script. This should act as a single script that can clean all of the files that follow the standardized format.
2. Improve and incorporate NLP for title mapping into the application. Give the NLP feedback and utilize accuracy metrics to help it improve in making predictions. 
3. Utilize regex or similar package to more cleanly remove unwanted characters from speficied columns.
4. Allow application to auto pull data from a google drive folder. Will likely need API keys.








