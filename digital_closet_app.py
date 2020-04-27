import os
import tkinter as tk
from PIL import Image, ImageTk
from enum import Enum


WINDOW_TITLE = "Digital Closet"
MAIN_FRAME_HEIGHT = 600
MAIN_FRAME_WIDTH = 350
INDIVIDUAL_FRAME_HEIGHT = 250
INDIVIDUAL_FRAME_WIDTH = 250

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
TOP_IMAGE_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "top_images")
BOTTOM_IMAGE_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "bottom_images")


class FrameType(Enum):
    top = "Top"
    bottom = "Bottom"


class DigitalCloset:
    def __init__(self, root):
        # Initialise with a root.
        self.root = root

        # Get all images.
        self.all_top_image_file_names = [file_name for file_name in os.listdir(TOP_IMAGE_DIRECTORY)]
        self.all_bottom_image_file_names = [file_name for file_name in os.listdir(BOTTOM_IMAGE_DIRECTORY)]

        # Get current display images.
        self.top_image_file_name = self.all_top_image_file_names[0]
        self.top_image_path = os.path.join(TOP_IMAGE_DIRECTORY, self.top_image_file_name)
        self.bottom_image_file_name = self.all_bottom_image_file_names[0]
        self.bottom_image_path = os.path.join(BOTTOM_IMAGE_DIRECTORY, self.bottom_image_file_name)

        # Make the individual frames.
        self.top_frame = tk.Frame(self.root)
        self.bottom_frame = tk.Frame(self.root)

        # Add corresponding images to the frames.
        self.top_frame_content = self.create_frame_content(self.top_image_path, self.top_frame)
        self.top_frame_content.pack(side=tk.TOP)
        self.bottom_frame_content = self.create_frame_content(self.bottom_image_path, self.bottom_frame)
        self.bottom_frame_content.pack(side=tk.BOTTOM)

        # Create the main frame.
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{MAIN_FRAME_WIDTH}x{MAIN_FRAME_HEIGHT}")

        # Add the top image.
        self.top_frame.pack()

        # Add the top buttons.
        self.top_prev_button = tk.Button(self.top_frame, text="Previous top", command=self.get_previous_top)
        self.top_prev_button.pack(side=tk.LEFT)
        self.top_next_button = tk.Button(self.top_frame, text="Next top", command=self.get_next_top)
        self.top_next_button.pack(side=tk.RIGHT)

        # Add the bottom image.
        self.bottom_frame.pack()

        # Add the bottom buttons.
        self.bottom_prev_button = tk.Button(self.bottom_frame, text="Previous bottom", command=self.get_previous_bottom)
        self.bottom_prev_button.pack(side=tk.LEFT)
        self.bottom_next_button = tk.Button(self.bottom_frame, text="Next bottom", command=self.get_next_bottom)
        self.bottom_next_button.pack(side=tk.RIGHT)

    def create_frame_content(self, image_file_path, frame):
        image = self.get_image(image_file_path)
        image_content = tk.Label(frame, image=image)
        image_content.image = image
        return image_content

    def get_image(self, image_file_path):
        image = Image.open(image_file_path)
        image = image.resize((INDIVIDUAL_FRAME_WIDTH, INDIVIDUAL_FRAME_HEIGHT))
        image = ImageTk.PhotoImage(image)
        return image

    def get_next_top(self):
        new_image_file_name = self.get_new_image_file_name(FrameType.top)
        self.top_image_file_name = new_image_file_name
        self.update_top_frame_content(new_image_file_name)

    def get_previous_top(self):
        new_image_file_name = self.get_new_image_file_name(FrameType.top, next_item=False)
        self.top_image_file_name = new_image_file_name
        self.update_top_frame_content(new_image_file_name)

    def get_next_bottom(self):
        new_image_file_name = self.get_new_image_file_name(FrameType.bottom)
        self.bottom_image_file_name = new_image_file_name
        self.update_bottom_frame_content(new_image_file_name)

    def get_previous_bottom(self):
        new_image_file_name = self.get_new_image_file_name(FrameType.bottom, next_item=False)
        self.bottom_image_file_name = new_image_file_name
        self.update_bottom_frame_content(new_image_file_name)

    def get_new_image_file_name(self, frame_type, next_item=True):
        if frame_type == FrameType.top:
            all_image_file_names = self.all_top_image_file_names
            current_image_file_name_index = all_image_file_names.index(self.top_image_file_name)
        elif frame_type == FrameType.bottom:
            all_image_file_names = self.all_bottom_image_file_names
            current_image_file_name_index = all_image_file_names.index(self.bottom_image_file_name)

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

    def update_top_frame_content(self, new_image_file_name):
        new_image_file_path = os.path.join(TOP_IMAGE_DIRECTORY, new_image_file_name)
        self.update_individual_frame_content(self.top_frame_content, new_image_file_path)

    def update_bottom_frame_content(self, new_image_file_name):
        new_image_file_path = os.path.join(BOTTOM_IMAGE_DIRECTORY, new_image_file_name)
        self.update_individual_frame_content(self.bottom_frame_content, new_image_file_path)

    def update_individual_frame_content(self, frame_content, new_image_file_path):
        image = self.get_image(new_image_file_path)
        frame_content.configure(image=image)
        frame_content.image = image


if __name__ == "__main__":
    root = tk.Tk()
    DigitalCloset(root)
    root.mainloop()


# TODO: Add validation to ensure no duplicate paths for same top or bottom
