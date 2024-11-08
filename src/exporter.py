import pandas as pd
from todoist_api_python.api import TodoistAPI
import json
import argparse
import os
import logging
import sys
from typing import Optional

class TodoistExporter:
    """Exports data from Todoist into CSV files for projects, tasks, labels, sections, and comments."""

    def __init__(self, token: str, output_dir: Optional[str] = "data"):
        self.api = TodoistAPI(token)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)  # Create the output directory if it doesn't exist
        logging.info(f"Data will be exported to directory: {self.output_dir}")

    def export_projects(self) -> None:
        """Exports all projects to a CSV file."""
        try:
            projects = self.api.get_projects()
            project_data = [p.__dict__ for p in projects]
            pd.DataFrame(project_data).to_csv(f"{self.output_dir}/projects.csv", index=False)
            logging.info("Projects exported successfully.")
        except Exception as e:
            logging.error(f"Error exporting projects: {e}")

    def export_tasks(self, completed: bool = False) -> None:
        """Exports all tasks (completed or active) to a CSV file."""
        try:
            tasks = self.api.get_tasks() if not completed else self.api.get_completed_items()
            task_data = [t.__dict__ for t in tasks]
            filename = f"{self.output_dir}/tasks.csv" if not completed else f"{self.output_dir}/tasks_completed.csv"
            pd.DataFrame(task_data).to_csv(filename, index=False)
            logging.info(f"Tasks ({'completed' if completed else 'active'}) exported successfully.")
        except Exception as e:
            logging.error(f"Error exporting tasks: {e}")

    def export_labels(self) -> None:
        """Exports all labels to a CSV file."""
        try:
            labels = self.api.get_labels()
            label_data = [l.__dict__ for l in labels]
            pd.DataFrame(label_data).to_csv(f"{self.output_dir}/labels.csv", index=False)
            logging.info("Labels exported successfully.")
        except Exception as e:
            logging.error(f"Error exporting labels: {e}")

    def export_sections(self) -> None:
        """Exports all sections to a CSV file."""
        try:
            projects = self.api.get_projects()
            all_sections = []
            for project in projects:
                sections = self.api.get_sections(project_id=project.id)
                section_data = [s.__dict__ for s in sections]
                all_sections.extend(section_data)
            pd.DataFrame(all_sections).to_csv(f"{self.output_dir}/sections.csv", index=False)
            logging.info("Sections exported successfully.")
        except Exception as e:
            logging.error(f"Error exporting sections: {e}")

    def export_comments(self) -> None:
        """Exports all comments for tasks to a CSV file."""
        try:
            tasks = self.api.get_tasks()
            all_comments = []
            for task in tasks:
                comments = self.api.get_comments(task_id=task.id)
                comment_data = [c.__dict__ for c in comments]
                all_comments.extend(comment_data)
            pd.DataFrame(all_comments).to_csv(f"{self.output_dir}/comments.csv", index=False)
            logging.info("Comments exported successfully.")
        except Exception as e:
            logging.error(f"Error exporting comments: {e}")

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    # Load API token from config.json
    try:
        with open("config.json") as f:
            config = json.load(f)
        token = config["TOKEN"]
    except (FileNotFoundError, KeyError) as e:
        logging.critical("config.json file not found or missing TOKEN entry.")
        sys.exit(1)

    # Set up command-line arguments
    parser = argparse.ArgumentParser(description="Export Todoist data to CSV files.")
    parser.add_argument("--projects", action="store_true", help="Export projects")
    parser.add_argument("--tasks", action="store_true", help="Export active tasks")
    parser.add_argument("--completed_tasks", action="store_true", help="Export completed tasks")
    parser.add_argument("--labels", action="store_true", help="Export labels")
    parser.add_argument("--sections", action="store_true", help="Export sections")
    parser.add_argument("--comments", action="store_true", help="Export comments")
    parser.add_argument("--all", action="store_true", help="Export all data types")
    parser.add_argument("--output_dir", type=str, default="data", help="Directory to save CSV files")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # Set verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize exporter with output directory
    exporter = TodoistExporter(token, output_dir=args.output_dir)

    # Execute exports based on arguments
    if args.all:
        exporter.export_projects()
        exporter.export_tasks(completed=False)
        exporter.export_tasks(completed=True)
        exporter.export_labels()
        exporter.export_sections()
        exporter.export_comments()
    else:
        if args.projects:
            exporter.export_projects()
        if args.tasks:
            exporter.export_tasks(completed=False)
        if args.completed_tasks:
            exporter.export_tasks(completed=True)
        if args.labels:
            exporter.export_labels()
        if args.sections:
            exporter.export_sections()
        if args.comments:
            exporter.export_comments()

    # If no specific arguments are given, export everything by default
    if not any(vars(args).values()):
        logging.info("No specific export flags provided, exporting all data.")
        exporter.export_projects()
        exporter.export_tasks(completed=False)
        exporter.export_tasks(completed=True)
        exporter.export_labels()
        exporter.export_sections()
        exporter.export_comments()

if __name__ == "__main__":
    main()