from flask import Flask,request,send_file
import qrcode
import os
import pathlib
from pathlib import Path
script_directory = pathlib.Path(__file__).parent.resolve()

template = """BEGIN:VCARD
VERSION:4.0
N:{last_name};{first_name}.;
ORG:{company}
TEL;TYPE#mobile,voice;VALUE#uri:tel:{mobile_phone}
TEL;TYPE#work,voice;VALUE#uri:tel:{work_phone}
ADR;TYPE#WORK;PREF#1:{work_address_line_1};{work_address_city};{work_address_stage_code};{work_address_pin};{work_address_country}
EMAIL:{email}
URL:{url}
REV:20080424T195243Z
x-qq:21588891
END:VCARD"""

def create_qr_code_image(qr_code_data,file_path):
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(qr_code_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="blue", back_color="white")
    img.save(file_path)

app= Flask(__name__)

@app.route("/result",methods=["POST","GET"])
def result():
    output =request.get_json()
    patho=os.path.join(script_directory,'qrs')
    path_dir=Path(patho)
    if path_dir.is_dir():
        filen=filen=patho+'/'+output['last_name']+'_'+output['company']+'.png'
    else:
        os.mkdir(patho)
        filen=patho+'/'+output['last_name']+'_'+output['company']+'.png'
    

    if len(output.keys()) <3:
        return {"status":"Bad Response"}
    else: 
        qdata=template.format(**output)
        create_qr_code_image(
        qr_code_data=qdata,file_path=filen)
        return send_file(filen)
        
        # return send_file(filen)

    


if __name__=='__main__':
    app.run(debug=True,port=2000)



