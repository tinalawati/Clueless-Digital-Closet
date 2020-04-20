import os
import tkinter as tk
from PIL import Image, ImageTk


WINDOW_TITLE = "Digital Closet"
MAIN_FRAME_HEIGHT = 450
MAIN_FRAME_WIDTH = 300
INDIVIDUAL_FRAME_HEIGHT = 200
INDIVIDUAL_FRAME_WIDTH = 200

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
TOP_IMAGE_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "top_images")
BOTTOM_IMAGE_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "bottom_images")


class DigitalCloset:
    def __init__(self, root):
        # Initialise with a root.
        self.root = root

        # Get all images.
        self.all_top_image_paths = [
            os.path.join(TOP_IMAGE_DIRECTORY, file_name) for file_name in os.listdir(TOP_IMAGE_DIRECTORY)
        ]
        self.all_bottom_image_paths = [
            os.path.join(BOTTOM_IMAGE_DIRECTORY, file_name) for file_name in os.listdir(BOTTOM_IMAGE_DIRECTORY)
        ]

        # Get current images.
        self.top_image_path = self.all_top_image_paths[0]
        self.bottom_image_path = self.all_bottom_image_paths[0]

        # Make the individual frames.
        self.top_frame = tk.Frame(self.root)
        self.bottom_frame = tk.Frame(self.root)

        # Add corresponding images to the frames.
        self.top_frame_content = self.create_frame_content(self.top_image_path, self.top_frame)
        self.top_frame_content.pack(side=tk.TOP)
        self.bottom_frame_content = self.create_frame_content(self.bottom_image_path, self.bottom_frame)
        self.bottom_frame_content.pack(side=tk.BOTTOM)

        # Create the main frame
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{MAIN_FRAME_WIDTH}x{MAIN_FRAME_HEIGHT}")

        # Add the individual frames to the main frame.
        self.top_frame.pack()
        self.bottom_frame.pack()

    @staticmethod
    def create_frame_content(image_path, frame):
        image = Image.open(image_path)
        image = image.resize((INDIVIDUAL_FRAME_WIDTH, INDIVIDUAL_FRAME_HEIGHT))
        image = ImageTk.PhotoImage(image)
        image_content = tk.Label(frame, image=image)
        image_content.image = image
        return image_content


if __name__ == "__main__":
    root = tk.Tk()
    DigitalCloset(root)
    root.mainloop()
