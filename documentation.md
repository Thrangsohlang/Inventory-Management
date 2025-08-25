# Inventory Management Function Documentation

This document explains how the functions in the `inventory` package support the project objectives of **inventory optimization**, **sales and purchase insights**, and **process improvement**. Metrics below were computed using the provided `Sample.zip` dataset.

## Dataset Utilities

### `load_datasets`
Loads CSV files from a ZIP archive into pandas DataFrames. It is the gateway for analysing the bundled sample data.

## Sales & Purchase Insights

### `top_selling_products` / `top_selling_from_zip`
Aggregates sales quantities to highlight best sellers. When applied to `SalesFINAL12312016_sample.csv`, the top products are:

| InventoryId | total_quantity |
|-------------|----------------|
| 53_HILLFAR_5952 | 120 |
| 41_LARNWICK_3606 | 48 |
| 66_EANVERNESS_6650 | 47 |

These figures help identify products driving revenue.

## Inventory Optimization

### `classify_inventory`
Performs ABC analysis by ranking items on cumulative value. Using `EndInvFINAL12312016_sample.csv` with value computed as `onHand * Price` produced:

- A: 409 items
- B: 319 items
- C: 272 items

This categorisation focuses management effort on high-value stock.

### `forecast_demand`
Employs Holt-Winters exponential smoothing to project future demand. Aggregated daily sales from the sample data yielded the following seven-day forecast:

```
2016-03-01    3.75
2016-03-02    2.89
2016-03-03    2.04
2016-03-04    1.18
2016-03-05    0.32
2016-03-06   -0.53
2016-03-07   -1.39
```

Forecasts guide procurement and production planning.

### `calculate_eoq`
Applies the economic order quantity formula. With total demand of 2,497 units, an order cost of 50, and holding cost of 2, the optimal order size is **353.34** units, balancing ordering and holding expenses.

### `compute_lead_times`
Determines the number of days between purchase orders and receipts. For `PurchasesFINAL12312016_sample.csv` the average lead time was **7.576** days, aiding suppliers and scheduling analysis.

### `calculate_reorder_point`
Combines average daily demand with lead time and safety stock to signal when to restock. Using an average daily demand of 41.62 units, the 7.576‑day lead time, and a safety stock of 10 units gives a reorder point of **325.29** units.

---
These functions collectively enable forecasting demand, prioritising inventory, optimising order quantities, monitoring supplier performance, and understanding sales trends, supporting the goals of improved inventory management and operational efficiency.
