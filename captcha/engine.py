import torch
from tqdm import tqdm

from data_collector import encoding_to_text


def train_one_epoch(model, dataloader, optimizer, criterion, device):
    model.train()
    total_loss = 0
    correct_predictions = 0
    total_samples = 0
    for i, (images, targets) in enumerate(tqdm(dataloader, desc="Training", leave=False)):
        images = images.to(device)
        targets = targets.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        # Calculate accuracy
        encoded_outputs = outputs.view(-1, 4, 26)
        predictions = torch.zeros_like(encoded_outputs, device=device)
        # Mark predictions' entries with 1 when it's the maximum index of each row at the second dimension
        max_indices = torch.argmax(encoded_outputs, dim=2, keepdim=True)
        # print(max_indices[0])
        predictions.scatter_(2, max_indices, 1)
        predictions = predictions.view(-1, 4 * 26)
        # print(predictions[0])
        targets = targets.view(-1, 4 * 26)
        # print(targets[0])
        # print(encoding_to_text(predictions[0].view(4, 26).cpu().numpy()))
        # print(encoding_to_text(targets[0].view(4, 26).cpu().numpy()))
        correct_predictions += (predictions == targets).all(1).sum().item()
        total_samples += targets.size(0)
    average_loss = total_loss / len(dataloader)
    accuracy = correct_predictions / total_samples
    return average_loss, accuracy


def evaluate(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0
    correct_predictions = 0
    total_samples = 0
    with torch.no_grad():
        for i, (images, targets) in enumerate(tqdm(dataloader, desc="Evaluating", leave=False)):
            images = images.to(device)
            targets = targets.to(device)
            outputs = model(images)
            loss = criterion(outputs, targets)
            total_loss += loss.item()
            # Calculate accuracy
            encoded_outputs = outputs.view(-1, 4, 26)
            predictions = torch.zeros_like(encoded_outputs, device=device)
            # Mark predictions' entries with 1 when it's the maximum index of each row at the second dimension
            max_indices = torch.argmax(encoded_outputs, dim=2, keepdim=True)
            predictions.scatter_(2, max_indices, 1)
            predictions = predictions.view(-1, 4 * 26)
            targets = targets.view(-1, 4 * 26)
            print(encoding_to_text(predictions[0].view(4, 26).cpu().numpy()))
            print(encoding_to_text(targets[0].view(4, 26).cpu().numpy()))
            correct_predictions += (predictions == targets).all(1).sum().item()
            total_samples += targets.size(0)
    average_loss = total_loss / len(dataloader)
    accuracy = correct_predictions / total_samples
    return average_loss, accuracy
