import os
import time
import yaml 

def read_config_file(config_path):
    '''Simply reads a yaml configuration file'''
    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

############################Please Specify Your Configuration Here########################################

#dataset params 
RGB_SEQ_DIR = '/home/ysz/datasets/testing_sequence_30/'  ###You should download the testing sequence and modify the dir.
YUV_SEQ_DIR = '/home/ysz/datasets/testing_sequence_30_yuv420/'
SEQ_LIST = ['001','002','003','004','005','006','007','008','009','010','011','012','013','014','015'] #


#execution params 
PATH_TO_SOURCE = '/home/ysz/GFVC_Software_v2/source/'
PATH_TO_EVAL = '/home/ysz/GFVC_Software_v2/evaluate/'

DATASETS = ['VOXCELEB','CFVQA']

# MODELS = ['CFTE','FV2V','FOMM','DAC','HDAC','HDAC_Extension']
MODELS = ['DAC','HDAC','HDAC_Extension']


ENCODE = True
DECODE = True
EVALUATE = True
RGB2YUV = True
EVAL_RGB = True
EVAL_YUV = True
SUMMARY_RESULTS = True

###########################################################################################################

os.chdir(PATH_TO_SOURCE)
dataset_config = {
 'sequence_dir':RGB_SEQ_DIR,
 'yuv_sequence_dir':YUV_SEQ_DIR,
 'seq_list':SEQ_LIST,
}
dataset_config_path = "../config_all/dataset_config.yaml"
with open(dataset_config_path, "w") as f:
    yaml.dump(dataset_config, f)



if ENCODE:
    print('Encoding........')
    for dataset in DATASETS:
        for model in MODELS:
            config_path = '../config_all/'+model+"_"+dataset+"_enc.yaml"
            os.system("python run.py --config "+ config_path + ' --dataset_config '+dataset_config_path)
if DECODE:
    print('Decoding........')
    for dataset in DATASETS:
        for model in MODELS:
            config_path = '../config_all/'+model+"_"+dataset+"_dec.yaml"
            os.system("python run.py --config "+ config_path + ' --dataset_config '+dataset_config_path)

os.chdir(PATH_TO_EVAL)
if EVALUATE:
    print('Evaluating........')
    
    if RGB2YUV:
        print('RGB to YUV converting........')
        for dataset in DATASETS:
            for model in MODELS:
                config_path = '../config_all/'+model+"_"+dataset+"_dec.yaml"
                os.system("python rgb444_to_yuv420.py --config "+ config_path + ' --dataset_config '+dataset_config_path)
    if EVAL_RGB:
        print('RGB quality evaluation........')
        for dataset in DATASETS:
            for model in MODELS:
                config_path = '../config_all/'+model+"_"+dataset+"_dec.yaml"
                os.system("python metrics.py --config "+ config_path + ' --dataset_config '+dataset_config_path)
    if EVAL_YUV:
        print('YUV quality evaluation........')
        for dataset in DATASETS:
            for model in MODELS:
                config_path = '../config_all/'+model+"_"+dataset+"_dec.yaml"
                os.system("python multiMetric_yuv420.py --config "+ config_path + ' --dataset_config '+dataset_config_path)

if SUMMARY_RESULTS:
    print('Summarizing evaluation results')
    for dataset in DATASETS:
        for model in MODELS:
            config_path = '../config_all/'+model+"_"+dataset+"_dec.yaml"
            os.system("python bitrate.py --config "+ config_path + ' --dataset_config '+dataset_config_path)
    tim = time.localtime()
    
    
    for model in MODELS:
        summary_path = os.path.join('../experiment/',str(tim[0])+'-'+str(tim[1]).zfill(2)+'-'+str(tim[2]).zfill(2)+'T'+str(tim[3]).zfill(2)+'-'+str(tim[4]).zfill(2)+'-'+str(tim[5]).zfill(2)+'-'+model+'-EvaluationSummary.txt')
        with open(summary_path, 'a') as f:
            for dataset in DATASETS:
                config_path = '../config_all/'+model+"_"+dataset+"_dec.yaml"
                args = read_config_file(config_path)
                Metrics = args['metrics'] 
                Iframe_format=args['iframe_format'] 
                if model in ['HDAC']:
                    qp_iter = args['base_layer_params']['qp']
                else:
                    qp_iter = args['qp_list'] 

                f.write('########## '+model+'_'+dataset+'_Bitrate '+'##########'+ '\n')
                bitrate_path = '../experiment/'+model+'/Iframe_'+Iframe_format+'/resultBit/'+dataset+'_resultBit.txt'
                with open(bitrate_path, 'r') as bitrate_result:
                    for line in bitrate_result.readlines()[:-1]: 
                        words=line.split()
                        for num in range(len(qp_iter)):
                            f.write(words[num]+ '\n')
            
                for metric in Metrics:
                    rgb_result_path='../experiment/'+model+'/Iframe_'+Iframe_format+'/evaluation/'+dataset+'_result_'+metric + '.txt'
                    f.write('########## '+model+'_'+dataset+'_RGB444_'+metric+' ##########'+ '\n')
                    with open(rgb_result_path, 'r') as rgb_result:
                        for line in rgb_result.readlines()[:-1]: 
                            words=line.split()
                            for num in range(len(qp_iter)):
                                if metric in ['dists','lpips']:
                                    f.write(str(1-float(words[num]))+ '\n')
                                else:
                                    f.write(words[num]+ '\n')

                for metric in ['psnr','ssim']:
                    yuv_result_path='../experiment/'+model+'/Iframe_'+Iframe_format+'/evaluation-YUV420/'+dataset+'_result_'+metric+'.txt'
                    f.write('########## '+model+'_'+dataset+'_YUV420_'+metric+' ##########'+ '\n')
                    with open(yuv_result_path, 'r') as yuv_result:
                        for line in yuv_result.readlines()[:-1]: 
                            words=line.split()
                            for num in range(len(qp_iter)):
                                f.write(words[num]+ '\n')

os.remove(dataset_config_path)
print('Done!')


                
             
