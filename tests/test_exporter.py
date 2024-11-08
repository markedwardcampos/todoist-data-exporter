import unittest
import os
from todoist_api_python.api import TodoistAPI
from exporter import TodoistExporter
from unittest.mock import patch, MagicMock

class TestTodoistExporter(unittest.TestCase):
    @patch("todoist_api_python.api.TodoistAPI")
    def setUp(self, MockAPI):
        # Mock Todoist API to avoid real API calls
        self.mock_api = MockAPI()
        self.exporter = TodoistExporter(token="mock-token", output_dir="test_data")
        
        # Mock return values for the API methods
        self.mock_api.get_projects.return_value = [
            MagicMock(id="123", name="Test Project")
        ]
        self.mock_api.get_tasks.return_value = [
            MagicMock(id="1", content="Test Task", project_id="123")
        ]
        self.mock_api.get_completed_items.return_value = [
            MagicMock(id="2", content="Completed Task", project_id="123")
        ]
        self.mock_api.get_labels.return_value = [
            MagicMock(id="1", name="Test Label")
        ]
        self.mock_api.get_sections.return_value = [
            MagicMock(id="1", name="Test Section", project_id="123")
        ]
        self.mock_api.get_comments.return_value = [
            MagicMock(id="1", content="Test Comment", task_id="1")
        ]

    def test_export_projects(self):
        """Test exporting projects to CSV."""
        self.exporter.export_projects()
        self.assertTrue(os.path.exists("test_data/projects.csv"))

    def test_export_tasks(self):
        """Test exporting active tasks to CSV."""
        self.exporter.export_tasks(completed=False)
        self.assertTrue(os.path.exists("test_data/tasks.csv"))

    def test_export_completed_tasks(self):
        """Test exporting completed tasks to CSV."""
        self.exporter.export_tasks(completed=True)
        self.assertTrue(os.path.exists("test_data/tasks_completed.csv"))

    def test_export_labels(self):
        """Test exporting labels to CSV."""
        self.exporter.export_labels()
        self.assertTrue(os.path.exists("test_data/labels.csv"))

    def test_export_sections(self):
        """Test exporting sections to CSV."""
        self.exporter.export_sections()
        self.assertTrue(os.path.exists("test_data/sections.csv"))

    def test_export_comments(self):
        """Test exporting comments to CSV."""
        self.exporter.export_comments()
        self.assertTrue(os.path.exists("test_data/comments.csv"))

    def tearDown(self):
        """Cleanup test files."""
        for filename in os.listdir("test_data"):
            file_path = os.path.join("test_data", filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)

if __name__ == "__main__":
    unittest.main()