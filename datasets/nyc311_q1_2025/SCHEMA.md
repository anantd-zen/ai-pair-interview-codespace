# Snapshot schema and source notes

## Requests

| Column | DuckDB type | Meaning |
|---|---|---|
| `request_id` | `VARCHAR` | NYC 311 public unique key. |
| `created_at` | `TIMESTAMP` | When the customer submitted the request. |
| `closed_at` | `TIMESTAMP` | When the responding agency closed it, if closed. |
| `agency` | `VARCHAR` | Responding agency acronym. |
| `agency_name` | `VARCHAR` | Responding agency or unit name. |
| `problem` | `VARCHAR` | Source `complaint_type`; currently displayed as Problem. |
| `problem_detail` | `VARCHAR` | Source `descriptor`; currently displayed as Problem Detail. |
| `additional_details` | `VARCHAR` | Additional request classification. |
| `location_type` | `VARCHAR` | General kind of location involved. |
| `incident_zip` | `VARCHAR` | ZIP code kept as an identifier, not a number. |
| `city` | `VARCHAR` | Geocoded city name. |
| `facility_type` | `VARCHAR` | Facility associated with the request, where applicable. |
| `status` | `VARCHAR` | Status visible when the snapshot was retrieved. |
| `due_at` | `TIMESTAMP` | Agency due timestamp, where supplied. |
| `resolution_description` | `VARCHAR` | Agency-provided resolution text. |
| `resolution_updated_at` | `TIMESTAMP` | Last published resolution-action update timestamp. |
| `community_board` | `VARCHAR` | Community-board designation. |
| `council_district` | `VARCHAR` | City Council district identifier. |
| `police_precinct` | `VARCHAR` | Police precinct identifier or label. |
| `bbl` | `VARCHAR` | Borough-block-lot property identifier. |
| `borough` | `VARCHAR` | Borough name. |
| `channel` | `VARCHAR` | How the request reached 311, such as mobile, phone, or web. |
| `park_facility_name` | `VARCHAR` | Park or facility name, where applicable. |
| `park_borough` | `VARCHAR` | Borough associated with a park request. |
| `vehicle_type` | `VARCHAR` | Vehicle category for relevant request types. |
| `taxi_company_borough` | `VARCHAR` | Taxi-company borough for relevant requests. |
| `bridge_highway_name` | `VARCHAR` | Bridge or highway for relevant requests. |
| `latitude_approx` | `DOUBLE` | Latitude rounded to three decimal places. |
| `longitude_approx` | `DOUBLE` | Longitude rounded to three decimal places. |
| `resolution_hours` | `DOUBLE` | Hours from creation to closure; null for open requests. |
| `closed_by_due_date` | `BOOLEAN` | Whether closure occurred by the supplied due timestamp. |

Exact street addresses, street and intersection names, landmarks, and taxi
pickup locations are deliberately omitted. Coordinates are rounded to roughly
neighborhood-block precision.

## Events

| Column | DuckDB type | Meaning |
|---|---|---|
| `event_id` | `VARCHAR` | Deterministic `request_id:event_type` identifier. |
| `request_id` | `VARCHAR` | Parent service request. |
| `event_type` | `VARCHAR` | `request_created`, `resolution_updated`, or `request_closed`. |
| `event_at` | `TIMESTAMP` | Timestamp supporting the derived event. |
| `agency` | `VARCHAR` | Responding agency. |
| `problem` | `VARCHAR` | Request problem category. |
| `problem_detail` | `VARCHAR` | Request problem detail. |
| `borough` | `VARCHAR` | Borough. |
| `status_after` | `VARCHAR` | Simplified projected state after the event. |
| `channel` | `VARCHAR` | Intake channel. |
| `payload` | `JSON` | Event-specific context retained as structured JSON. |

## Official dictionary caveats

The official workbook says:

- The dataset is published and changed daily, with roughly a one-day buffer.
- Expected values associated with fields are non-exhaustive.
- It contains service requests that can be directed to specific agencies, not all inquiries.
- Complaint counts measure reporting behavior, not objective conditions.
- Geocoded fields were added from request locations, and the complete list of geocoded fields could not be verified.
- NYCHA, Department of Correction, and other agencies with separate customer-service systems may be absent or incomplete.

The official workbook remains authoritative and is stored in `reference/`.

