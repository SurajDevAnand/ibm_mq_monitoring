import json
from collections import OrderedDict


metrics=[

"Queue Name",
"Current Queue Depth",
"Handles Open : Input Count",
"Handles Open : Output Count",

]



class IbmMq:

        def __init__(self,conf_details):
                self.maindata={}
                self.queue_manager,self.channel,self.host,self.port=conf_details
                self.conn_info='%s(%s)' % (self.host, self.port)




        def metricCollector(self):


                try:
                        global pymqi
                        import pymqi
                        self.mqConnector()
                        return self.maindata


                except Exception as e:
                        self.maindata['status']=0
                        self.maindata['msg']=str(e)
                        return self.maindata

                
                


        def mqConnector(self):

                try:
                        self.qmgr = pymqi.connect(self.queue_manager, self.channel, self.conn_info)
                        self.pcf = pymqi.PCFExecute(self.qmgr)
                        self.queueCollector()
                        
                except Exception as e:
                        
                        self.maindata['status']=0
                        self.maindata['msg']=str(e)
                        return self.maindata

        def queueCollector(self):

                try:

                        attr2 = {

                        pymqi.CMQC.MQCA_Q_NAME :'*',
                        pymqi.CMQC.MQIA_Q_TYPE :pymqi.CMQC.MQQT_LOCAL,
                        pymqi.CMQCFC.MQIACF_STATUS_TYPE:pymqi.CMQCFC.MQIACF_Q_STATUS,
                        pymqi.CMQCFC.MQIACF_Q_STATUS_ATTRS:
                                [
                                 pymqi.CMQCFC.MQCACF_LAST_GET_DATE,
                                 pymqi.CMQCFC.MQCACF_LAST_GET_TIME,
                                 pymqi.CMQCFC.MQCACF_LAST_PUT_DATE,
                                 pymqi.CMQCFC.MQCACF_LAST_PUT_TIME,
                                 pymqi.CMQCFC.MQIACF_OLDEST_MSG_AGE,
                                 pymqi.CMQCFC.MQIACF_UNCOMMITTED_MSGS ]
                        }
                        responses2 = self.pcf.MQCMD_INQUIRE_Q_STATUS(attr2)


                        
                        attr1= {

                                pymqi.CMQC.MQCA_Q_NAME :'*',
                        }
                        responses1 = self.pcf.MQCMD_INQUIRE_Q(attr1)



                        for response in responses1:
                                queue_name = response[pymqi.CMQC.MQCA_Q_NAME]

                                if queue_name.decode("utf-8").strip()=="ORDER.INPUT":

                                        self.maindata["Queue Name"]= queue_name.decode("utf-8").strip()
                                        self.maindata["Current Queue Depth"]=response[pymqi.CMQC.MQIA_CURRENT_Q_DEPTH]
                                        self.maindata["Handles Open : Input Count"]=response[pymqi.CMQC.MQIA_OPEN_INPUT_COUNT]
                                        self.maindata["Handles Open : Output Count"]=response[pymqi.CMQC.MQIA_OPEN_OUTPUT_COUNT]
                                        break

                        for response in responses2:
                                queue_name = response[pymqi.CMQC.MQCA_Q_NAME]

                                if queue_name.decode("utf-8").strip()=="ORDER.INPUT":
                        
                                        self.maindata["Last Msg get Date"]=response[pymqi.CMQCFC.MQCACF_LAST_GET_DATE].decode("utf-8")
                                        self.maindata["Last Msg get Time"]=response[pymqi.CMQCFC.MQCACF_LAST_GET_TIME].decode("utf-8")
                                        self.maindata["Last Msg put Date"]=response[pymqi.CMQCFC.MQCACF_LAST_PUT_DATE].decode("utf-8")
                                        self.maindata["Last Msg put Time"]=response[pymqi.CMQCFC.MQCACF_LAST_PUT_TIME].decode("utf-8")
                                        self.maindata["Oldest Msg Age"]=response[pymqi.CMQCFC.MQIACF_OLDEST_MSG_AGE]
                                        self.maindata["No. of Uncommitted Msgs"]=response[pymqi.CMQCFC.MQIACF_UNCOMMITTED_MSGS]
                                        break

                except Exception as e:
                        self.maindata['status']=0
                        self.maindata['msg']=str(e)
                        return self.maindata


                


if __name__=="__main__":

        queue_manager = 'QMLAB1'
        channel = 'QMLAB1.SVRCONN'
        host = '127.0.0.1'
        port = '1414'

        conf_details=[queue_manager,channel,host,port]
        ibm_obj=IbmMq(conf_details)
        ibm_mq_metric_data=ibm_obj.metricCollector()
        print(json.dumps(ibm_mq_metric_data,indent=True))