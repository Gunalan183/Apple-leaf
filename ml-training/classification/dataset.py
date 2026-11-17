"""
GAN-Sim-GAN PyTorch Dataset
Custom Dataset class for Apple Leaf Disease images
"""

import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets
from PIL import Image
from pathlib import Path


class AppleLeafDataset(Dataset):
    """
    Custom Dataset for Apple Leaf Disease Classification
    Uses ImageFolder internally for automatic class detection
    """
    
    def __init__(self, root_dir, transform=None, class_names=None):
        """
        Args:
            root_dir (str or Path): Root directory with class subdirectories
            transform (callable, optional): Transform to apply to images
            class_names (list, optional): Expected class names for validation
        """
        self.root_dir = Path(root_dir)
        self.transform = transform
        
        # Use ImageFolder for automatic class detection
        self.dataset = datasets.ImageFolder(root=str(root_dir))
        
        # Validate class names if provided
        if class_names is not None:
            detected_classes = [self.dataset.classes[i] for i in range(len(self.dataset.classes))]
            detected_classes_sorted = sorted(detected_classes)
            class_names_sorted = sorted(class_names)
            
            if detected_classes_sorted != class_names_sorted:
                print(f"⚠️  Warning: Class mismatch!")
                print(f"   Expected: {class_names_sorted}")
                print(f"   Found: {detected_classes_sorted}")
        
        self.classes = self.dataset.classes
        self.class_to_idx = self.dataset.class_to_idx
        self.idx_to_class = {v: k for k, v in self.class_to_idx.items()}
    
    def __len__(self):
        """Return the total number of images"""
        return len(self.dataset)
    
    def __getitem__(self, idx):
        """
        Get image and label at index
        
        Args:
            idx (int): Index
            
        Returns:
            tuple: (image, label) where image is transformed PIL Image
        """
        image, label = self.dataset[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label
    
    def get_class_name(self, label_idx):
        """Get class name from label index"""
        return self.idx_to_class[label_idx]
    
    def get_class_distribution(self):
        """
        Calculate class distribution in the dataset
        
        Returns:
            dict: Class name -> count
        """
        class_counts = {}
        for class_name in self.classes:
            class_dir = self.root_dir / class_name
            if class_dir.exists():
                count = len(list(class_dir.glob('*.[jp][pn][g]*')))
                count += len(list(class_dir.glob('*.jpeg')))
                class_counts[class_name] = count
        
        return class_counts


def create_dataloaders(train_dir, val_dir, test_dir, 
                       train_transform, val_transform,
                       batch_size=32, num_workers=4,
                       class_names=None):
    """
    Create PyTorch DataLoaders for train, validation, and test sets
    
    Args:
        train_dir: Training data directory
        val_dir: Validation data directory
        test_dir: Test data directory
        train_transform: Transforms for training (with augmentation)
        val_transform: Transforms for validation/test (no augmentation)
        batch_size: Batch size for DataLoader
        num_workers: Number of worker processes
        class_names: Expected class names
        
    Returns:
        tuple: (train_loader, val_loader, test_loader, dataset_sizes, class_names)
    """
    
    # Create datasets
    train_dataset = AppleLeafDataset(
        root_dir=train_dir,
        transform=train_transform,
        class_names=class_names
    )
    
    val_dataset = AppleLeafDataset(
        root_dir=val_dir,
        transform=val_transform,
        class_names=class_names
    )
    
    test_dataset = AppleLeafDataset(
        root_dir=test_dir,
        transform=val_transform,
        class_names=class_names
    )
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available()
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available()
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available()
    )
    
    # Get dataset sizes
    dataset_sizes = {
        'train': len(train_dataset),
        'val': len(val_dataset),
        'test': len(test_dataset)
    }
    
    # Print summary
    print("📊 Dataset Summary:")
    print(f"   Training: {dataset_sizes['train']} images")
    print(f"   Validation: {dataset_sizes['val']} images")
    print(f"   Test: {dataset_sizes['test']} images")
    print(f"\n   Classes: {train_dataset.classes}")
    print(f"   Class indices: {train_dataset.class_to_idx}")
    
    # Print class distribution
    print("\n   Training class distribution:")
    train_dist = train_dataset.get_class_distribution()
    for class_name, count in train_dist.items():
        percentage = (count / dataset_sizes['train']) * 100
        print(f"      {class_name}: {count} ({percentage:.1f}%)")
    
    return train_loader, val_loader, test_loader, dataset_sizes, train_dataset.classes


if __name__ == "__main__":
    # Test dataset loading
    from pathlib import Path
    import sys
    
    # Add parent directory to path
    sys.path.append(str(Path(__file__).parent.parent))
    
    from classification.config import TRAIN_DIR, CLASS_NAMES
    from classification.transforms import get_transforms
    
    print("Testing Dataset Loading...")
    print(f"Train directory: {TRAIN_DIR}")
    
    train_transform, _ = get_transforms()
    
    dataset = AppleLeafDataset(
        root_dir=TRAIN_DIR,
        transform=train_transform,
        class_names=CLASS_NAMES
    )
    
    print(f"\nDataset size: {len(dataset)}")
    print(f"Classes: {dataset.classes}")
    print(f"Class to index: {dataset.class_to_idx}")
    
    # Test loading a sample
    image, label = dataset[0]
    print(f"\nSample image shape: {image.shape}")
    print(f"Sample label: {label} ({dataset.get_class_name(label)})")
    
    print("\n✅ Dataset test passed!")
