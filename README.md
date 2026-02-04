# Image-to-Graph-Converter

Transform images into **chart-ready data structures** that can be rendered by common React chart libraries.

### README Report — Data Structures Needed (OCR → “Graph” → React Chart Components)

This report summarizes the **data structures** your OCR/extraction pipeline should output so the same extracted data can be rendered with:

- **Recharts**: [Recharts examples](https://recharts.github.io/en-US/examples/)
- **MUI X Charts**: [MUI X Charts](https://mui.com/x/react-charts/)
- **Chart.js**: [Chart.js bar docs](https://www.chartjs.org/docs/latest/charts/bar.html)

---

### What each charting library expects

#### Recharts (React components)
Recharts charts typically take:

- **`data`**: an array of objects (rows)
- **`XAxis dataKey`**: the property name for the x value inside each row
- **One component per series** (e.g. `<Line dataKey="sales" />`, `<Bar dataKey="uv" />`)

Conceptually, your extracted data should look like:
- `[{ name: 'Jan', sales: 4000, expenses: 2400 }, { name: 'Feb', ... }]`
- X-axis reads `name`
- Each series reads one numeric key (`sales`, `expenses`, etc.)

Reference: Recharts usage patterns in [Recharts examples](https://recharts.github.io/en-US/examples/).

#### MUI X Charts (React components)
MUI X Charts commonly uses:

- **`dataset`**: array of objects (rows)
- **`series`**: array of series descriptors with **`dataKey`** (points into each row)
- **`xAxis`**: array where you can set **`dataKey`** (points into each row); bar charts often use `scaleType: 'band'`

Conceptually:
- `dataset=[{ x: 1, y: 32 }, { x: 2, y: 41 }]`
- `xAxis={[{ dataKey: 'x' }]}`
- `series={[{ dataKey: 'y', label: 'Series A' }]}`

Reference: MUI X Charts docs: [MUI X Charts](https://mui.com/x/react-charts/).

#### Chart.js
Chart.js bar charts typically use:

- **`data.labels`**: array of x-axis labels
- **`data.datasets`**: array of series/datasets
- Each dataset has **`label`**, **`data`** (array aligned to `labels`), plus style fields

Conceptually:
- `labels = ['Jan', 'Feb', ...]`
- `datasets = [{ label: 'Sales', data: [4000, 3000, ...] }]`

Reference: [Chart.js bar docs](https://www.chartjs.org/docs/latest/charts/bar.html).

---
