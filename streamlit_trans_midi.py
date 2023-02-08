import streamlit as st 
from trans_scale_midi import trans_music
from mido import MidiFile
from io import StringIO,BytesIO
import os 

scale_file="scale.csv"
os.makedirs("temp",exist_ok=True)

# st.title("Midi音乐调式转换")
st.title("Midi Scale Transformation")
# st.write("## 上传midi文件")
st.write("## Upload midi file")
input_file = st.file_uploader("Choose a file",type=['mid'],accept_multiple_files=False)

if input_file is not None:
    midi_byte=input_file.getvalue()
    midi_file=MidiFile(file=BytesIO(midi_byte), clip=True)

st.write("## Choose Scale")

col1,col2=st.columns(2)

with col1:
    origin_scale_name = st.selectbox(
        'From Scale',
            ('Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian')
    )
    origin_root = st.selectbox(
        'From root',
            ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
    )
with col2:
    target_scale_name = st.selectbox(
        'To Scale',
            ('Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian'),
            index=5
    )
    target_root = st.selectbox(
        'To root',
            ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'),
            index=5
    )

button_trans=st.button("Transform")

if button_trans:
    output_file = target_scale_name+"_"+target_root+"_"+input_file.name
    output_file_with_path = os.path.join("temp",output_file)
    trans_music(midi_file,output_file_with_path,  
                    scale_file,
                    origin_scale_name,origin_root, 
                    target_scale_name, target_root)
    st.write("Complete!")
    # download output file
    download_button=st.download_button(
        label="Download File",
        data=open(output_file_with_path, 'rb').read(),
        file_name=output_file,
    )
    # 删除临时文件
    os.remove(output_file_with_path)

