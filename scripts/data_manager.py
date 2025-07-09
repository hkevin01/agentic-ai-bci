#!/usr/bin/env python3
"""
Data download and management script for BCI datasets.
"""

import argparse
import asyncio
from pathlib import Path
from typing import List, Optional

import requests
from loguru import logger


class DatasetDownloader:
    """Download and manage BCI datasets from various sources."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or (
            Path(__file__).parent.parent / "data" / "raw"
        )
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def list_openneuro_datasets(self, limit: int = 10) -> List[dict]:
        """List available datasets from OpenNeuro."""
        logger.info("Fetching OpenNeuro datasets...")
        
        try:
            response = requests.get(
                "https://openneuro.org/crn/api/datasets",
                params={"limit": limit}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch OpenNeuro datasets: {e}")
            return []
    
    def list_physionet_datasets(self) -> List[dict]:
        """List relevant BCI datasets from PhysioNet."""
        # Common BCI-related datasets on PhysioNet
        bci_datasets = [
            {
                "id": "eegmmidb",
                "name": "EEG Motor Movement/Imagery Dataset",
                "description": (
                    "64-channel EEG recordings of motor movement "
                    "and imagery tasks"
                )
            },
            {
                "id": "chbmit",
                "name": "CHB-MIT Scalp EEG Database",
                "description": (
                    "Continuous scalp EEG from pediatric subjects "
                    "with intractable seizures"
                )
            },
            {
                "id": "sleep-edfx",
                "name": "Sleep-EDF Database Expanded",
                "description": "Sleep recordings with annotations"
            }
        ]
        return bci_datasets
    
    async def download_sample_dataset(self, dataset_id: str) -> bool:
        """Download a sample dataset for testing."""
        logger.info(f"Downloading sample data for {dataset_id}...")
        
        # This is a placeholder - implement actual download logic
        # based on the specific dataset API
        
        sample_dir = self.data_dir / dataset_id
        sample_dir.mkdir(exist_ok=True)
        
        # Create a sample metadata file
        metadata = {
            "dataset_id": dataset_id,
            "download_date": "2025-01-09",
            "description": f"Sample data for {dataset_id}",
            "files": []
        }
        
        import json
        with open(sample_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Sample dataset {dataset_id} prepared in {sample_dir}")
        return True
    
    def create_sample_eeg_data(self):
        """Create synthetic EEG data for development and testing."""
        logger.info("Creating synthetic EEG data...")
        
        import numpy as np

        # Generate synthetic EEG data
        n_channels = 64
        n_samples = 1000
        sampling_rate = 256
        
        # Create synthetic data with some basic patterns
        time = np.linspace(0, n_samples / sampling_rate, n_samples)
        data = np.random.randn(n_channels, n_samples) * 50  # Base noise
        
        # Add some alpha rhythm (8-12 Hz)
        alpha_freq = 10
        for ch in range(n_channels):
            alpha_component = 20 * np.sin(2 * np.pi * alpha_freq * time)
            data[ch] += alpha_component * (0.5 + 0.5 * np.random.rand())
        
        # Save as numpy array
        sample_dir = self.data_dir / "synthetic_eeg"
        sample_dir.mkdir(exist_ok=True)
        
        np.save(sample_dir / "eeg_data.npy", data)
        
        # Create channel information
        channels = [f"Ch{i+1:02d}" for i in range(n_channels)]
        
        metadata = {
            "n_channels": n_channels,
            "n_samples": n_samples,
            "sampling_rate": sampling_rate,
            "channels": channels,
            "description": "Synthetic EEG data for development"
        }
        
        import json
        with open(sample_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Synthetic EEG data created in {sample_dir}")


def main():
    """Main function for data management script."""
    parser = argparse.ArgumentParser(description="BCI Dataset Management")
    
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands"
    )
    
    # List datasets command
    list_parser = subparsers.add_parser("list", help="List available datasets")
    list_parser.add_argument(
        "--source",
        choices=["openneuro", "physionet", "all"],
        default="all",
        help="Dataset source"
    )
    
    # Download command
    download_parser = subparsers.add_parser(
        "download", help="Download dataset"
    )
    download_parser.add_argument("dataset_id", help="Dataset identifier")
    download_parser.add_argument(
        "--data-dir", type=Path, help="Data directory"
    )
    
    # Create synthetic data command
    subparsers.add_parser(
        "create-synthetic", help="Create synthetic EEG data"
    )
    
    args = parser.parse_args()
    
    data_dir = getattr(args, 'data_dir', None)
    downloader = DatasetDownloader(data_dir)
    
    if args.command == "list":
        if args.source in ["openneuro", "all"]:
            datasets = downloader.list_openneuro_datasets()
            print("\nOpenNeuro Datasets:")
            for ds in datasets[:5]:  # Show first 5
                label = ds.get('label', 'Unknown')
                desc = ds.get('description', 'No description')
                print(f"- {label}: {desc}")
        
        if args.source in ["physionet", "all"]:
            datasets = downloader.list_physionet_datasets()
            print("\nPhysioNet BCI Datasets:")
            for ds in datasets:
                print(f"- {ds['name']}: {ds['description']}")
    
    elif args.command == "download":
        asyncio.run(downloader.download_sample_dataset(args.dataset_id))
    
    elif args.command == "create-synthetic":
        downloader.create_sample_eeg_data()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
