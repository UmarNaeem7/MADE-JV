# Project Plan

## Title
Change in Air Quality Across the Americas & the Primary Contributors

## Main Question
How has air qulaity in the major countries in North & South Americas changed over the past & what are the primary causes for such changes?

## Description
Air quality degradation is an important problem because it directly affects all the living things including humans, animals & plants. It can lead to health risks, negative environmental impact, economic costs, poor quality of life, etc.

This project analyses the problem by looking at the air quality datasets & emissions datasets & then drawing useful insights & conclusions. The aim would be to find strong correlations between air quality degradations & harmful emissions to determine which emissions have the most negative impact on air quality.

The results can help identifying which countries in the Americas need to pay serious attention to their air quality improvement and as a next step which emissions (causes) they need to lower down.

## Datasources

### Datasource1: EDGAR - Emissions Database for Global Atmospheric Research (Air Quality Metrics)
* Metadata URL: https://edgar.jrc.ec.europa.eu/dataset_ap81
* Data URL: https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/EDGAR/datasets/v81_FT2022_AP_new/EDGAR_PM25_1970_2022.zip
* Data Type: Excel file (that is zipped)
* Note: This in only one of the few datasets for AQI, all of the datasets to be used in the project can be found in the [air_quality_metrics.txt][i2] file.

This data source contains data about air quality measurements in pm 2.5 metric for all the countries from the years 1970-2022.

### Datasource2: EDGAR - Emissions Database for Global Atmospheric Research (Pollutants)
* Metadata URL: https://edgar.jrc.ec.europa.eu/emissions_data_and_maps
* Data URL: https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/EDGAR/datasets/v80_FT2022_GHG/EDGAR_CH4_1970_2022.zip
* Data Type: Excel file (that is zipped)
* Note: This in only one of the few datasets for pollutants, all of the datasets to be used in the project can be found in the [pollutants.txt][i3] file.

This data source contains data about emissions of CH4 (Methane) in all the countries from the years 1970.2022. Emissions can be of several types like greenhouse gases, aerosols, air pollutants, etc. This dataset focuses on the emissions of methane gas in particular.

## Project Pipeline

### Data Extraction & Preprocessing
The project requires the use of several datasets. They have been divided into 2 categories based on the purpose they will serve in this project:

1. Air quality metrics
2. Pollutants

Since, there are 7 datasets to be used in the project, their corresponding download urls have been placed in a links folder inside the project dir based on their category of use.

The script `data_extraction.py` takes care of automating the data extraction process by automatically fetching the urls from the `links` folder & then saving them to the `data` dir.

All the download urls give a zip file with the dataset in the excel format. The built-in python library `zipfile` is used to unzip the response from the get requests & then the excel file that is the dataset is found & saved in the `data` dir.
The datasets are already cleaned & ready for use out of the box for the purpose of this project so no additional pre-processing is required. 


## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Data Extraction Issue [#1][i1]
2. Automated Tests Issue [#2][i4]

[i1]: https://github.com/UmarNaeem7/MADE-JV/issues/1#issue-2647649796
[i2]: https://github.com/UmarNaeem7/MADE-JV/blob/main/project/links/air_quality_metrics.txt
[i3]: https://github.com/UmarNaeem7/MADE-JV/blob/main/project/links/pollutants.txt
[i4]: https://github.com/UmarNaeem7/MADE-JV/issues/2#issue-2719062504