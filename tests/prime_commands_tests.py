import unittest
import os
import shutil
from modules.prime_commands import update, Markdown

class TestLuhm(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.original_cwd = os.getcwd()
        self.test_dir = os.path.join(self.original_cwd, "test_dir")

        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

        os.chdir(self.test_dir)

        # Create sample markdown files with links
        self.file_one = os.path.join(self.test_dir, "file_one.md")
        self.file_two = os.path.join(self.test_dir, "file_two.md")
        self.file_three = os.path.join(self.test_dir, "file_three.md")

        with open(self.file_one, "w") as file_one:
            file_one.write("---\nFront links:\n---\n\n[link to file_two](./file_two.md)\n")

        with open(self.file_two, "w") as file_two:
            file_two.write("[link to file_one](./file_one.md)\n")

        with open(self.file_three, "w") as file_three:
            file_three.write("[link to file_one](./file_one.md)\n[link to file_two](./file_two.md)\n")

    def tearDown(self):
        # Remove the temporary directory after each test
        shutil.rmtree(self.test_dir)
        os.chdir(self.original_cwd)

    def test_update_metadata(self):
        # Run the update function
        markdowns = [Markdown(self.file_one), Markdown(self.file_two), Markdown(self.file_three)]
        update(markdowns)

        # Check if the metadata is updated correctly in the three files
        with open(self.file_one, "r") as file_one:
            content_one = file_one.read()
            self.assertIn("Front links", content_one)
            self.assertIn("Back links", content_one)

        with open(self.file_two, "r") as file_two:
            content_two = file_two.read()
            self.assertIn("Front links", content_two)
            self.assertIn("Back links", content_two)

        with open(self.file_three, "r") as file_three:
            content_three = file_three.read()
            self.assertIn("Front links", content_three)
            self.assertIn("Back links", content_three)


if __name__ == '__main__':
        unittest.main()
