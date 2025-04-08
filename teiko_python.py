import pandas as pd
import numpy as np
from plotnine import *
from scipy.stats import mannwhitneyu
from scipy.stats import ttest_ind


# Read in the data
cell = pd.read_csv("cell-count.csv")

 
# # 1. Convert Cell Count to Relative Frequency


# Select Relevant Columns
cell_cols = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]
dat = cell[cell_cols + ["sample"]].copy()

# Create a "total cell count" column
dat["total_count"] = dat[cell_cols].sum(axis=1)

# Convert from a wide to long format
dat = pd.melt(dat, id_vars = ["sample", "total_count"],
              var_name = "population",
              value_name = "count")

# Calculate Cell frequencies
dat = dat.assign(percentage = lambda x : 100 * x["count"] / x["total_count"])

# Write out the dataframe to a csv file
dat.to_csv("output_files/problem1.csv", index = False)

 
# # 2. Responder/Non-Responder Statistics
# ## Part A: Boxplots


# Filter to the relevant data
dat2 = cell[(cell["treatment"] == "tr1") & (cell["condition"] == "melanoma")] \
    [["sample", "response"]] \
    .copy()

# Join Relative Frequency Data with reponses and treatments
dat2 = pd.merge(dat, dat2, how = "inner", on = "sample")

# Make boxplots
rel_frq_plot = ggplot(dat2, aes(x = "response", y = "percentage", fill = "response")) \
+ geom_boxplot() \
+ facet_wrap("~population") \
+ theme_bw() \
+ theme(legend_position = "none") \
+ labs(
    title = "Boxplots of Population Relative Frequencies",
    x = "Response",
    y = "Relative Frequency (Percentage)"
)

# Save the Plot to a file
rel_frq_plot.save("output_files/problem2A_plot.png", dpi=500)

 
# # Part B: Statistics

results = {"population" : [],
           "test" : [],
           "p-value" : []}

# Run through a loop of each cell population
for i in dat2["population"].unique():
    # Get data for each cell population
    tmp = dat2[dat2["population"] == i].copy()
    pop1 = tmp[tmp["response"] == "y"]["percentage"]
    pop2 = tmp[tmp["response"] == "n"]["percentage"]
    
    # Calculate Two Sample T-Test Statistic
    stat, t_p_value = ttest_ind(pop1, pop2)

    # Record Results
    results["population"].append(i)
    results["test"].append("t_test")
    results["p-value"].append(t_p_value)

    # Calculate Wilcoxon Rank-Sum Test (More Robust)
    stat, w_p_value = mannwhitneyu(pop1, pop2)

    # Record Results
    results["population"].append(i)
    results["test"].append("Wilcoxon")
    results["p-value"].append(w_p_value)

results_df = pd.DataFrame(results)

# Write out the results to a CSV file
results_df.to_csv("output_files/problem2B_results.csv", index = False)
