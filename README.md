This repository contains a Python script for cleaning, processing, and analyzing trade data related to waste and scrap among OECD countries. The data is sourced from a CSV file and undergoes various transformation steps to prepare it for analysis.

The purpose of this project is to process and analyze trade data concerning waste and scrap exports and imports by different countries. The dataset requires significant cleaning and transformation to be suitable for further analysis. This script automates these tasks, ensuring the data is structured and ready for use.

Key columns in the dataset are:
OECD Country: Represents the OECD member country reporting the trade data.
Year: Indicates the year of the trade activity, covering exports and imports from 2003 to 2016.
Weight in Tons: Specifies the volume of trade in tons. Exported weights are shown as negative numbers, while imported weights are positive.
Type of Shipment: Identifies whether the trade activity is an export or an import.

Dependencies:
Pandas
