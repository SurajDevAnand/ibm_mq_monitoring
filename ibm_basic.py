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

result2 = pcf.MQCMD_INQUIRE_CONNECTIONS(attr2)


for queue_info in result2:
        queue_name = queue_info[pymqi.CMQC.MQCA_Q_NAME]

        if queue_name.decode("utf-8").strip()=="ORDER.INPUT":

                print(queue_name)
                print(queue_info[pymqi.CMQC.MQIA_CURRENT_Q_DEPTH])
                print(queue_info[pymqi.CMQC.MQIA_OPEN_INPUT_COUNT])
                print(queue_info[pymqi.CMQC.MQIA_OPEN_OUTPUT_COUNT])
                print(queue_info[pymqi.CMQC.MQIA_Q_TYPE])
                break



for queue_info in result1:
        queue_name = queue_info[pymqi.CMQC.MQCA_Q_NAME]

        if queue_name.decode("utf-8").strip()=="ORDER.INPUT":
        
                print(queue_info[pymqi.CMQCFC.MQCACF_LAST_GET_DATE])
                print(queue_info[pymqi.CMQCFC.MQCACF_LAST_GET_TIME])
                print(queue_info[pymqi.CMQCFC.MQCACF_LAST_PUT_DATE])
                print(queue_info[pymqi.CMQCFC.MQCACF_LAST_PUT_TIME])
                print(queue_info[pymqi.CMQCFC.MQIACF_OLDEST_MSG_AGE])
                print(queue_info[pymqi.CMQCFC.MQIACF_UNCOMMITTED_MSGS])
