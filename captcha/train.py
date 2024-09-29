import argparse

import torch
from torch.utils.data import DataLoader

from model import CaptchaModel
from dataset import get_datasets, collate_fn
from engine import train_one_epoch, evaluate


def main(args):
    # initialize the model
    device = torch.device("mps")
    model = CaptchaModel().to(device)
    dataset_train, dataset_val, dataset_test = get_datasets()
    # get dataloaders
    dataloader_train = DataLoader(dataset_train, batch_size=args.batch_size, shuffle=True, collate_fn=collate_fn)
    dataloader_val = DataLoader(dataset_val, batch_size=args.batch_size, shuffle=False, collate_fn=collate_fn)
    dataloader_test = DataLoader(dataset_test, batch_size=args.batch_size, shuffle=False, collate_fn=collate_fn)
    # initialize the optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.1)
    criterion = torch.nn.BCEWithLogitsLoss()
    for epoch in range(args.epochs):
        train_loss, train_accuracy = train_one_epoch(model, dataloader_train, optimizer, criterion, device)
        val_loss, val_accuracy = evaluate(model, dataloader_val, criterion, device)
        print(f"Epoch {epoch + 1}/{args.epochs}")
        print(f"Train Loss: {train_loss:.4f} Accuracy: {train_accuracy:.4f}")
        print(f"Val Loss: {val_loss:.4f} Accuracy: {val_accuracy:.4f}")
    test_loss, test_accuracy = evaluate(model, dataloader_test, criterion, device)
    print(f"Test Loss: {test_loss:.4f} Accuracy: {test_accuracy:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=30, help="Number of epochs to train")
    parser.add_argument("--lr", type=float, default=0.0001, help="Learning rate")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size")
    args = parser.parse_args()
    main(args)
