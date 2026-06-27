#Importing Libraries
import pandas as pd
from pathlib import Path 
from src.features import ORIG_COLS




#Path to data director
data_dir = Path("../data")

orig_frames = []

#function to load origination files 
def orig_loader():
    """
    Collected dataset consist of the txt file without any header names and delimiter as '|'
    so we need to properly retrive the data as pandas DataFrame .
    """

    for year in range(2000,2011) :
        files = data_dir / f"sample_{year}" / f"sample_orig_{year}.txt"

        #Loading txt file of particular year as dataFrame
        
        df = pd.read_csv(
            files,
            sep="|",header=None,low_memory=False #here low memory ensure loading file at one as dataset each year have only 50k row
            )
        df.columns = ORIG_COLS
        df["ORIG_YEAR"] = year # adding year to each row 
        orig_frames.append(df)

    orig = pd.concat(orig_frames,ignore_index=True) 
    # we are ignoring index cause while creating all df pandas assign index automatically and each df is differetn from other so we amy have repetation of index we will assign index later
    return orig


perf_frames = []

#Updated Perf Laoder 
def perf_loader():
    """
    Load performance files year by year.
    We only need 3 columns out of 32 keeps memory low
    instead of loading 33M rows of unnecessary data.
    """

    for year in range(2000, 2011):
        file = data_dir / f"sample_{year}" / f"sample_svcg_{year}.txt"

        df = pd.read_csv(
            file,
            sep="|",
            header=None,
            usecols=[0, 3, 8], # only loading 3 columns we need — col 0 is loan id, col 3 is delinquency status, col 8 is zero balance code
            low_memory=False
        )

        df.columns = ["LOAN_SEQ_NUM", "DELINQ_STATUS", "ZERO_BAL_CODE"] # assigning names to 3 columns manually as files have no header

        df["PERF_YEAR"] = year # adding year to each row so we know which year this record belongs to

        perf_frames.append(df)

        del df # free memory immediately after appending — we dont need the individual year df anymore

    return pd.concat(perf_frames, ignore_index=True) # ignoring index as each year df has its own index starting from 0


# df = orig_loader()
# print(df.shape)
# print(df["ORIG_YEAR"].value_counts().sort_index())
# expected output
# (550000, 33)
# ORIG_YEAR
# 2000    50000
# 2001    50000
# 2002    50000
# 2003    50000
# 2004    50000
# 2005    50000
# 2006    50000
# 2007    50000
# 2008    50000
# 2009    50000
# 2010    50000



# df = perf_loader()
# print(df.shape)
# print(df["PERF_YEAR"].value_counts().sort_index())
# ExpectedOutput 

# (33058391, 33)
# PERF_YEAR
# 2000    1442327
# 2001    1976051
# 2002    2494549
# 2003    4073882
# 2004    3979075
# 2005    3869881
# 2006    3196675
# 2007    3003932
# 2008    2449679
# 2009    3146053
# 2010    3426287
# Name: count, dtype: int64



# perf = perf_loader()
# print("Shape:", perf.shape)
# print("\nSample:")
# print(perf.head())
# print("\nColumn types:")
# print(perf.dtypes)
# Expected Output - try to run in notebooks files to solve no such directy issues

# Shape: (33058391, 4)

# Sample:
#    LOAN_SEQ_NUM DELINQ_STATUS  ZERO_BAL_CODE  PERF_YEAR
# 0  F00Q10000035             0            NaN       2000
# 1  F00Q10000035             0            NaN       2000
# 2  F00Q10000035             0            NaN       2000
# 3  F00Q10000035             0            NaN       2000
# 4  F00Q10000035             0            NaN       2000

# Column types:
# LOAN_SEQ_NUM         str
# DELINQ_STATUS        str
# ZERO_BAL_CODE    float64
# PERF_YEAR          int64
# dtype: object

    
