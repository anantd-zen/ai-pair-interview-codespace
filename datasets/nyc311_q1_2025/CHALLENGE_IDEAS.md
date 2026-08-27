# SQL pairing ideas

## Operational analytics

- Compare median and p90 resolution time by agency and problem.
- Measure SLA performance without treating missing due dates as failures.
- Find problems with deteriorating weekly resolution time.
- Build a backlog-aging report as of the end of each week.
- Compare channel mix and closure performance across boroughs.

## Event-shaped analytics

- Reconstruct request state at a supplied timestamp.
- Detect impossible ordering such as closure before creation.
- Make an event projection idempotent when duplicate rows arrive.
- Find requests whose resolution update occurred after closure.
- Calculate elapsed time between lifecycle events with window functions.

## Data quality and anomaly work

- Identify spatial-temporal complaint bursts using rounded coordinates.
- Find likely duplicate requests without relying on exact addresses.
- Quantify missingness by agency and request category.
- Explain why a naive average resolution time is biased by still-open requests.
- Compare request volume with distinct geographic cells to avoid hotspot distortion.

