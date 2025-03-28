import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data files
subscription_df = pd.read_csv(r"C:\Users\bhara\OneDrive\Desktop\SHIKHA DATA ENGINEER\subscription_information.csv")

financial_df = pd.read_csv(r"C:\Users\bhara\OneDrive\Desktop\SHIKHA DATA ENGINEER\finanical_information.csv")
payment_df = pd.read_csv(r"C:\Users\bhara\OneDrive\Desktop\SHIKHA DATA ENGINEER\payment_information.csv")
industry_client_df =pd.read_csv(r"C:\Users\bhara\OneDrive\Desktop\SHIKHA DATA ENGINEER\industry_client_details.csv")

# Question 1: Count Finance Lending and Blockchain Clients
finance_clients = industry_client_df[industry_client_df['industry'] == 'Finance Lending'].shape[0]
blockchain_clients = industry_client_df[industry_client_df['industry'] == 'Block Chain'].shape[0]
print(f"Finance Lending Clients: {finance_clients}")
print(f"Blockchain Clients: {blockchain_clients}")

# Question 2: Industry with Highest Renewal Rate
merged_df = subscription_df.merge(industry_client_df, on="client_id", how="left")
renewal_rates = merged_df.groupby("industry")["renewed"].mean().sort_values(ascending=False)
highest_renewal_industry = renewal_rates.idxmax()
highest_renewal_rate = renewal_rates.max()
print(f"Highest Renewal Industry: {highest_renewal_industry} ({highest_renewal_rate:.2%})")

# Question 3: Average Inflation Rate When Renewed
subscription_df["end_date"] = pd.to_datetime(subscription_df["end_date"])
financial_df["start_date"] = pd.to_datetime(financial_df["start_date"])
financial_df["end_date"] = pd.to_datetime(financial_df["end_date"])

def get_inflation_rate(subscription_end):
    """Retrieve inflation rate for a given subscription end date."""
    matching_row = financial_df[(financial_df["start_date"] <= subscription_end) & (financial_df["end_date"] >= subscription_end)]
    return matching_row["inflation_rate"].values[0] if not matching_row.empty else None

subscription_df["inflation_rate"] = subscription_df["end_date"].apply(get_inflation_rate)
average_inflation_rate = subscription_df[subscription_df["renewed"]]["inflation_rate"].mean()
print(f"Average Inflation Rate When Renewed: {average_inflation_rate:.2f}%")

# Question 4: Median Amount Paid Per Year
payment_df["payment_date"] = pd.to_datetime(payment_df["payment_date"])
payment_df["year"] = payment_df["payment_date"].dt.year
median_payment_per_year = payment_df.groupby("year")["amount_paid"].median()
print("\nMedian Amount Paid Each Year:")
print(median_payment_per_year)

# Plot: Industry-wise Renewal Rate
plt.figure(figsize=(10, 5))
sns.barplot(x=renewal_rates.index, y=renewal_rates.values, palette="viridis")
plt.xticks(rotation=45)
plt.xlabel("Industry")
plt.ylabel("Renewal Rate")
plt.title("Renewal Rate by Industry")
plt.show()
