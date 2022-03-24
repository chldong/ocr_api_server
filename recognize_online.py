#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-
"""
使用自建的接口识别来自网络的验证码
需要配置参数：
    remote_url = "https://www.xxxxxxx.com/getImg"  验证码链接地址
    rec_times = 1  识别的次数
"""
import datetime
import requests
import time
import os
# import json
# import base64
# from PIL import Image
# from io import BytesIO
# from calendar import c


def recognize_captcha(remote_url, rec_times, save_path, image_suffix):
    # image_file_name = 'captcha.{}'.format(image_suffix)

    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }

    for index in range(rec_times):
        # 请求
        while True:
            try:
                response = requests.request("GET", remote_url, headers=headers, timeout=6)

                if response.text:
                    break
                else:
                    print("retry, response.text is empty")
            except Exception as ee:
                print(ee)

        # 转换
        # text = response.text
        # print(text)
        # jsonobj = json.loads(text)
        # imgt = jsonobj['Img']
        # print(imgt)
        # img=base64.b64decode(imgt)
        # imgs = open(image_file_name,"wb")
        # imgs.write(img)
        # imgs.close()
      
        # 获取
        code_img = requests.get(url=remote_url,headers=headers).content
        # 保存
        # with open(image_file_name,'wb') as fp:
        #     fp.write(code_img)
        
        # 识别
        s = time.time()
        url = "http://localhost:9898/ocr/file"
        files = {'image': code_img}
        r = requests.post(url=url, files=files)
        e = time.time()
        # print(r.text)
        # 识别结果
        # print("识别结果: {}".format(r.text))
        # predict_text = json.loads(r.text)["value"]
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("【{}】 次数:{} 耗时：{}ms 预测：{}".format(now_time, index, int((e-s)*1000), r.text))

        # 以预测结果为名称保存文件
        img_name = "{}_{}.{}".format(r.text, str(time.time()).replace(".", ""), image_suffix)
        path = os.path.join(save_path, img_name)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        with open(path, "wb") as f:
            f.write(code_img)
        print("======================")


def main():
    # with open("conf/config.json", "r") as f:
    #     sample_conf = json.load(f)
    # save_path = sample_conf["online_image_dir"]  # 下载图片保存的地址
    # remote_url = sample_conf["remote_url"]  # 网络验证码地址
    # image_suffix = sample_conf["image_suffix"]  # 文件后缀
    # 配置相关参数
    save_path = 'online'  # 下载图片保存的地址
    remote_url = 'http://captcha.qq.com/getimage?aid=2000201&uin=0&0.22020985170895468'  # 网络验证码地址
    image_suffix = 'jpeg'  # 文件后缀
    rec_times = 9
    recognize_captcha(remote_url, rec_times, save_path, image_suffix)


if __name__ == '__main__':
    main()
    

