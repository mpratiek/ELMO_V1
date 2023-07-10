import urllib.request
from urllib.request import urlopen
from PIL import Image
import timm
import torch
import json
import argparse
import io

def main():

    parser = argparse.ArgumentParser(description="timm example")
    parser.add_argument("--model_name",dest="model_name")
    parser.add_argument("--image_path",dest="image_path")
    parser.add_argument("--class_path",dest="class_path")
    args = parser.parse_args()

    print(args.model_name)
    print(args.image_path)


    model = timm.create_model(args.model_name, pretrained=True)
    model = model.eval()

    # get model specific transforms (normalization, resize)
    data_config = timm.data.resolve_model_data_config(model)
    transforms = timm.data.create_transform(**data_config, is_training=False)

    img = Image.open(args.image_path)

    output = model(transforms(img).unsqueeze(0))  # unsqueeze single image into batch of 1
    top5_probabilities, top5_class_indices = torch.topk(output.softmax(dim=1) * 100, k=5)

    top1_class = top5_class_indices[0][0].item()
    top1_prob = top5_probabilities[0][0].item()

    with open(args.class_path,"r") as f:
        categories = [s.strip() for s in f.readlines()]
    output = {"predicted": categories[top1_class], "confidence": top1_prob}
    print(json.dumps(output))

if __name__ == "__main__":
    main()


