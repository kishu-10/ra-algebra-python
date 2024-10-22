def distinct(relation):
    """Return distinct rows from the relation."""
    seen_rows = set()
    result = []
    for row in relation:
        row_tuple = tuple(row.items())
        if row_tuple not in seen_rows:
            result.append(row)
            seen_rows.add(row_tuple)
    return result


def select_operation(relation, attribute, comparison, value):
    """SELECT operation"""
    result = []
    for row in relation:
        if comparison == ">":
            if float(row[attribute]) > float(value):
                result.append(row)
        elif comparison == "<":
            if float(row[attribute]) < float(value):
                result.append(row)
        elif comparison == "=":
            if (
                str(row[attribute]).strip() == str(value).strip("'").strip()
                if "'" in str(value)
                else str(row[attribute]).strip() == str(value).strip()
            ):
                result.append(row)
    return result


def project_operation(relation, attributes):
    """PROJECT operation: keep only specified columns (attributes)"""
    result = []
    for row in relation:
        projected_row = {attr: row[attr] for attr in attributes}
        result.append(projected_row)
    return distinct(result)


def cross_product(relation1, relation2):
    """CROSS PRODUCT operation: combine every row of the first table with every row of the second table"""
    result = []
    for row1 in relation1:
        for row2 in relation2:
            combined_row = row1.copy()
            combined_row.update(row2)
            result.append(combined_row)
    return result


def join_operation(relation1, relation2, attr1, attr2, comparison):
    """JOIN operation: combine rows from two tables where a condition between attributes is met"""
    result = []
    for row1 in relation1:
        for row2 in relation2:
            if comparison == "=" and row1[attr1] == row2[attr2]:
                combined_row = row1.copy()
                combined_row.update(row2)
                result.append(combined_row)
    return result


def natural_join(relation1, relation2):
    """NATURAL JOIN operation: combine rows from two tables where all common attributes match"""
    result = []
    common_attributes = set(relation1[0].keys()) & set(relation2[0].keys())
    for row1 in relation1:
        for row2 in relation2:
            if all(row1[attr] == row2[attr] for attr in common_attributes):
                combined_row = row1.copy()
                combined_row.update(row2)
                result.append(combined_row)
    return result


def union_operation(left_relation, right_relation):
    """UNION operation: combine rows from two tables, ensuring no duplicates"""
    result = left_relation + right_relation
    return distinct(result)


def intersect_operation(left_relation, right_relation):
    """INTERSECT operation: find common rows between two tables"""
    result = []
    for row in left_relation:
        if row in right_relation:
            result.append(row)
    return result


def difference_operation(left_relation, right_relation):
    """DIFFERENCE operation: find rows in the first table that are not in the second"""
    result = []
    for row in left_relation:
        if row not in right_relation:
            result.append(row)
    return result
