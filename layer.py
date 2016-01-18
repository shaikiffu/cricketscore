from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity

import json
import urllib2

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #send receipt otherwise we keep receiving the same message over and over
        if messageProtocolEntity.getBody().lower()=="score":
            response=urllib2.urlopen("http://cricscore-api.appspot.com/csa")
            #get the json
            response=response.read()
            #covert to python format 
            response=json.loads(response)
            
            #url to receive score of all the matches
            main_url="https://cricscore-api.appspot.com/csa?id="
            for r in response:
                match_id=str(r["id"])
                if r==response[0]:
                    main_url+=match_id
                else:
                    main_url=main_url+'+'+match_id

            #receive the jason which contains data of all the matches and extract info
            all_matches=json.loads(urllib2.urlopen(main_url).read())
            count=0
            answer=""
            for match in all_matches :
                count+=1
                first=str(match["de"])
                second=str(match["si"])
                answer=answer+str(count)+") "+first+"\n \n"+second+"\n \n"
            
        else:
            answer="notcha"
        if True:
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())

            outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                answer,
                to = messageProtocolEntity.getFrom())

            self.toLower(receipt)
            self.toLower(outgoingMessageProtocolEntity)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)
