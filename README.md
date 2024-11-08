
# Todoist Data Exporter

The **Todoist Data Exporter** is a Python script that exports data from Todoist, including projects, tasks, labels, sections, and comments, into CSV files. This tool enables users to analyze and visualize their Todoist data independently.

## Features

- Exports **Projects** with metadata like project names, IDs, and colors.
- Exports **Tasks** (both active and completed) with details like content, due dates, labels, and project association.
- Exports **Labels** created in Todoist.
- Exports **Sections** within projects.
- Exports **Comments** associated with tasks and projects.

## Installation

### Prerequisites

- Python 3.7 or above
- A Todoist API token (obtainable from your Todoist account under **Settings > Integrations**)

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/todoist-data-exporter.git
   cd todoist-data-exporter
   ```

2. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API token**:

   - Create a `config.json` file in the project root with your Todoist API token:

   ```json
   {
     "TOKEN": "your_todoist_api_token_here"
   }
   ```

## Usage

Run the exporter script to export data to CSV files:

```bash
python src/exporter.py
```

This will generate CSV files in the default `data` directory:

- `projects.csv` – list of all projects
- `tasks.csv` – list of all active tasks
- `tasks_completed.csv` – list of completed tasks
- `labels.csv` – list of labels
- `sections.csv` – list of sections per project
- `comments.csv` – list of comments on tasks

### Optional Command-Line Arguments

You can specify which entities to export using command-line arguments. Here are some examples:

- Export only projects and tasks:

  ```bash
  python src/exporter.py --projects --tasks
  ```

- Export all entities with `--all` flag:

  ```bash
  python src/exporter.py --all
  ```

- Specify an output directory other than the default `data/`:

  ```bash
  python src/exporter.py --all --output_dir="custom_data"
  ```

- Enable verbose output for debugging:

  ```bash
  python src/exporter.py --all --verbose
  ```

Use `--help` for a full list of options:

```bash
python src/exporter.py --help
```

### Arguments Summary

- `--all`: Export all entities (projects, tasks, completed tasks, labels, sections, and comments).
- `--output_dir`: Specify a custom directory to save CSV files.
- `--projects`: Export only projects.
- `--tasks`: Export only active tasks.
- `--completed_tasks`: Export only completed tasks.
- `--labels`: Export only labels.
- `--sections`: Export only sections.
- `--comments`: Export only comments.
- `--verbose`: Enable detailed logging output.

## Development

### Testing

Run tests using `unittest` with the following command:

```bash
python -m unittest discover -s tests
```

This will create temporary CSV files in the `test_data` directory. Ensure `test_data` is listed in `.gitignore` to avoid committing test output files.

### Contributing

1. Fork this repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- Thanks to [Doist](https://doist.com/) for providing the [Todoist API](https://developer.todoist.com/).

## Contact

Feel free to contact me for questions or suggestions!
