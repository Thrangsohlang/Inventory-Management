# 🎯 Objectives
- Inventory Optimization → Determine the ideal inventory levels for different product categories.
- Sales & Purchase Insights → Identify trends, top-performing products, and supplier efficiency.
- Process Improvement → Optimize procurement and stock control to minimize financial loss.

---

## 🔎 Tasks to be Performed (Any/All)
### **1️⃣ Demand Forecasting**
- Analyze **historical sales data** to predict future demand.
- Use **time-series models** for accuracy.

### **2️⃣ ABC Analysis**
- Classify inventory into **A (high value), B (moderate), and C (low priority)**.
- Prioritize high-value inventory management.

### **3️⃣ Economic Order Quantity (EOQ) Analysis**
- Calculate **optimal order quantity** to minimize ordering & carrying costs.
- Implement **just-in-time inventory practices** where feasible.

### **4️⃣ Reorder Point Analysis**
- Determine **reorder points for each product** to avoid stockouts.
- Factor in **lead time** to ensure continuity.

### **5️⃣ Lead Time Analysis**
- Optimize **supply chain efficiency** by assessing material procurement timelines.
- Reduce **waiting periods** for production inputs.

### **6️⃣ Any other aspects/analysis/trends that you can bring to the table**

## Datasets
Datasets can be downloaded from this link [DataSet](https://www.kaggle.com/datasets/sloozecareers/slooze-challenge/data)

## 🧪 Example: Sales Insights

The :mod:`inventory` package provides helpers for analysing the provided
``datasets.zip`` archive.  For instance, the snippet below prints the five
best-selling products from the sales dataset:

```python
from inventory import top_selling_from_zip

top = top_selling_from_zip(
    "datasets.zip",
    sales_file="SalesFINAL12312016.csv",  # name inside the archive
    product_col="Item",                   # product identifier column
    quantity_col="Quantity",              # quantity sold column
    top_n=5,
)
print(top)
```

Adjust the column names according to those used in the dataset.

### Working with the bundled sample data

For a quick start the repository includes a smaller ``Sample.zip`` archive.
Most functions now provide ``*_from_zip`` helpers that load the relevant CSV
directly from the archive.  For example, to list the top products in the sample
sales dataset:

```python
from inventory import top_selling_sample

print(top_selling_sample())  # defaults to "Sample.zip" in the project root
```

Similar helpers exist for demand forecasting, lead time analysis and other
inventory calculations.
