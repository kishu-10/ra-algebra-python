import csv
import os


def read_csv(file_name):
    """Reads a CSV file and returns a list of dictionaries representing the rows."""
    with open(file_name, "r") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def write_output(file_name, results, query):
    """Writes the output of a query to a CSV file."""
    with open(file_name, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([f"Query: {query}"])
        if results:
            writer.writerow(results[0].keys())
            writer.writerows([row.values() for row in results])
        writer.writerow([])


def write_shortened_output(file_name, results, query):
    """Writes the first 3 lines of the output for a query."""
    with open(file_name, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([f"Query: {query} (Shortened)"])
        if results:
            writer.writerow(results[0].keys())
            writer.writerows([row.values() for row in results[:3]])
        writer.writerow([])


def remove_file_if_exists(file_name):
    """Removes the file if it exists."""
    if os.path.exists(file_name):
        os.remove(file_name)
