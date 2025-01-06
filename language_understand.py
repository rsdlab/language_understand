#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file language_understand.py
 @brief ModuleDescription
 @date $Date$


"""
# </rtc-template>

import sys
import os
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

# add module
import openai
import yaml

home_path = os.environ['HOME']
file_path = home_path+'/apikey.yml'
with open(file_path, 'r') as file:
    data = yaml.safe_load(file)

# OpenAI APIキーの設定
openai.api_key = data['key']

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
language_understand_spec = ["implementation_id", "language_understand", 
         "type_name",         "language_understand", 
         "description",       "ModuleDescription", 
         "version",           "1.0.0", 
         "vendor",            "rsdlab", 
         "category",          "Category", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         "conf.default.judge", "false",

         "conf.__widget__.judge", "text",

         "conf.__type__.judge", "string",

         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class language_understand
# @brief ModuleDescription
# 
# 
# </rtc-template>
class language_understand(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_data_in = OpenRTM_aist.instantiateDataType(RTC.TimedWString)
        """
        """
        self._data_inIn = OpenRTM_aist.InPort("data_in", self._d_data_in)
        self._d_data_out = OpenRTM_aist.instantiateDataType(RTC.TimedWString)
        """
        """
        self._data_outOut = OpenRTM_aist.OutPort("data_out", self._d_data_out)
        self._d_speech_text = OpenRTM_aist.instantiateDataType(RTC.TimedWString)
        """
        """
        self._speech_textOut = OpenRTM_aist.OutPort("speech_text", self._d_speech_text)


		


        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
        """
        
         - Name:  judge
         - DefaultValue: false
        """
        self._judge = ['false']
		
        # </rtc-template>


		 
    ##
    #
    # The initialize action (on CREATED->ALIVE transition)
    # 
    # @return RTC::ReturnCode_t
    # 
    #
    def onInitialize(self):
        # Bind variables and configuration variable
        self.bindParameter("judge", self._judge, "false")
		
        # Set InPort buffers
        self.addInPort("data_in",self._data_inIn)
		
        # Set OutPort buffers
        self.addOutPort("data_out",self._data_outOut)
        self.addOutPort("speech_text",self._speech_textOut)
		
        # Set service provider to Ports
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports
		
        return RTC.RTC_OK
	

    def onActivated(self, ec_id):
    
        return RTC.RTC_OK
	

    def onDeactivated(self, ec_id):
    
        return RTC.RTC_OK
	

    def onExecute(self, ec_id):
        if self._data_inIn.isNew(): 
            print("come")
            self._d_data_in=self._data_inIn.read()
            text = self._d_data_in.data
            print(text)

            judgement=chat(text)
            print("結果")
            print(judgement)

            self._d_speech_text.data=judgement
            self._d_data_out.data=judgement

            if "体調は「良い」" in judgement or "体調は「悪い」" in judgement:
                self._speech_textOut.write()
                self._data_outOut.write()
                
                
            else:
                self._d_data_out.data = text
                self._data_outOut.write()


            print("ok")

        return RTC.RTC_OK
	

	
use_model = 'gpt-4'

ChatSetting = '''
以下のようにルールを設定します．
与えられたテキストを元に、ユーザーの体調が「良い」or「悪い」かを判断して教えてください。
必ずルールを守ってください．
'''

def chat(text):
    print('\r' + '　'*10 + '\r', end='')
    print('\nChatGPT:')
    response = openai.ChatCompletion.create(
        model=use_model,
        messages=[
            {"role": "system",
             "content": ChatSetting},
            {"role": "user",
             "content": text},
        ],
        max_tokens=1024,
        n=1,
        stream=True,
        temperature=0.5,
        stop=None,
        presence_penalty=0.5,
        frequency_penalty=0.5
    )

    fullResponse = ""
    RealTimeResponse = ""   
    senN = 0
    sentences = []
    sentenceHistory = ""

    for chunk in response:
        text = chunk['choices'][0]['delta'].get('content')
        if(text==None):
            pass
        else:
            fullResponse += text
            RealTimeResponse += text
            # print(text, end='', flush=True) # 部分的なレスポンスを随時表示していく

            target_char = ["。", "！", "？"]

            for index, char in enumerate(RealTimeResponse):
                if char in target_char:
                    pos = index + 2        # 区切り位置
                    sentence = RealTimeResponse[:pos]           # 1文の区切り
                    RealTimeResponse = RealTimeResponse[pos:]   # 残りの部分
                    
                    '''
                    if outputtype == 'sound':
                        # loop = asyncio.get_event_loop()
                        # loop.run_in_executor(None, streamprint, sentence, pos, 'ChatGPT') # 投げっぱなし. fire and forget.
                        speech(sentence, senN , filename , language ,Player_check)

                    else:
                        for i in range(0,len(sentence)):
                            print(sentence[i], end='', flush=True)
                            time.sleep(0.05)
                    '''
                            
                    sentences.append(sentence)
                    sentenceHistory += sentence
                    senN = senN +1

                    break
                else:
                    pass

    return sentenceHistory
	


def language_understandInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=language_understand_spec)
    manager.registerFactory(profile,
                            language_understand,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    language_understandInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("language_understand" + args)

def main():
    # remove --instance_name= option
    argv = [i for i in sys.argv if not "--instance_name=" in i]
    # Initialize manager
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()

if __name__ == "__main__":
    main()

