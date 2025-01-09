# works

import cv2
import numpy as np
from src.face_mesh import (
    get_landmark_points, 
    get_triangles, 
    triangulation, 
    swap_new_face, 
    add_piece_of_new_face, 
    warp_triangle
)

class FaceSwapper:
    """Class to handle face swapping logic for both images and video."""
    def __init__(self, src_image_path=None, width=640, height=480):
        # Constants
        self.WIDTH = width
        self.HEIGHT = height
        
        # Initialize video capture
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(3, self.WIDTH)
        self.cap.set(4, self.HEIGHT)
        
        # Load source image
        self.src_image = None
        if src_image_path:
            self.set_src_image(self.src_image)
        
    def set_src_image(self, image):
        """Set and process the source image for face swapping."""
        if image is None:
            raise ValueError("Cannot set a None image as the source.")
        self.src_image = image
        self.src_image_gray = cv2.cvtColor(self.src_image, cv2.COLOR_BGR2GRAY)
        self.src_mask = np.zeros_like(self.src_image_gray)
        self.src_landmark_points = get_landmark_points(self.src_image)
        if not self.src_landmark_points:
            raise ValueError("No facial landmarks detected in the source image.")
        self.src_np_points = np.array(self.src_landmark_points)
        self.src_convexHull = cv2.convexHull(self.src_np_points)
        cv2.fillConvexPoly(self.src_mask, self.src_convexHull, 255)
        self.indexes_triangles = get_triangles(
            convexhull=self.src_convexHull,
            landmarks_points=self.src_landmark_points,
            np_points=self.src_np_points
        )

    def set_src_image_path(self, src_image_path):
        """Load and set the source image by path."""
        image = cv2.imread(src_image_path)
        if image is None:
            raise ValueError(f"Could not load source image: {src_image_path}")
        self.set_src_image(image)

    def process_frame(self, dest_image):
        """Process a single frame/image for face swapping."""
        if self.src_image is None:
            raise ValueError("Source image not set")
            
        dest_image_gray = cv2.cvtColor(dest_image, cv2.COLOR_BGR2GRAY)        
        # Get destination landmark points
        dest_landmark_points = get_landmark_points(dest_image)

        # If no face detected, return original image
        if dest_landmark_points is None:
            print("No face detected in the destination image")
            return cv2.cvtColor(dest_image, cv2.COLOR_BGR2RGB)
        
        dest_np_points = np.array(dest_landmark_points)
        dest_convexHull = cv2.convexHull(dest_np_points)
        
        height, width, channels = dest_image.shape
        new_face = np.zeros((height, width, channels), np.uint8)
        
        # Triangulation and warping
        for triangle_index in self.indexes_triangles:
            points, src_cropped_triangle, cropped_triangle_mask, _ = triangulation(
                triangle_index=triangle_index,
                landmark_points=self.src_landmark_points,
                img=self.src_image
            )
            
            points2, _, dest_cropped_triangle_mask, rect = triangulation(
                triangle_index=triangle_index,
                landmark_points=dest_landmark_points
            )
            
            warped_triangle = warp_triangle(
                rect=rect, points1=points, points2=points2,
                src_cropped_triangle=src_cropped_triangle,
                dest_cropped_triangle_mask=dest_cropped_triangle_mask
            )
            add_piece_of_new_face(
                new_face=new_face, rect=rect, warped_triangle=warped_triangle
            )
        
        result = swap_new_face(
            dest_image=dest_image, dest_image_gray=dest_image_gray,
            dest_convexHull=dest_convexHull, new_face=new_face
        )
        result = cv2.medianBlur(result, 3)
        
        return cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    
    def swap_image(self, dest_image_path):
        """Perform face swap on a static image."""
        if self.src_image is None:
            raise ValueError("Source image not set")
    
        # Load destination image
        dest_image = cv2.imread(dest_image_path)
        if dest_image is None:
            raise ValueError(f"Could not load destination image: {dest_image_path}")
        
        # Resize if needed while maintaining aspect ratio
        aspect_ratio = dest_image.shape[1] / dest_image.shape[0]
        if dest_image.shape[1] > self.WIDTH:
            new_width = self.WIDTH
            new_height = int(new_width / aspect_ratio)
            dest_image = cv2.resize(dest_image, (new_width, new_height))
        
        return self.process_frame(dest_image)

    def start_video(self):
        """Initialize video capture for real-time face swapping."""
        if self.cap is None:
            self.init_video_capture()
        return self.cap is not None

    def read_video_frame(self):
        """Read and process a frame from video capture."""
        if self.cap is None:
            raise ValueError("Video capture not initialized")
            
        ret, frame = self.cap.read()
        if not ret:
            return None
            
        return self.process_frame(frame)

    def release_video(self):
        """Release video capture resources."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def __del__(self):
        """Cleanup resources on deletion."""
        self.release_video()

    def clear_temp_data(self):
        """Clears temporary data such as intermediate frames."""
        self.temp_frame = None  # Example: Clear any cached frame
