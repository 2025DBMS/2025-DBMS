import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import numpy as np
from typing import List, Tuple, Dict, Union
import os

class SimilaritySearch:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def compute_image_similarity(self, image1: Union[str, Image.Image], 
                               image2: Union[str, Image.Image]) -> float:
        """Compute similarity between two images"""
        if isinstance(image1, str):
            image1 = Image.open(image1)
        if isinstance(image2, str):
            image2 = Image.open(image2)

        inputs1 = self.processor(images=image1, return_tensors="pt", padding=True)
        inputs2 = self.processor(images=image2, return_tensors="pt", padding=True)

        with torch.no_grad():
            features1 = self.model.get_image_features(**inputs1)
            features2 = self.model.get_image_features(**inputs2)

        similarity = torch.nn.functional.cosine_similarity(features1, features2)
        return float(similarity)

    def compute_text_similarity(self, text1: str, text2: str) -> float:
        """Compute similarity between two text strings"""
        inputs1 = self.processor(text=text1, return_tensors="pt", padding=True)
        inputs2 = self.processor(text=text2, return_tensors="pt", padding=True)

        with torch.no_grad():
            features1 = self.model.get_text_features(**inputs1)
            features2 = self.model.get_text_features(**inputs2)

        similarity = torch.nn.functional.cosine_similarity(features1, features2)
        return float(similarity)

    def get_image_features(self, image: Union[str, Image.Image]) -> np.ndarray:
        """Get image features for embedding"""
        if isinstance(image, str):
            image = Image.open(image)
        inputs = self.processor(images=image, return_tensors="pt", padding=True)
        with torch.no_grad():
            features = self.model.get_image_features(**inputs)
        return features.cpu().numpy().flatten()

    def get_text_features(self, text: str) -> np.ndarray:
        """Get text features for embedding"""
        inputs = self.processor(text=text, return_tensors="pt", padding=True)
        with torch.no_grad():
            features = self.model.get_text_features(**inputs)
        return features.cpu().numpy().flatten() 