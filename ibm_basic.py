import pymqi
import json



queue_manager = 'QMLAB1'
channel = 'QMLAB1.SVRCONN'
host = '127.0.0.1'
port = '1414'
conn_info = '%s(%s)' % (host, port)

qmgr = pymqi.connect(queue_manager, channel, conn_info)



pcf = pymqi.PCFExecute(qmgr)

attr1 = {
        pymqi.CMQC.MQCA_Q_NAME :'*',
        pymqi.CMQC.MQIA_Q_TYPE :pymqi.CMQC.MQQT_LOCAL,
        pymqi.CMQCFC.MQIACF_STATUS_TYPE:pymqi.CMQCFC.MQIACF_Q_STATUS,
        pymqi.CMQCFC.MQIACF_Q_STATUS_ATTRS:[pymqi.CMQCFC.MQCACF_LAST_GET_DATE,
                                            pymqi.CMQCFC.MQCACF_LAST_GET_TIME,
                                            pymqi.CMQCFC.MQCACF_LAST_PUT_DATE,
                                            pymqi.CMQCFC.MQCACF_LAST_PUT_TIME,
                                            pymqi.CMQCFC.MQIACF_OLDEST_MSG_AGE,
                                            pymqi.CMQCFC.MQIACF_UNCOMMITTED_MSGS]
    }

result1 = pcf.MQCMD_INQUIRE_Q_STATUS(attr1)



attr2= {
        pymqi.CMQC.MQCA_Q_NAME :'*',
}

result2 = pcf.MQCMD_INQUIRE_Q(attr2)


attr3={
        pymqi.CMQCFC.MQCACH_CHANNEL_NAME:"*",
        pymqi.CMQCFC.MQIACH_CHANNEL_INSTANCE_ATTRS : 
                                                   [pymqi.CMQCFC.MQCACH_CHANNEL_NAME, 
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

result3 = pcf.MQCMD_INQUIRE_CHANNEL_STATUS(attr3)





def listenerCollector():
        try:
                attr={
                        pymqi.CMQCFC.MQCACH_LISTENER_NAME:"*"
                }


                listener_responses=pcf.MQCMD_INQUIRE_LISTENER(attr)
                listener_name=""

                for response in listener_responses:
                        if response[pymqi.CMQCFC.MQCACH_LISTENER_NAME].decode('utf-8').strip()=='QMLAB1.LISTENER':
                                listener_name=response[pymqi.CMQCFC.MQCACH_LISTENER_NAME]
                
                attr2={
                        pymqi.CMQCFC.MQCACH_LISTENER_NAME:"*"

                }
                listenser_responses2=pcf.MQCMD_INQUIRE_LISTENER_STATUS(attr2)




        except Exception as e:
                print(str(e))


def QMgrCollector():
        try:
                attr={
                        pymqi.CMQCFC.MQIACF_Q_MGR_STATUS_ATTRS:[
                                pymqi.CMQCFC.MQIACF_CHINIT_STATUS,
                                pymqi.CMQCFC.MQIACF_CMD_SERVER_STATUS,
                                pymqi.CMQCFC.MQIACF_CONNECTION_COUNT,
                                pymqi.CMQCFC.MQIACF_Q_MGR_STATUS
                                

                        ]
                }
                qmgr_responses=pcf.CMQCFC.MQCMD_INQUIRE_Q_MGR_STATUS(attr)
                print(qmgr_responses[0][pymqi.CMQCFC.MQIACF_Q_MGR_STATUS])

                for response in qmgr_responses:
                        Qmgr_name=response[pymqi.CMQC.MQCA_Q_MGR_NAME]

                        if Qmgr_name.decode('utf-8').strip() == "QMLAB1":
                                print(response[pymqi.CMQCFC.MQIACF_CHINIT_STATUS])
                                print(response[pymqi.CMQCFC.MQIACF_CMD_SERVER_STATUS])
                                print(response[pymqi.CMQCFC.MQIACF_CONNECTION_COUNT])
                                print(response[pymqi.CMQCFC.MQIACF_Q_MGR_STATUS])



        except Exception as e:
                print(str(e))

QMgrCollector()
