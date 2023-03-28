import torch
import torchvision.transforms as standard_transforms
import numpy as np

from PIL import Image
import cv2
from p2pnet.engine import *
from p2pnet.models import build_model
import os
import warnings

warnings.filterwarnings("ignore")


def infer_p2pnet(img_path: str):
    args = {
        "backbone": "vgg16_bn",
        "gpu_id": 0,
        "weight_path": "p2pnet/weights/SHTechA.pth",
        "output_dir": "p2pnet/logs/",
        "row": 2,
        "line": 2,
    }

    os.environ["CUDA_VISIBLE_DEVICES"] = "{}".format(args["gpu_id"])
    device = torch.device("cuda")
    model = build_model(args)
    model.to(device)

    # load trained model
    if args["weight_path"] is not None:
        checkpoint = torch.load(args["weight_path"], map_location="cpu")
        model.load_state_dict(checkpoint["model"])

    # convert to eval mode
    model.eval()

    # create the pre-processing transform
    transform = standard_transforms.Compose(
        [
            standard_transforms.ToTensor(),
            standard_transforms.Normalize(
                mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
            ),
        ]
    )

    # load the images
    img_raw = Image.open(img_path).convert("RGB")

    # round the size
    width, height = img_raw.size
    new_width = width // 128 * 128
    new_height = height // 128 * 128
    img_raw = img_raw.resize((new_width, new_height), Image.ANTIALIAS)

    # pre-proccessing
    img = transform(img_raw)

    samples = torch.Tensor(img).unsqueeze(0)
    samples = samples.to(device)

    # run inference
    outputs = model(samples)
    outputs_scores = torch.nn.functional.softmax(outputs["pred_logits"], -1)[:, :, 1][0]
    outputs_points = outputs["pred_points"][0]
    threshold = 0.5

    # filter the predictions
    points = outputs_points[outputs_scores > threshold].detach().cpu().numpy().tolist()
    predict_cnt = int((outputs_scores > threshold).sum())
    outputs_scores = torch.nn.functional.softmax(outputs["pred_logits"], -1)[:, :, 1][0]
    outputs_points = outputs["pred_points"][0]

    # draw the predictions
    size = 2
    img_to_draw = cv2.cvtColor(np.array(img_raw), cv2.COLOR_RGB2BGR)
    for p in points:
        img_to_draw = cv2.circle(
            img_to_draw, (int(p[0]), int(p[1])), size, (0, 0, 255), -1
        )

    # save the visualized image
    cv2.imwrite(
        os.path.join(args["output_dir"], "pred{}.jpg".format(predict_cnt)), img_to_draw
    )

    return predict_cnt