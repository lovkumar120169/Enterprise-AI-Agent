def build_metadata_filter(
    department: str | None = None,
    country: str | None = None,
    year: int | None = None
) -> dict | None:

    filters = []

    if department:

        filters.append(
            {
                "equals": {
                    "key": "department",
                    "value": department
                }
            }
        )

    if country:

        filters.append(
            {
                "equals": {
                    "key": "country",
                    "value": country
                }
            }
        )

    if year:

        filters.append(
            {
                "equals": {
                    "key": "year",
                    "value": year
                }
            }
        )

    if not filters:

        return None

    if len(filters) == 1:

        return filters[0]

    return {
        "andAll": filters
    }