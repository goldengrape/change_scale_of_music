# %% [markdown]
# 对音乐的调式scale进行变换

# %%
import numpy as np
from mido import MidiFile
import argparse


# %% [markdown]
# ## 数字音高与音名的转换

# %%
note_num={"C":0, "Db":1, "D":2, "Eb":3,"E":4, "F":5, "Gb":6,
"G":7, "Ab":8, "A":9, "Bb":10, "B":11,}
num_note={v:k for k,v in note_num.items()}

# %%
# Conversion of digital pitch and sound names

def pitch_to_name(pitch, root):
    root_num=note_num[root]+60 
    pitch_num=pitch-root_num
    octave=pitch_num//12+4
    pitch_num=pitch_num%12
    return num_note[pitch_num], octave

def name_to_pitch(name, octave, root):
    root_num=note_num[root]+60
    pitch_num=note_num[name]+12*(octave-4)
    return pitch_num+root_num


# %% [markdown]
# ## Scale的重映射
# 
# 对于major/Ionian：
# 
# * 音高是
#   * [C,D,E,F,G,A,B]
#   * [0,2,4,5,7,9,11]
#    
# 对于minor/Aeolian 
# * 音高是
#   * [C,D,Eb,F,G,Ab,Bb]
#   * [0,2,3, 5,7,8,10]
# 
# 重映射时：
# 
# |原scale|原音高|新scale|新音高|
# |:--|:--|:--|:--|
# |E|4|Eb|3|
# |A|9|Ab|8|
# |B|11|Bb|10|
# 
# 整体：
# 
# |序数|0|-|1|-|2|3|-|4|-|5|-|6|
# |:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|
# |Ionian|0|1|2|3|4|5|6|7|8|9|10|11|
# |Aeolian|0|1|2|-|3|5|6|7|-|8|-|10|

# %%


# %% [markdown]
# |序数  | 0|   1|  2|  3|  4|  5|  6|
# |:--   |:--|:--|:--|:--|:--|:--|:--|
# |Ionian|        C|  D|  E|  F|  G|  A|  B|
# |Aeolian|       C|  D| Eb|  F|  G| Ab| Bb|
# |Dorian|        C|  D| Eb|  F|  G|  A| Bb|
# |Phrygian|      C| Db| Eb|  F|  G| Ab| Bb|
# |Lydian|        C|  D|  E| Gb|  G|  A|  B|
# |Mixolydian|    C|  D|  E|  F|  G|  A| Bb|
# |Locrian|       C| Db| Eb|  F| Gb| Ab| Bb|

# %%
def read_scale(scale_file):
    with open(scale_file, "r") as f:
        text=f.read()
        text=text.replace(" ", "")
        text=text.split("\n")
        text=[t.split(",") for t in text]
        scale_dict={t[0].upper():t[1:] for t in text}
    return scale_dict

# %%
def note_to_index(note, scale):
    scale_num = np.asarray([note_num[x] for x in scale])
    if note in scale:
        return scale.index(note)
    else:
        x=np.count_nonzero(note_num[note] > np.array(scale_num))-0.5 
        return x 

# %%
def trans_scale(note, scale_origin, scale_target):
    origin_note_index= note_to_index(note, scale_origin)
    if int(origin_note_index) == origin_note_index:
        target_note=scale_target[origin_note_index]
    else:
        # 如果序数不为整数，取上下两个音符的平均值
        lower_note_index=int(origin_note_index)
        if lower_note_index < len(scale_target)-1:
            upper_note_index=lower_note_index+1
            lower_note=scale_target[lower_note_index]
            upper_note_index=int(origin_note_index)+1
            upper_note=scale_target[upper_note_index]
            target_note_num=np.round((note_num[lower_note]+note_num[upper_note])/2)
            target_note=num_note[target_note_num]
        else:
            # if over the last note, take the average of last note and B
            target_note_num=np.round((note_num[scale_target[-1]]+11)/2)
            target_note=num_note[target_note_num]
    return target_note

# %% [markdown]
# # 读取并遍历midi文件

# %%
def trans_music(mid, output_file,
                scale_file, 
                origin_scale_name, origin_root, 
                target_scale_name, target_root):
                
    scale=read_scale(scale_file)
    origin_scale=scale[origin_scale_name.upper()]
    target_scale=scale[target_scale_name.upper()]
    
    # mid = MidiFile(input_file, clip=True)
    for track in mid.tracks:
        for msg in track:
            if (msg.type=='note_on'):
                origin_name,origin_octave=pitch_to_name(msg.note, origin_root)
                target_name=trans_scale(origin_name,origin_scale, target_scale)
                target_pitch=name_to_pitch(target_name,origin_octave,target_root)
                msg.note=target_pitch
    mid.save(output_file)
    return True  




# %% [markdown]
# ## CLI

# %%

def arg_parse():
    '''
    解析命令行参数
    '''
    # 创建解析步骤
    parser = argparse.ArgumentParser(description='更改midi音乐的调式')

    # 添加参数步骤
    parser.add_argument('-i','--input',type=str, help='输入的midi文件名' )
    parser.add_argument('-o','--output', type=str, default='', help='输出的midi文件名')
    parser.add_argument('-s', '--scale', type=str, default="scale.csv", help='调式定义文件')               
    parser.add_argument('-is','--input_scale', type=str,help='原曲的调式名称')               
    parser.add_argument('-os','--output_scale', type=str,help='输出的调式名称')               
    parser.add_argument('-ir','--input_root', type=str,help='原曲的root名称')               
    parser.add_argument('-or','--output_root', type=str,help='输出的root名称') 

    # 解析参数步骤  
    args = parser.parse_args()
    return(args)

# %%
# scale_file="scale.csv"
# origin_scale_name="Ionian"
# origin_root="D"
# target_scale_name="Lydian"
# target_root="D"

# input_file="Canon_in_D.mid"
# output_file="Canon_in_D_Lydian.mid"
if __name__ == "__main__":
    args=arg_parse()

    scale_file=args.scale
    origin_scale_name=args.input_scale
    origin_root=args.input_root
    target_scale_name=args.output_scale
    target_root=args.output_root
    input_file=args.input
    output_file=args.output

    trans_music(input_file,output_file,  
                scale_file,
                origin_scale_name,origin_root, 
                target_scale_name, target_root);


# %%



