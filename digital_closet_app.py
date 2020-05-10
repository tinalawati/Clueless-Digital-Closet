import os
import sys
import tkinter as tk

from enum import Enum
from PIL import Image, ImageTk

from helpers import get_duplicates


WINDOW_TITLE = "Clueless Digital Closet"
MAIN_FRAME_HEIGHT = 600
MAIN_FRAME_WIDTH = 350
INDIVIDUAL_FRAME_HEIGHT = 250
INDIVIDUAL_FRAME_WIDTH = 250


class ContentType(Enum):
    """Different types of content to be displayed in individual frames."""
    top = "top"
    bottom = "bottom"


class DigitalCloset:
    """Digital representation of a person's closet."""

    def __init__(self, root, image_directories):
        """Create an instance of a digital closet, complete with necessary images and navigation functions.

        :param root: Root
        :type root: tkinter.Tk
        :param image_directories: Image directory paths for each content type.
        :type image_directories: dict
        """
        # Carry out validation checks.
        self.validate_image_directories(image_directories)

        # Initialise.
        self.root = root
        self.image_directories = image_directories

        # Names of all images.
        self.top_images = self.get_image_file_names(image_directories, ContentType.top.value)
        self.bottom_images = self.get_image_file_names(image_directories, ContentType.bottom.value)

        # Names of current images.
        self.current_top_image = self.top_images[0]
        self.current_bottom_image = self.bottom_images[0]

        # Create the main frame.
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{MAIN_FRAME_WIDTH}x{MAIN_FRAME_HEIGHT}")

        # Create the individual frame for tops.
        self.top_frame = tk.Frame(self.root)
        current_top_image_path = os.path.join(image_directories[ContentType.top.value], self.current_top_image)
        self.top_frame_content = self.create_individual_frame_content(current_top_image_path, self.top_frame)
        self.top_frame_content.pack(side=tk.TOP)
        self.top_frame.pack()

        # Create navigation buttons for the top frame.
        self.top_prev_button = tk.Button(self.top_frame, text="Previous top", command=self.get_previous_top)
        self.top_prev_button.pack(side=tk.LEFT)
        self.top_next_button = tk.Button(self.top_frame, text="Next top", command=self.get_next_top)
        self.top_next_button.pack(side=tk.RIGHT)

        # Create the individual frame for bottoms.
        self.bottom_frame = tk.Frame(self.root)
        current_bottom_image_path = os.path.join(image_directories[ContentType.bottom.value], self.current_bottom_image)
        self.bottom_frame_content = self.create_individual_frame_content(current_bottom_image_path, self.bottom_frame)
        self.bottom_frame_content.pack(side=tk.BOTTOM)
        self.bottom_frame.pack()

        # Create navigation buttons for the bottom frame.
        self.bottom_prev_button = tk.Button(self.bottom_frame, text="Previous bottom", command=self.get_previous_bottom)
        self.bottom_prev_button.pack(side=tk.LEFT)
        self.bottom_next_button = tk.Button(self.bottom_frame, text="Next bottom", command=self.get_next_bottom)
        self.bottom_next_button.pack(side=tk.RIGHT)

    def validate_image_directories(self, directories):
        """Carry out validation checks on the given image directories.

        :param directories: Directory paths for all content types.
        :type directories: dict
        """
        if not isinstance(directories, dict):
            sys.exit("Given directories must be an instance of a dictionary.")

        exit_msg = ""

        for content_type in ContentType:
            if directories.get(content_type.value):
                all_image_file_names = self.get_image_file_names(directories, content_type)
                duplicate_file_names = get_duplicates(all_image_file_names)

                if duplicate_file_names:
                    exit_msg += (
                        f"Duplicate file names detected in directory for content type '{content_type.value}'. They "
                        f"are: {', '.join(duplicate_file_names)}.\n"
                    )
            else:
                exit_msg += f"No directory found for content type '{content_type.value}' within given directories.\n"

        if exit_msg:
            sys.exit(exit_msg)

    @staticmethod
    def get_image_file_names(directories, content_type):
        """For the given content type, get the file names of images in the relevant directory.

        :param directories: Directory paths for all content types.
        :type directories: dict
        :param content_type: Type of content.
        :type content_type: ContentType choice value
        :return: File names for image files.
        :rtype: list
        """
        return [file_name for file_name in os.listdir(directories[content_type])]

    def create_individual_frame_content(self, image_path, frame):
        """Return the content to be displayed in an individual frame.

        :param image_path: File path for an image.
        :type image_path: str
        :param frame: Individual frame.
        :type frame: tkinter.Frame
        :return: The content to be displayed in the frame.
        :rtype: tkinter.Label
        """
        image = self.get_image(image_path)
        image_content = tk.Label(frame, image=image)
        image_content.image = image
        return image_content

    @staticmethod
    def get_image(image_path):
        """Return an image based on the requested image path.

        :param image_path: File path for an image.
        :type image_path: str
        :return: Image.
        :rtype: PIL.ImageTk.PhotoImage
        """
        image = Image.open(image_path)
        image = image.resize((INDIVIDUAL_FRAME_WIDTH, INDIVIDUAL_FRAME_HEIGHT))
        image = ImageTk.PhotoImage(image)
        return image

    def get_next_top(self):
        """Get the next top to be displayed in the top frame."""
        new_top_image = self.get_new_image_file_name(ContentType.top.value)
        self.current_top_image = new_top_image
        self.update_frame_content(ContentType.top.value, new_top_image)

    def get_previous_top(self):
        """Get the previous top to be displayed in the top frame."""
        new_top_image = self.get_new_image_file_name(ContentType.top.value, next_item=False)
        self.current_top_image = new_top_image
        self.update_frame_content(ContentType.top.value, new_top_image)

    def get_next_bottom(self):
        """Get the next bottom to be displayed in the bottom frame."""
        new_bottom_image = self.get_new_image_file_name(ContentType.bottom.value)
        self.current_bottom_image = new_bottom_image
        self.update_frame_content(ContentType.bottom.value, new_bottom_image)

    def get_previous_bottom(self):
        """Get the previous bottom to be displayed in the bottom frame."""
        new_bottom_image = self.get_new_image_file_name(ContentType.bottom.value, next_item=False)
        self.current_bottom_image = new_bottom_image
        self.update_frame_content(ContentType.bottom.value, new_bottom_image)

    def get_new_image_file_name(self, content_type, next_item=True):
        """Get the file name of the new image to be displayed.

        :param content_type: Type of content.
        :type content_type: ContentType choice value
        :param next_item: Whether to display the next item (True) or whether to display the previous item (False).
        :type next_item: bool
        :return: File name of an image.
        :rtype: str
        """
        if content_type == ContentType.top.value:
            all_image_file_names = self.top_images
            current_image_file_name_index = all_image_file_names.index(self.current_top_image)
        elif content_type == ContentType.bottom.value:
            all_image_file_names = self.bottom_images
            current_image_file_name_index = all_image_file_names.index(self.current_bottom_image)

        total_image_file_names = len(all_image_file_names)

        if next_item:
            if current_image_file_name_index == (total_image_file_names - 1):
                new_image_file_name = all_image_file_names[0]
            else:
                new_image_file_name = all_image_file_names[current_image_file_name_index + 1]
        else:
            if current_image_file_name_index == 0:
                new_image_file_name = all_image_file_names[total_image_file_names - 1]
            else:
                new_image_file_name = all_image_file_names[current_image_file_name_index - 1]

        return new_image_file_name

    def update_frame_content(self, content_type, new_image_file_name):
        """Update the content of the individual frame.

        :param content_type: Type of content.
        :type content_type: ContentType choice value
        :param new_image_file_name: File name of the new image to be displayed.
        :type new_image_file_name: str
        """
        new_image_file_path = os.path.join(self.image_directories[content_type], new_image_file_name)
        image = self.get_image(new_image_file_path)

        if content_type == ContentType.top.value:
            frame_content = self.top_frame_content
        elif content_type == ContentType.bottom.value:
            frame_content = self.bottom_frame_content

        frame_content.configure(image=image)
        frame_content.image = image


# Launch an instance of a digital closet when the script is run.
if __name__ == "__main__":
    root = tk.Tk()
    current_dir = os.path.dirname(os.path.realpath(__file__))
    image_directories = {
        "top": os.path.join(current_dir, "top_images"), "bottom": os.path.join(current_dir, "bottom_images")
    }
    DigitalCloset(root, image_directories)
    root.mainloop()
