This is GFVC Software_v2
# Implementation Codes
We optimize the implemention codes of three representative GFVC works, i.e., [FOMM](https://github.com/AliaksandrSiarohin/first-order-model), [CFTE](https://github.com/Berlin0610/CFTE_DCC2022) and [FV2V](https://github.com/zhanglonghao1992/One-Shot_Free-View_Neural_Talking_Head_Synthesis), and further provide the unified codes regarding the encoder and decoder processes.
Current extensions to the original code include [DAC](https://ieeexplore.ieee.org/document/9414731) and [HDAC](https://github.com/Goluck-Konuko/animation-based-codecs)

+ Download the `CFTE-checkpoint.pth.tar`, `FOMM-checkpoint.pth.tar`, and `FV2V-checkpoint.pth.tar` to the path `./GFVC/CFTE/checkpoint/`, `./GFVC/FOMM/checkpoint/`, `./GFVC/FV2V/checkpoint/` , `./GFVC/DAC/checkpoint/` and  `./GFVC/HDAC/checkpoint/`respectively.
+ The checkpoints for FOMM, CFTE and FV2V are available at [this link](https://portland-my.sharepoint.com/:u:/g/personal/bolinchen3-c_my_cityu_edu_hk/EZ3rHarhkzhMisnJDTM7XOYBIH0lVI2jrdOK_xn_mj-tVg?e=KHfCa0) while DAC and HDAC are available [here](https://drive.google.com/drive/folders/1DHbGHgJk4s1799B-CuFXM87XcuNnosCa?usp=sharing). Please use `DAC-10-checkpoint.pth.tar` as DAC model.

+ The overall testing dataset in **RGB444** domain is available at [this link](https://portland-my.sharepoint.com/:f:/g/personal/bolinchen3-c_my_cityu_edu_hk/En0W90hNlrZLokuzGb67lgIBMqeHSIZZHff95ZyI0-WG7g?e=1cx4ZG).
+ The overall testing dataset in **YUV420** domain is available at [this link](https://portland-my.sharepoint.com/:f:/g/personal/bolinchen3-c_my_cityu_edu_hk/Emy2k26BY1VKoeXwxTWlPtoB8Z6kM62g3eEl0uyyuKjLfQ?e=wFzKjn).
+ The specific details can be seen in the subfolder `source`.
+ The code can be launched by running `'python run.py' --config ../config/{model}.yaml` under 'source/' fold after specifying all setting in configs under 'config/{model}.yaml'
