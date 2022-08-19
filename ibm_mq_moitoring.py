import json
from collections import OrderedDict

"""
MQCHSSTATE_OTHER = 0
MQCHSSTATE_END_OF_BATCH = 100
MQCHSSTATE_SENDING = 200
MQCHSSTATE_RECEIVING = 300
MQCHSSTATE_SERIALIZING = 400
MQCHSSTATE_RESYNCHING = 500
MQCHSSTATE_HEARTBEATING = 600
MQCHSSTATE_IN_SCYEXIT = 700
MQCHSSTATE_IN_RCVEXIT = 800
MQCHSSTATE_IN_SENDEXIT = 900
MQCHSSTATE_IN_MSGEXIT = 1000
MQCHSSTATE_IN_MREXIT = 1100
MQCHSSTATE_IN_CHADEXIT = 1200
MQCHSSTATE_NET_CONNECTING = 1250
MQCHSSTATE_SSL_HANDSHAKING = 1300
MQCHSSTATE_NAME_SERVER = 1400
MQCHSSTATE_IN_MQPUT = 1500
MQCHSSTATE_IN_MQGET = 1600
MQCHSSTATE_IN_MQI_CALL = 1700
MQCHSSTATE_COMPRESSING = 1800
"""

metrics=[

# Queue Metrics
"Queue Name",
"Current Queue Depth",
"Handles Open : Input Count",
"Handles Open : Output Count",
"Last Msg get Date",
"Last Msg get Time",
"Last Msg put Date",
"Last Msg put Time",
"Oldest Msg Age",
"No. of Uncommitted Msgs",

# Channel Metrics
"Channel Name",
"Channel Connection Name",
"Channel Status",
"No. of MQI calls",
"Bytes Sent",
"Bytes Received",
"Buffers Sent",
"Buffers Received",
"Channel Substate"
"Channel Start Date",
"Channel Start Time"
]



class IbmMq:

        def __init__(self,conf_details):
                self.maindata={}
                self.queue_manager,self.channel,self.host,self.port=conf_details
                self.conn_info='%s(%s)' % (self.host, self.port)
                self.main()




        def main(self):


                try:
                        global pymqi
                        import pymqi
                        self.mqConnector()


                except Exception as e:
                        self.maindata['status']=0
                        self.maindata['msg']=str(e)
                        

        def metricCollector(self):

        
                self.queueCollector()
                self.channelCollector()
                self.QMgrCollector()
                return self.maindata



                


        def mqConnector(self):

                try:
                        self.qmgr = pymqi.connect(self.queue_manager, self.channel, self.conn_info)
                        self.pcf = pymqi.PCFExecute(self.qmgr)
                        self.metricCollector()
                        
                except Exception as e:
                        
                        self.maindata['status']=0
                        self.maindata['msg']=str(e)



        def QMgrCollector(self):
                try:

                        Queue_manager_status=["","STARTING","RUNNING","QUIESCING","STANDBY"]
                        attr={
                                pymqi.CMQCFC.MQIACF_Q_MGR_STATUS_ATTRS:[
                                        pymqi.CMQCFC.MQIACF_CHINIT_STATUS,
                                        pymqi.CMQCFC.MQIACF_CMD_SERVER_STATUS,
                                        pymqi.CMQCFC.MQIACF_CONNECTION_COUNT,
                                        pymqi.CMQCFC.MQIACF_Q_MGR_STATUS
                                        

                                ]
                        }
                        qmgr_responses=self.pcf.CMQCFC.MQCMD_INQUIRE_Q_MGR_STATUS(attr)
                        print(qmgr_responses[0][pymqi.CMQCFC.MQIACF_Q_MGR_STATUS])

                        for response in qmgr_responses:
                                Qmgr_name=response[pymqi.CMQC.MQCA_Q_MGR_NAME]

                                if Qmgr_name.decode('utf-8').strip() == "QMLAB1":
                                        self.maindata["QManager_metrics.Connection_count"]=response[pymqi.CMQCFC.MQIACF_CONNECTION_COUNT]
                                        self.maindata["QManager_metrics.Status"]=Queue_manager_status[response[pymqi.CMQCFC.MQIACF_Q_MGR_STATUS]]



                except Exception as e:
                        self.maindata['status']=0
                        self.maindata['msg']=str(e)                        

        def queueCollector(self):

                try:



                        
                        attr1= {

                                pymqi.CMQC.MQCA_Q_NAME :'*',
                        }
                        queue_responses1 = self.pcf.MQCMD_INQUIRE_Q(attr1)

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
                        queue_responses2 = self.pcf.MQCMD_INQUIRE_Q_STATUS(attr2)

                        queue_responses3=self.pcf.MQCMD_RESET_Q_STATS(attr1)




                        



                        for response in queue_responses1:
                                queue_name = response[pymqi.CMQC.MQCA_Q_NAME]

                                if queue_name.decode("utf-8").strip()=="ORDER.INPUT":

                                        self.maindata["Queue_Metrics.Queue Name"]= queue_name.decode("utf-8").strip()
                                        self.maindata["Queue_Metrics.Current Queue Depth"]=response[pymqi.CMQC.MQIA_CURRENT_Q_DEPTH]
                                        self.maindata["Queue_Metrics.Max Queue Depth"]=response[pymqi.CMQC.MQIA_MAX_Q_DEPTH]
                                        self.maindata["Queue_Metrics.Handles Open(Input Count)"]=response[pymqi.CMQC.MQIA_OPEN_INPUT_COUNT]
                                        self.maindata["Queue_Metrics.Handles Open(Output Count)"]=response[pymqi.CMQC.MQIA_OPEN_OUTPUT_COUNT]
                                        break

                        for response in queue_responses2:
                                queue_name = response[pymqi.CMQC.MQCA_Q_NAME]

                                if queue_name.decode("utf-8").strip()=="ORDER.INPUT":
                        
                                        self.maindata["Queue_Metrics.Last Msg get Date"]=response[pymqi.CMQCFC.MQCACF_LAST_GET_DATE].decode("utf-8")
                                        self.maindata["Queue_Metrics.Last Msg get Time"]=response[pymqi.CMQCFC.MQCACF_LAST_GET_TIME].decode("utf-8")
                                        self.maindata["Queue_Metrics.Last Msg put Date"]=response[pymqi.CMQCFC.MQCACF_LAST_PUT_DATE].decode("utf-8")
                                        self.maindata["Queue_Metrics.Last Msg put Time"]=response[pymqi.CMQCFC.MQCACF_LAST_PUT_TIME].decode("utf-8")
                                        self.maindata["Queue_Metrics.Oldest Msg Age"]=response[pymqi.CMQCFC.MQIACF_OLDEST_MSG_AGE]
                                        self.maindata["Queue_Metrics.No. of Uncommitted Msgs"]=response[pymqi.CMQCFC.MQIACF_UNCOMMITTED_MSGS]
                                        break
 
                        for response in queue_responses3:
                                queue_name = response[pymqi.CMQC.MQCA_Q_NAME]

                                if queue_name.decode("utf-8").strip()=="ORDER.INPUT":    
                                        self.maindata["Queue_Metrics.High Queue Depth"]=response[pymqi.CMQC.MQIA_HIGH_Q_DEPTH]
                                        self.maindata["Queue_Metrics.Msg Dequeue Count"]=response[pymqi.CMQC.MQIA_MSG_DEQ_COUNT]
                                        self.maindata["Queue_Metrics.Msg Enqueue Count"]=response[pymqi.CMQC.MQIA_MSG_ENQ_COUNT]

                                        
                        




                except Exception as e:
                        self.maindata['status']=0
                        self.maindata['msg']=str(e)
                        return self.maindata
        



        def channelCollector(self):

                try:

                        channel_statuses=["Channel Inactive","Channel Binding", "Channel Starting", "Channel Running", "Channel Stopping", "Channel Retrying", "Channel Stopped", "Channel Requesting", "Channel Paused", "Channel Disconnected", "Channel Initializing", "Channel Switching"]
                        channel_substate={
                                0:"Undefined State",
                                100:"End of batch processing",
                                200:"Network send",
                                300:"Network receive",
                                400:"Serialized on queue manager access",
                                500:"Resynching with partner",
                                600:"Heartbeating with partner",
                                700:"Running security exit",
                                800:"Running receive exit",
                                900:"Running send exit",
                                1000:"Running message exit",
                                1100:"Running retry exit",
                                1200:"Running channel auto-definition exit",
                                1250:"Network connect",
                                1300:"SSL Handshaking",
                                1400:"Name server request",
                                1500:"Performing MQPUT",
                                1600:"Performing MQGET",
                                1700:"Executing IBM MQ API call",
                                1800:"Compressing or decompressing data"
                                }
                        




                        attr={
                                pymqi.CMQCFC.MQCACH_CHANNEL_NAME:"*",
                                pymqi.CMQCFC.MQIACH_CHANNEL_INSTANCE_ATTRS : 
                                                        [ 
                                                        pymqi.CMQCFC.MQCACH_CHANNEL_NAME, 
                                                        pymqi.CMQCFC.MQCACH_CONNECTION_NAME, 
                                                        pymqi.CMQCFC.MQIACH_CHANNEL_STATUS, 
                                                        pymqi.CMQCFC.MQIACH_MSGS,
                                                        pymqi.CMQCFC.MQIACH_BYTES_SENT,
                                                        pymqi.CMQCFC.MQIACH_BYTES_RECEIVED,
                                                        pymqi.CMQCFC.MQIACH_BUFFERS_SENT,
                                                        pymqi.CMQCFC.MQIACH_BUFFERS_RECEIVED,
                                                        pymqi.CMQCFC.MQIACH_INDOUBT_STATUS,
                                                        pymqi.CMQCFC.MQIACH_CHANNEL_SUBSTATE,
                                                        pymqi.CMQCFC.MQCACH_CHANNEL_START_DATE,
                                                        pymqi.CMQCFC.MQCACH_CHANNEL_START_TIME
                                                        ]}
                        

                        channel_responses=self.pcf.MQCMD_INQUIRE_CHANNEL_STATUS(attr)

                        for channel_response in channel_responses:
                                channel_name=channel_response[pymqi.CMQCFC.MQCACH_CHANNEL_NAME]
                                if channel_name.decode('utf-8').strip()=="QMLAB1.SVRCONN":
                                        self.maindata["Channel_Metrics.Channel Name"]=channel_name.decode('utf-8').strip()
                                        self.maindata["Channel_Metrics.Channel Connection Name"]=channel_response[pymqi.CMQCFC.MQCACH_CONNECTION_NAME].decode('utf-8').strip()
                                        self.maindata["Channel_Metrics.Channel Status"]=channel_statuses[channel_response[pymqi.CMQCFC.MQIACH_CHANNEL_STATUS]]
                                        self.maindata["Channel_Metrics.No. of MQI calls"]=channel_response[pymqi.CMQCFC.MQIACH_MSGS]
                                        self.maindata["Channel_Metrics.Bytes Sent"]=channel_response[pymqi.CMQCFC.MQIACH_BYTES_SENT]
                                        self.maindata["Channel_Metrics.Bytes Received"]=channel_response[pymqi.CMQCFC.MQIACH_BYTES_RECEIVED]
                                        self.maindata["Channel_Metrics.Buffers Sent"]=channel_response[pymqi.CMQCFC.MQIACH_BUFFERS_SENT]
                                        self.maindata["Channel_Metrics.Buffers Received"]=channel_response[pymqi.CMQCFC.MQIACH_BUFFERS_RECEIVED]

                                        substate_data=channel_response[pymqi.CMQCFC.MQIACH_CHANNEL_SUBSTATE]
                                        self.maindata["Channel_Metrics.Channel Substate"]=channel_substate.get(substate_data)
                                        self.maindata["Channel_Metrics.Channel Start Date"]=channel_response[pymqi.CMQCFC.MQCACH_CHANNEL_START_DATE].decode('utf-8')
                                        self.maindata["Channel_Metrics.Channel Start Time"]=channel_response[pymqi.CMQCFC.MQCACH_CHANNEL_START_TIME].decode('utf-8')
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

