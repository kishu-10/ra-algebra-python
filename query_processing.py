from relational_algebra import (
    intersect_operation,
    join_operation,
    select_operation,
    project_operation,
    difference_operation,
    union_operation,
    cross_product,
    natural_join,
)


def extract_subquery(query):
    """Extract the innermost subquery within parentheses."""
    start = query.find("(")
    end = query.rfind(")")
    if start == -1 or end == -1:
        raise ValueError(f"Malformed query: {query}")
    return query[start + 1 : end]


def extract_join_attributes(join_condition, join_operation):
    """Extracts the join attributes from a JOIN condition string in the format 'JOIN_{attr1=attr2}'."""
    condition = join_condition[join_condition.find("{") + 1 : join_condition.find("}")]
    attribute1, attribute2 = map(str.strip, condition.split(join_operation))
    return attribute1, attribute2


def contains_set_operation(query):
    """Check if the query contains set operations (Union, Difference, or Intersection) and split accordingly."""
    if any(char in query for char in ["-", "U", "INTE"]):
        present_chars = [char for char in ["-", "U", "INTE"] if char in query]
        queries = query.split(present_chars[0])
        return True, queries
    return False, None


def handle_subqueries(query, data):
    """Recursively process nested queries."""
    query = query.strip()

    # Check for set operations first
    if contains_set_operation(query)[0]:
        left_query, right_query = map(str.strip, contains_set_operation(query)[1])
        if " - " in query:
            return difference_operation(
                handle_subqueries(left_query, data),
                handle_subqueries(right_query, data),
            )
        elif " U " in query:
            return union_operation(
                handle_subqueries(left_query, data),
                handle_subqueries(right_query, data),
            )
        elif " INTE " in query:
            return intersect_operation(
                handle_subqueries(left_query, data),
                handle_subqueries(right_query, data),
            )

    # To remove opening and closing bracket
    if query.startswith("("):
        query = query.strip("(")[:-1]

    # Handle SELECT operation
    if query.startswith("SELE"):
        condition = query[query.find("{") + 1 : query.find("}")]

        if ">" in condition:
            attribute, value = condition.split(">")
            comparison = ">"
        elif "<" in condition:
            attribute, value = condition.split("<")
            comparison = "<"
        elif "=" in condition:
            attribute, value = condition.split("=")
            comparison = "="
        else:
            raise ValueError("Invalid comparison operator")

        attribute = attribute.strip()
        value = value.strip()
        sub_query = extract_subquery(query)
        table_name = sub_query.strip(")")
        return select_operation(data[table_name], attribute, comparison, value)

    # Handle PROJECT operation
    if query.startswith("PROJ"):
        attributes = query[query.find("{") + 1 : query.find("}")]
        sub_query = extract_subquery(query)
        result = handle_subqueries(sub_query, data)
        return project_operation(result, attributes.split(","))

    # Handle CROSS PRODUCT
    if " X " in query:
        left_table_name, right_table_name = map(str.strip, query.split(" X "))
        return cross_product(data[left_table_name], data[right_table_name])

    # Handle JOIN operation
    if "JOIN" in query:
        parts = query.split("(")
        sub_query = extract_subquery(query)
        left_table_name = sub_query.split(",")[0].strip()
        right_table_name = sub_query.split(",")[-1].strip()

        join_condition = parts[0].split()[0]

        if ">" in join_condition:
            attribute1, attribute2 = extract_join_attributes(join_condition, ">")
            comparison = ">"
        elif "<" in join_condition:
            attribute1, attribute2 = extract_join_attributes(join_condition, "<")
            comparison = "<"
        elif "=" in join_condition:
            attribute1, attribute2 = extract_join_attributes(join_condition, "=")
            comparison = "="
        else:
            raise ValueError("Invalid comparison operator")

        attribute1 = attribute1.strip()
        attribute2 = attribute2.strip()

        return join_operation(
            data[left_table_name],
            data[right_table_name],
            attribute1,
            attribute2,
            comparison,
        )

    # Handle NATURAL JOIN
    if "*" in query:
        left_table_name, right_table_name = map(str.strip, query.split("*"))
        return natural_join(data[left_table_name], data[right_table_name])

    raise ValueError(f"Unrecognized query format: {query}")
