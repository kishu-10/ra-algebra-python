from file_operations import (
    read_csv,
    write_output,
    write_shortened_output,
    remove_file_if_exists,
)
from query_processing import handle_subqueries


def process_queries():
    """Main function to process queries from RAqueries.txt."""
    data = {
        "ACTORS": read_csv("ACTORS.csv"),
        "MOVIES": read_csv("MOVIES.csv"),
        "PAY": read_csv("PAY.csv"),
    }

    output_file = "RAoutput.csv"
    remove_file_if_exists(output_file)

    with open("RAqueries.txt", "r") as query_file:
        queries = query_file.readlines()

    for query in map(str.strip, queries):
        if not query:
            continue
        try:
            print(f"Processing query: {query}")
            results = handle_subqueries(query, data)
            write_output(output_file, results, query)
            write_shortened_output(output_file, results, query)
        except Exception as e:
            print(f"Error processing query '{query}': {e}")

    print(f"Processing complete. Results written to {output_file}.")


process_queries()
