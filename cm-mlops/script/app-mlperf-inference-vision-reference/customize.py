from cmind import utils
import os
import json
import shutil

def preprocess(i):

    os_info = i['os_info']
    env = i['env']
    #print(i['state'])
    if 'CM_LOADGEN_EXTRA_OPTIONS' not in env:
        env['CM_LOADGEN_EXTRA_OPTIONS'] = ""
    if 'CM_LOADGEN_MODE' not in env:
        env['CM_LOADGEN_MODE'] = "performance"
    elif env['CM_LOADGEN_MODE'] == "accuracy":
        env['CM_LOADGEN_EXTRA_OPTIONS'] += " --accuracy"

    if 'CM_LOADGEN_QPS' not in env:
        env['CM_LOADGEN_QPS_OPT'] = ""
    else:
        env['CM_LOADGEN_QPS_OPT'] = " --qps " + env['CM_LOADGEN_QPS']
    if 'CM_LOADGEN_SCENARIO' not in env:
        env['CM_LOADGEN_SCENARIO'] = "Offline"
    env['CM_LOADGEN_EXTRA_OPTIONS'] +=  env['CM_LOADGEN_QPS_OPT']
    if 'OUTPUT_BASE_DIR' not in env:
        env['OUTPUT_BASE_DIR'] = env['CM_MLC_INFERENCE_VISION_PATH']
    if 'OUTPUT_DIR' not in env:
        env['OUTPUT_DIR'] =  os.path.join(env['OUTPUT_BASE_DIR'], "results", env['CM_BACKEND'] + "-" + env['CM_DEVICE'], env['CM_MODEL'],
        env['CM_LOADGEN_SCENARIO'].lower(), env['CM_LOADGEN_MODE'])

    if 'CM_MLC_USER_CONF' not in env:
        env['CM_MLC_USER_CONF'] = os.path.join(env['CM_MLC_INFERENCE_VISION_PATH'], "user.conf")
    if 'CM_MLC_MLPERF_CONF' not in env:
        env['CM_MLC_MLPERF_CONF'] = os.path.join(env['CM_MLC_INFERENCE_SOURCE'], "mlperf.conf")

    env['CM_LOADGEN_EXTRA_OPTIONS'] +=  " --mlperf_conf " + env['CM_MLC_MLPERF_CONF']
    env['CM_LOADGEN_EXTRA_OPTIONS'] +=  " --user_conf " + env['CM_MLC_USER_CONF']

    return {'return':0}

def postprocess(i):
    os_info = i['os_info']
    env = i['env']

    measurements = {}
    measurements['retraining'] = env.get('CM_MODEL_RETRAINING','')
    measurements['input_data_types'] = env.get('CM_MODEL_INPUT_DATA_TYPES','fp32')
    measurements['weight_data_types'] = env.get('CM_MODEL_WEIGHT_DATA_TYPES','fp32')
    measurements['weight_transformations'] = env.get('CM_MODEL_WEIGHT_TRANSFORMATIONS','none')
    os.chdir(env['OUTPUT_DIR'])
    with open ("measurements.json", "w") as fp:
        json.dump(measurements, fp, indent=2)
    if os.path.exists(env['CM_MLC_MLPERF_CONF']):
        shutil.copy(env['CM_MLC_MLPERF_CONF'], 'mlperf.conf')
    if os.path.exists(env['CM_MLC_USER_CONF']):
        shutil.copy(env['CM_MLC_USER_CONF'], 'user.conf')

    return {'return':0}