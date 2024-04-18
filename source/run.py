# +
import os
from tqdm import tqdm
from argparse import ArgumentParser
from GFVC.utils import read_config_file


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--config", type=str, help="Path to codec configuration file")
    parser.add_argument("--dataset_config", type=str, default=None,help="Path to codec configuration file")
    opt = parser.parse_args()
    args = read_config_file(opt.config)
    if opt.dataset_config is not None:
        dataset_args = read_config_file(opt.dataset_config)
        seqlist= dataset_args['seq_list'] 
        Sequence_dir=dataset_args['sequence_dir'] 
    else:
        seqlist= args['seq_list'] 
        Sequence_dir=args['sequence_dir'] 
        

    frames = args['num_frames']
    testingdata_name=args['dataset']
    model_name=args['codec_name']
    quantization_factor=args['quantization_factor']
    

    qplist= args['qp_list'] 
    if model_name in ['DAC']:
        ref_codec = args['ref_codec']
    if model_name in ['HDAC','HDAC_Extension']:
        ref_codec = args['ref_codec']
        bl_qplist = args['base_layer_params']['qp']

 
    
    gop_size = args['gop_size']

    #Input Frame dimensions
    height=args['height'] #256
    width=args['width'] #256
  
    coding_mode=args['inference_mode'] 
    iframe_format=args['iframe_format']  

    for qp in qplist:
        for seq in tqdm(seqlist):
            original_seq=Sequence_dir+testingdata_name+'_'+str(seq)+'_'+str(width)+'x'+str(height)+'_25_8bit_444.rgb'
            cmd = "./run.sh "+model_name+" "+coding_mode+" "+original_seq+" "+str(frames)+" "+str(quantization_factor)+" "+str(qp)+" "+str(iframe_format) +" "
            if model_name in ['FOMM','CFTE', 'FV2V']:
                cmd += " "+str(gop_size)
                os.system(cmd) 
                print(model_name+"_"+coding_mode+"_"+testingdata_name+"_"+seq+"_QP"+str(qp)+" Finished")
            elif model_name in ['DAC']:
                cmd +=ref_codec+ " "+ args['adaptive_metric'] + " " + str(args['adaptive_thresh']) + " " + str(args['num_kp'])+" "
                cmd += " "+str(gop_size)
                os.system(cmd) 
                print(model_name+"_"+coding_mode+"_"+testingdata_name+"_"+seq+"_QP"+str(qp)+" Finished")
            elif model_name in ['HDAC', 'HDAC_Extension']:
                for blqp in bl_qplist:
                 
                    cmd_blqp = cmd + ref_codec+ " "+ args['adaptive_metric'] + " " + str(args['adaptive_thresh']) + " " + str(args['num_kp'])+" "
                    cmd_blqp +=  args['base_layer_params']['use_base_layer'] + " "+ args['base_layer_params']['base_codec'] + " "+ str(blqp) + " " + str(args['base_layer_params']['scale_factor'])
                    cmd_blqp += " "+str(gop_size)
                    # print(cmd_blqp)
                    # sys.exit()
                    os.system(cmd_blqp) 
            
                    print(model_name+"_"+coding_mode+"_"+testingdata_name+"_"+seq+"_Keyframe QP"+str(qp)+"_Base_layer_QP_"+str(blqp)+" Finished")
            
