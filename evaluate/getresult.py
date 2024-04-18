# +
# get file size in python
import os
import numpy as np



Inputformat='Iframe_YUV420' # 'RGB444' OR 'YUV420'
testingdata_name='CFVQA' # 'CFVQA' OR 'VOXCELEB'
Model='FV2V'             ## 'FV2V' OR 'FOMM' OR 'CFTE' 
Metric = 'lpips' ## 'psnr' 'dists' 'lpips' 'ssim'
# txt_path='../experiment/'+Model+'/'+Inputformat+'/evaluation-YUV420/'+testingdata_name+'_result_'+Metric+'.txt'
txt_path='../experiment/'+Model+'/'+Inputformat+'/evaluation/'+testingdata_name+'_result_'+Metric + '.txt'
# txt_path = '/home/ysz/GFVC/experiment/FV2V/Iframe_YUV420/resultBit/CFVQA_resultBit.txt'


with open(txt_path, 'r') as file:
    # content = file.read()
    for line in file: 
        words=line.split()
        for num in range(4):
            if Metric in ['psnr','ssim']:
                print(words[num])
            elif Metric in ['lpips','dists']:
                print(1-float(words[num]))

    
    
