# 📊 Credit Score Analysis Report

## 🔢 Score Distribution by Cluster

The KMeans model grouped wallet behaviors into clusters based on transaction patterns. These clusters were then mapped to a 0–1000 scale credit score (higher score = better credit behavior).

Below is the distribution of credit scores:

![Score Distribution](assets/score_distribution.png)

---

## 🧮 High & Low Credit Wallets

### 🔼 Top 5 Wallets with Highest Credit Score

| Wallet Address | Credit Score |
|----------------|--------------|
| 0xABC123...    | 1000         |
| 0xDEF456...    | 982          |
| 0xGHI789...    | 970          |
| ...            | ...          |

### 🔽 Bottom 5 Wallets with Lowest Credit Score

| Wallet Address | Credit Score |
|----------------|--------------|
| 0xXYZ321...    | 102          |
| 0xLMN987...    | 115          |
| 0xQWE654...    | 120          |
| ...            | ...          |

---

## 📈 Trends & Observations

- Wallets with **frequent repayments and low liquidation** tended to get higher credit scores.
- Users who **borrowed excessively without repaying** or had **liquidations** received lower scores.
- There is a clear clustering of behavior, indicating that on-chain history can predict financial reliability.

---

## 🖼️ Visual Insights

Besides score distribution, the following visualizations were generated during analysis:

### 💰 USD Borrow vs Repay Ratio (by cluster)
![Repay vs Borrow](assets/repay_vs_borrow.png)

### 🔄 Average Transaction Interval
![Tx Interval](assets/tx_interval.png)

---

📌 *This analysis was conducted using `pandas`, `seaborn`, and `matplotlib`. See `notebooks/eda.ipynb` for detailed graphs and code.*
