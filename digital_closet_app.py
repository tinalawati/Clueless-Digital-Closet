import os
import tkinter as tk

from PIL import Image, ImageTk
from enum import Enum


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

        :param root: #TODO
        :type root: #TODO
        :param image_directories: Image directory paths for each content type.
        :type image_directories: dict
        """
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
        self.top_frame_content = self.create_frame_content(current_top_image_path, self.top_frame)
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
        self.bottom_frame_content = self.create_frame_content(current_bottom_image_path, self.bottom_frame)
        self.bottom_frame_content.pack(side=tk.BOTTOM)
        self.bottom_frame.pack()

        # Create navigation buttons for the bottom frame.
        self.bottom_prev_button = tk.Button(self.bottom_frame, text="Previous bottom", command=self.get_previous_bottom)
        self.bottom_prev_button.pack(side=tk.LEFT)
        self.bottom_next_button = tk.Button(self.bottom_frame, text="Next bottom", command=self.get_next_bottom)
        self.bottom_next_button.pack(side=tk.RIGHT)

    def get_image_file_names(self, directories, image_type):
        # TODO: Check there is image_type as key in directories dict
        # TODO: Ensure no duplicate file names
        return [file_name for file_name in os.listdir(directories[image_type])]

    def create_frame_content(self, image_path, frame):
        image = self.get_image(image_path)
        image_content = tk.Label(frame, image=image)
        image_content.image = image
        return image_content

    def get_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((INDIVIDUAL_FRAME_WIDTH, INDIVIDUAL_FRAME_HEIGHT))
        image = ImageTk.PhotoImage(image)
        return image

    def get_next_top(self):
        new_top_image = self.get_new_image_file_name(ContentType.top.value)
        self.current_top_image = new_top_image
        self.update_frame_content(ContentType.top.value, new_top_image)

    def get_previous_top(self):
        new_top_image = self.get_new_image_file_name(ContentType.top.value, next_item=False)
        self.current_top_image = new_top_image
        self.update_frame_content(ContentType.top.value, new_top_image)

    def get_next_bottom(self):
        new_bottom_image = self.get_new_image_file_name(ContentType.bottom.value)
        self.current_bottom_image = new_bottom_image
        self.update_frame_content(ContentType.bottom.value, new_bottom_image)

    def get_previous_bottom(self):
        new_bottom_image = self.get_new_image_file_name(ContentType.bottom.value, next_item=False)
        self.current_bottom_image = new_bottom_image
        self.update_frame_content(ContentType.bottom.value, new_bottom_image)

    def get_new_image_file_name(self, content_type, next_item=True):
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
