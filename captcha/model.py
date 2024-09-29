import torch.nn as nn
from transformers import MobileViTV2Model


class CaptchaModel(nn.Module):
    def __init__(self):
        super(CaptchaModel, self).__init__()
        self.backbone = MobileViTV2Model.from_pretrained("apple/mobilevitv2-1.0-imagenet1k-256")
        self.classifier = nn.Linear(512 * 8 * 8, 26 * 4)

    def forward(self, x):
        x = self.backbone(**x).last_hidden_state
        y_hat = self.classifier(x.flatten(1))
        return y_hat
