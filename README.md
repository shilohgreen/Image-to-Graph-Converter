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

## Standardized Data Format (Library-Agnostic)

A universal format designed to be:
1. **Minimal** — Contains only essential data
2. **SQL-friendly** — Flat structure, JSONB-compatible
3. **Adaptable** — Easily transforms to any chart library

### The Universal Chart Data Schema

```json
{
  "meta": {
    "title": "Chart Title",
    "type": "bar|line|pie|scatter|area",
    "xAxis": { "label": "X Axis Label", "type": "category|number|date" },
    "yAxis": { "label": "Y Axis Label", "unit": "optional unit" }
  },
  "series": [
    { "key": "seriesKey1", "label": "Series 1 Display Name" },
    { "key": "seriesKey2", "label": "Series 2 Display Name" }
  ],
  "data": [
    { "x": "Category1", "seriesKey1": 100, "seriesKey2": 200 },
    { "x": "Category2", "seriesKey1": 150, "seriesKey2": 180 }
  ]
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `meta.title` | string | Yes | Chart title |
| `meta.type` | string | Yes | Chart type hint |
| `meta.xAxis.label` | string | No | X-axis display label |
| `meta.xAxis.type` | string | No | `category`, `number`, or `date` |
| `meta.yAxis.label` | string | No | Y-axis display label |
| `meta.yAxis.unit` | string | No | Unit suffix (e.g., "seconds", "$") |
| `series[]` | array | Yes | Series definitions |
| `series[].key` | string | Yes | Key matching data columns |
| `series[].label` | string | Yes | Display name for legend |
| `data[]` | array | Yes | Row-oriented data points |
| `data[].x` | string/number | Yes | X-axis value (category or numeric) |
| `data[].<seriesKey>` | number | Yes | Y-value for each series |

---

### Example: Grouped Bar Chart (1H.jpg - Lap Timings)

**Extracted data:**
```json
{
  "meta": {
    "title": "Lap timings for Aman, Ben and Cavin",
    "type": "bar",
    "xAxis": { "label": "Lap", "type": "category" },
    "yAxis": { "label": "Timings", "unit": "seconds" }
  },
  "series": [
    { "key": "aman", "label": "Aman" },
    { "key": "ben", "label": "Ben" },
    { "key": "cavin", "label": "Cavin" }
  ],
  "data": [
    { "x": "Lap 1", "aman": 58, "ben": 58, "cavin": 58 },
    { "x": "Lap 2", "aman": 59, "ben": 59, "cavin": 59 },
    { "x": "Lap 3", "aman": 60, "ben": 60, "cavin": 60 },
    { "x": "Lap 4", "aman": 90, "ben": 61, "cavin": 75 }
  ]
}
```

### Example: Table Data (1E.jpg - Step Counts)

**Extracted data:**
```json
{
  "meta": {
    "title": "Kai's step counts over two days",
    "type": "bar",
    "xAxis": { "label": "Period", "type": "category" },
    "yAxis": { "label": "Steps", "unit": "" }
  },
  "series": [
    { "key": "dayA", "label": "Day A" },
    { "key": "dayB", "label": "Day B" }
  ],
  "data": [
    { "x": "Period 1", "dayA": 6, "dayB": 6 },
    { "x": "Period 2", "dayA": 7, "dayB": 7 },
    { "x": "Period 3", "dayA": 7, "dayB": 7 },
    { "x": "Period 4", "dayA": 30, "dayB": 8 }
  ]
}
```

---

## Transformations to Chart Libraries

### → Recharts

```javascript
// Direct usage - data array is already compatible
<BarChart data={chartData.data}>
  <XAxis dataKey="x" label={chartData.meta.xAxis.label} />
  <YAxis label={chartData.meta.yAxis.label} />
  {chartData.series.map(s => (
    <Bar key={s.key} dataKey={s.key} name={s.label} />
  ))}
</BarChart>
```

### → MUI X Charts

```javascript
// Map to MUI X format
const muiProps = {
  dataset: chartData.data,
  xAxis: [{ scaleType: 'band', dataKey: 'x', label: chartData.meta.xAxis.label }],
  series: chartData.series.map(s => ({ dataKey: s.key, label: s.label })),
};
<BarChart {...muiProps} />
```

### → Chart.js

```javascript
// Transform to Chart.js column-oriented format
const chartJsData = {
  labels: chartData.data.map(d => d.x),
  datasets: chartData.series.map(s => ({
    label: s.label,
    data: chartData.data.map(d => d[s.key]),
  })),
};
```

---

## SQL Schema (PostgreSQL)

```sql
CREATE TABLE charts (
  id          SERIAL PRIMARY KEY,
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  source_file VARCHAR(255),
  meta        JSONB NOT NULL,      -- { title, type, xAxis, yAxis }
  series      JSONB NOT NULL,      -- [{ key, label }, ...]
  data        JSONB NOT NULL       -- [{ x, ...seriesValues }, ...]
);

-- Index for querying by chart type
CREATE INDEX idx_charts_type ON charts ((meta->>'type'));

-- Example insert
INSERT INTO charts (source_file, meta, series, data) VALUES (
  '1H.jpg',
  '{"title": "Lap timings", "type": "bar", "xAxis": {"label": "Lap"}, "yAxis": {"label": "Timings", "unit": "seconds"}}',
  '[{"key": "aman", "label": "Aman"}, {"key": "ben", "label": "Ben"}]',
  '[{"x": "Lap 1", "aman": 58, "ben": 58}]'
);
```

---

## Data Structure Enforcement Policies

PostgreSQL constraints and triggers to enforce the schema at the database level.

### 1. Basic Structure CHECK Constraints

```sql
-- Enforce meta structure
ALTER TABLE charts ADD CONSTRAINT chk_meta_structure CHECK (
  jsonb_typeof(meta) = 'object' AND
  meta ? 'title' AND
  jsonb_typeof(meta->'title') = 'string' AND
  meta ? 'type' AND
  jsonb_typeof(meta->'type') = 'string' AND
  meta->>'type' IN ('bar', 'line', 'pie', 'scatter', 'area') AND
  (NOT (meta ? 'xAxis') OR jsonb_typeof(meta->'xAxis') = 'object') AND
  (NOT (meta ? 'yAxis') OR jsonb_typeof(meta->'yAxis') = 'object')
);

-- Enforce series array structure
ALTER TABLE charts ADD CONSTRAINT chk_series_structure CHECK (
  jsonb_typeof(series) = 'array' AND
  jsonb_array_length(series) > 0 AND
  -- Each series item must be an object with 'key' and 'label'
  (SELECT bool_and(
    jsonb_typeof(elem) = 'object' AND
    elem ? 'key' AND
    jsonb_typeof(elem->'key') = 'string' AND
    elem ? 'label' AND
    jsonb_typeof(elem->'label') = 'string'
  ) FROM jsonb_array_elements(series) AS elem)
);

-- Enforce data array structure
ALTER TABLE charts ADD CONSTRAINT chk_data_structure CHECK (
  jsonb_typeof(data) = 'array' AND
  jsonb_array_length(data) > 0 AND
  -- Each data item must be an object with 'x'
  (SELECT bool_and(
    jsonb_typeof(elem) = 'object' AND
    elem ? 'x'
  ) FROM jsonb_array_elements(data) AS elem)
);
```

### 2. Cross-Reference Validation Function

Validates that series keys referenced in `data` match `series` definitions:

```sql
CREATE OR REPLACE FUNCTION validate_chart_data()
RETURNS TRIGGER AS $$
DECLARE
  series_keys TEXT[];
  data_keys TEXT[];
  missing_key TEXT;
BEGIN
  -- Extract all series keys
  SELECT ARRAY_AGG(elem->>'key')
  INTO series_keys
  FROM jsonb_array_elements(NEW.series) AS elem;
  
  -- Extract all keys from first data row (excluding 'x')
  SELECT ARRAY_AGG(key)
  INTO data_keys
  FROM jsonb_each((SELECT elem FROM jsonb_array_elements(NEW.data) AS elem LIMIT 1))
  WHERE key != 'x';
  
  -- Check that all data keys exist in series
  IF data_keys IS NOT NULL THEN
    FOREACH missing_key IN ARRAY data_keys
    LOOP
      IF NOT (missing_key = ANY(series_keys)) THEN
        RAISE EXCEPTION 'Data key "%" not found in series definitions', missing_key;
      END IF;
    END LOOP;
  END IF;
  
  -- Check that all series keys appear in data (at least one row)
  IF series_keys IS NOT NULL THEN
    FOREACH missing_key IN ARRAY series_keys
    LOOP
      IF NOT EXISTS (
        SELECT 1
        FROM jsonb_array_elements(NEW.data) AS row
        WHERE row ? missing_key
      ) THEN
        RAISE EXCEPTION 'Series key "%" not found in any data row', missing_key;
      END IF;
    END LOOP;
  END IF;
  
  -- Validate that all data rows have same keys (excluding 'x')
  IF EXISTS (
    SELECT 1
    FROM (
      SELECT jsonb_object_keys(elem) - 'x' AS keys
      FROM jsonb_array_elements(NEW.data) AS elem
    ) AS row_keys
    GROUP BY keys
    HAVING COUNT(*) < (SELECT COUNT(*) FROM jsonb_array_elements(NEW.data))
  ) THEN
    RAISE EXCEPTION 'All data rows must have the same series keys';
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### 3. Trigger to Enforce Validation

```sql
CREATE TRIGGER trigger_validate_chart_data
  BEFORE INSERT OR UPDATE ON charts
  FOR EACH ROW
  EXECUTE FUNCTION validate_chart_data();
```

### 4. Additional Type-Specific Validations

```sql
-- Ensure numeric values in data rows (for series keys)
CREATE OR REPLACE FUNCTION validate_numeric_series()
RETURNS TRIGGER AS $$
DECLARE
  series_key TEXT;
  data_row JSONB;
  value JSONB;
BEGIN
  -- For each series key, validate all values are numeric
  FOR series_key IN
    SELECT elem->>'key' FROM jsonb_array_elements(NEW.series) AS elem
  LOOP
    FOR data_row IN
      SELECT elem FROM jsonb_array_elements(NEW.data) AS elem
    LOOP
      IF data_row ? series_key THEN
        value := data_row->series_key;
        IF jsonb_typeof(value) NOT IN ('number', 'null') THEN
          RAISE EXCEPTION 'Series "%" contains non-numeric value: %', series_key, value;
        END IF;
      END IF;
    END LOOP;
  END LOOP;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validate_numeric_series
  BEFORE INSERT OR UPDATE ON charts
  FOR EACH ROW
  EXECUTE FUNCTION validate_numeric_series();
```

### 5. Validation Summary

| Policy Type | What It Enforces | Example Rejection |
|-------------|------------------|-------------------|
| **CHECK: meta structure** | Required `title` (string), `type` (enum), optional `xAxis`/`yAxis` (objects) | `{"type": "bar"}` (missing title) |
| **CHECK: series structure** | Array of objects, each with `key` (string) and `label` (string) | `[{"key": "sales"}]` (missing label) |
| **CHECK: data structure** | Array of objects, each with `x` key | `[{"sales": 100}]` (missing x) |
| **TRIGGER: cross-reference** | All data keys exist in series, all series keys appear in data | Data has `"sales"` but series only defines `"revenue"` |
| **TRIGGER: numeric values** | All series values are numbers (or null) | `{"x": "Jan", "sales": "N/A"}` |
| **TRIGGER: consistent keys** | All data rows have same series keys | Row 1 has `{x, sales}`, Row 2 has `{x, revenue}` |

### 6. Testing the Policies

```sql
-- ✅ Valid insert (passes all checks)
INSERT INTO charts (meta, series, data) VALUES (
  '{"title": "Sales", "type": "bar"}',
  '[{"key": "sales", "label": "Sales"}]',
  '[{"x": "Jan", "sales": 100}]'
);

-- ❌ Rejected: missing title
INSERT INTO charts (meta, series, data) VALUES (
  '{"type": "bar"}',
  '[{"key": "sales", "label": "Sales"}]',
  '[{"x": "Jan", "sales": 100}]'
);
-- ERROR: new row for relation "charts" violates check constraint "chk_meta_structure"

-- ❌ Rejected: series key mismatch
INSERT INTO charts (meta, series, data) VALUES (
  '{"title": "Sales", "type": "bar"}',
  '[{"key": "revenue", "label": "Revenue"}]',
  '[{"x": "Jan", "sales": 100}]'
);
-- ERROR: Data key "sales" not found in series definitions

-- ❌ Rejected: non-numeric value
INSERT INTO charts (meta, series, data) VALUES (
  '{"title": "Sales", "type": "bar"}',
  '[{"key": "sales", "label": "Sales"}]',
  '[{"x": "Jan", "sales": "N/A"}]'
);
-- ERROR: Series "sales" contains non-numeric value: "N/A"
```

---

