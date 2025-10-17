# **Unit 1 Summary** — Arman Hyder

## Discover: Identifying Key Performance Indicators and Trends

Our initial discovery phase focused on identifying the most critical Key Performance Indicators (KPIs) for The Look: eCommerce. We pinpointed three primary metrics: **Monthly Revenue**, **Average Order Value (AOV)**, and **90-day Repeat Purchase Rate**. These KPIs were chosen because they offer a holistic view of business health, covering sales volume, customer spending habits, and customer loyalty. Our analysis of monthly revenue trends clearly revealed seasonal patterns, which is crucial for forecasting and inventory management. We utilized sophisticated SQL window functions to accurately compute both Month-over-Month (MoM) and Year-over-Year (YoY) growth rates for these KPIs, providing a detailed understanding of performance fluctuations and long-term trajectories.

## Investigate: Deep Dive into Specific Segments and Drivers

For a focused investigation, we selected **'Womens Dresses'** as our deep-dive product category and defined our customer segment as **'gender \= F' (Female customers)**. This allowed us to narrow our scope and uncover specific drivers influencing sales within this important segment. Our findings indicated a strong correlation between regions with higher revenue and those exhibiting a higher average discount percentage, suggesting that price elasticity plays a significant role in these markets for 'Womens Dresses' among female customers. Furthermore, our initial observations suggested robust performance from mobile traffic, although we recognized the need for further validation using median-based checks to account for potential outlier bias.

## Validate: Cross-Checking Insights for Accuracy

Recognizing the potential for misleading insights from aggregated data, we performed two key validation exercises:

1. **Device AOV (Mean vs. Median):** Our initial analysis using the mean AOV suggested a significant advantage for mobile devices. However, a deeper look using the median AOV revealed that this perceived advantage was largely overstated due to outliers. The median-based analysis provided a more accurate representation, demonstrating that while mobile performance is strong, the **mean-based insight was misleading** and needed correction for strategic decision-making.  
2. **Regional Effect (Category-Mix Normalization):** We observed that certain countries appeared to outperform others in terms of raw revenue. To ensure this wasn't an artifact of product mix, we applied category-mix normalization. This validation step revealed that some prior top-ranking regions were benefiting from an unusually high proportion of sales from premium product categories. After normalization, the **country rankings shifted**, providing a truer reflection of regional performance independent of category composition. This highlights the importance of accounting for underlying factors to avoid drawing incorrect conclusions.

## Extend: Enhancing Data Communication and Accessibility

To extend our analytical capabilities and improve communication of insights, we developed two key tools:

1. **Interactive Plotly Chart:** We created an interactive Plotly time series chart that visualizes monthly revenue alongside toggles for both MoM and YoY growth rates. This dynamic visualization allows stakeholders to explore trends and growth figures with ease, fostering a more intuitive understanding of performance.  
2. **Executive Looker Studio Dashboard:** We designed an executive dashboard in Looker Studio, incorporating essential business metrics. This dashboard includes a **scorecard displaying revenue for the last 30 days**, a **donut chart illustrating sales percentage by region**, and a **bar chart showcasing the top 5 product categories by revenue**. This dashboard provides a clear, high-level overview for leadership, enabling quick access to critical business information.

## Recommendations: Actionable Strategies for Growth

Based on our comprehensive analysis, we propose the following actionable recommendations for The Look: eCommerce:

1. **Strategic Focus on 'Womens Dresses' with Controlled Discounting:** We recommend focusing marketing and inventory efforts for 'Womens Dresses' in the identified top-performing regions. Within these regions, it is crucial to implement **controlled discounting strategies**, carefully monitoring their impact on profitability rather than solely revenue. Simultaneously, increasing mobile-focused marketing spend in these regions is advised, given the strong, albeit more nuanced, mobile performance. Crucially, all performance tracking for this category should emphasize the **median Average Order Value** to gain a more accurate understanding of customer spending habits, free from outlier influence.  
2. **Data-Driven Resource Allocation through Normalized KPIs:** To optimize resource allocation and avoid missteps, we strongly advise using **mix-normalized regional KPIs** for guiding budget distribution and inventory management. This approach ensures that capital is allocated based on genuine regional performance, rather than skewed by product category mix. This analysis should be **revisited monthly** to adapt to evolving market dynamics and maintain agility in our operational strategies.

