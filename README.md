Backend for crowd counting

Initialization:

```
conda create -y -n py372 python=3.7
conda activate py372

conda install -y pytorch==1.5.1 torchvision==0.6.1 cudatoolkit=10.2 -c pytorch
conda install -y -c menpo opencv
conda install -y -c anaconda scipy

pip install fastapi uvicorn
pip install uvloop==0.14.0
```

To run:

```
uvicorn main:app --reload
```
