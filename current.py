from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
import sys
array=[0,0,0,0,0,0,0]       #initiializing array so that we can store datapaths of differetn switches

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

 

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)			#switch features event. triggers flowmod entries
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
	index=datapath.id
	array[index]=datapath                              #storing datapaths in array on receiving the switch features
        print "This is datapath"
	print datapath.id
	print datapath
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        match = ofp_parser.OFPMatch()
        actions = [ofp_parser.OFPActionOutput(ofp.OFPP_CONTROLLER,
                                          ofp.OFPCML_NO_BUFFER)]
	empty_match = ofp_parser.OFPMatch()
        instructions = []
        self.remove_table_flows(datapath, 0, empty_match,instructions)
                
        self.add_flow(datapath, 0, match, actions)		#adding initial flow for tablemiss entry
	self.logger.info("Switch Feature Handling completed successfully ")
        self.send_flow_mod(datapath)                            #flowmod  function used to send in initial flow entries
	
    def remove_table_flows(self, datapath, table_id, match, instructions):
  	ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser
        flow_mod = ofp_parser.OFPFlowMod(datapath, 0, 0,table_id,
                                  ofp.OFPFC_DELETE, 0, 0,
                                  1,ofp.OFPCML_NO_BUFFER,
                                  ofp.OFPP_ANY,
                                  ofp.OFPG_ANY, 0,       
                                  match, instructions)
        print "deleting all flow entries in table "
        datapath.send_msg(flow_mod)


       
    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:

            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)
        self.logger.info("Added table miss entry ")
    def send_flow_mod(self, datapath):
        self.logger.info("Sending flowmod message ")
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser                             #giving  parameters like timeouts
        cookie = cookie_mask = 0
        table_id = 0
        idle_timeout = 0
        hard_timeout= 0
        priority = 6633 
        buffer_id = ofp.OFP_NO_BUFFER
        dpid = datapath.id
        if dpid == 1:								#flowmod to switch A, adding flows from H1 to H2
            out_port1=2
  	    self.logger.info("Flow added to switch A")
            matchit = ofp_parser.OFPMatch(in_port=1,ipv4_dst='10.0.1.1',eth_type=0x0800)
    	    actions = [datapath.ofproto_parser.OFPActionSetField(eth_src="fe:16:3e:00:5c:17"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_dst="fe:16:3e:00:64:6f"),datapath.ofproto_parser.OFPActionOutput(out_port1)]
 
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req1 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req1)
	    out_port2=1
  	    self.logger.info("Flow added to switch A")				      #flowmod to switch A, adding flows from H2 to H1
            matchit = ofp_parser.OFPMatch(in_port=2,ipv4_dst='10.0.0.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:29:c7"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:25:ed"),datapath.ofproto_parser.OFPActionOutput(out_port2)]
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req2 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req2)
	    
        elif dpid == 2:								#flowmod to switch B, adding flows from H1 to H2
            out_port1=2
	    self.logger.info("Flow added to switch B")
            matchit = ofp_parser.OFPMatch(in_port=1,ipv4_dst='10.0.1.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:24:97"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:17:3d"),datapath.ofproto_parser.OFPActionOutput(out_port1)] 
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req1 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst) 
            datapath.send_msg(req1)
	    out_port2=1							    #flowmod to switch B, adding flows from H2 to H1
	    self.logger.info("Flow added to switch B")
            matchit = ofp_parser.OFPMatch(in_port=2,ipv4_dst='10.0.0.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:5c:17"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:64:6f"),datapath.ofproto_parser.OFPActionOutput(out_port2)]  
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req2 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst) 
            datapath.send_msg(req2)
	elif dpid == 3:								
            out_port1=2						#flowmod to switch C, adding flows from H2 to H1
  	    self.logger.info("Flow added to switch C")
            matchit = ofp_parser.OFPMatch(in_port=1,ipv4_dst='10.0.0.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:17:3d"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:24:97"),datapath.ofproto_parser.OFPActionOutput(out_port1)]  
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req2 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
	    						#flowmod to switch C, adding flows from H1 to H2
            datapath.send_msg(req2)
            out_port2=1	
 	    self.logger.info("Flow added to switch C")
            matchit = ofp_parser.OFPMatch(in_port=2,ipv4_dst='10.0.1.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:41:9d"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:73:9f"),datapath.ofproto_parser.OFPActionOutput(out_port2)]  
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req1 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req1)
	
	elif dpid == 4:								#flowmod to switch D, adding flows from H1 to H2
            out_port1=3
  	    self.logger.info("Flow added to switch D")
            matchit = ofp_parser.OFPMatch(in_port=1,ipv4_dst='10.0.1.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:ba:e3"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:14:62"),datapath.ofproto_parser.OFPActionOutput(out_port1)]  
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req1 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req1)
	    out_port2=1								#flowmod to switch D, adding flows from H2 to H1
  	    self.logger.info("Flow added to switch D")
            matchit = ofp_parser.OFPMatch(in_port=3,ipv4_dst='10.0.0.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:73:9f"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:41:9d"),datapath.ofproto_parser.OFPActionOutput(out_port2)]  
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req2 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req2)
	elif dpid == 5:								#flowmod to switch E, adding flows from H1 to H2
            out_port1=2
  	    self.logger.info("Flow added to switch E")
            matchit = ofp_parser.OFPMatch(in_port=1,ipv4_dst='10.0.1.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:4f:8f"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:3c:fb"),datapath.ofproto_parser.OFPActionOutput(out_port1)]  
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req)
	    out_port2=1								#flowmod to switch E, adding flows from H2 to H1
  	    self.logger.info("Flow added to switch E")
            matchit = ofp_parser.OFPMatch(in_port=2,ipv4_dst='10.0.0.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:39:29"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:5a:55"),datapath.ofproto_parser.OFPActionOutput(out_port2)] 
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req2 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req2)
	elif dpid == 6:								#flowmod to switch F, adding flows from H1 to H2
            out_port1=1
  	    self.logger.info("Flow added to switch F")
            matchit = ofp_parser.OFPMatch(in_port=2,ipv4_dst='10.0.1.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:54:95"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:47:96"),datapath.ofproto_parser.OFPActionOutput(out_port1)] 
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req)
	    out_port2=2								#flowmod to switch F, adding flows from H2 to H1
  	    self.logger.info("FLow added to switch F")
            matchit = ofp_parser.OFPMatch(in_port=1,ipv4_dst='10.0.0.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:3c:5b"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:4f:8f"),datapath.ofproto_parser.OFPActionOutput(out_port2)] 
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req2 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req2)
	
    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)			#Port status change event
    def port_status_handler(self, ev):
    		msg = ev.msg
    		dp = msg.datapath
		dpid = dp.id 							
    		ofp = dp.ofproto 
                port_no = msg.desc.port_no
		state=msg.desc.state
		print state
		print "Port Status message"					
                self.logger.info("This is the Port no")
                print port_no
		print dpid							
 		if msg.reason == ofp.OFPPR_MODIFY:
			if dp.id==2 or dp.id==3:				# if link is down on switch A or B
				self.send_flow_linkdown(array[1])		#flowmod for A
				self.send_flow_linkdown(array[4])		#flowmod for D
			elif dp.id==5 or dp.id==6:
				self.send_flow_linkdownback(array[1])
                                self.send_flow_linkdownback(array[4])
                        elif dp.id==1: 
                                if port_no==3:
                                        print "Port 1 of switch A is down"
                                	self.send_flow_linkdown(array[1])
                                	self.send_flow_linkdown(array[4])
                                elif port_no==2:
                                        print "Port 2 of switch A is down"
                                	self.send_flow_linkdownback(array[1])
                                 	self.send_flow_linkdownback(array[4])
                                else:
                                	self.logger.info("Connectivity to the Host is lost")
       			elif dp.id==4: 
                                if port_no==1:
                                	self.send_flow_linkdown(array[1])
                                	self.send_flow_linkdown(array[4])
                                elif port_no==2:
                                	self.send_flow_linkdownback(array[1])
                                 	self.send_flow_linkdownback(array[4])
                                else:
                                	self.logger.info("Connectivity to the Host is lost")
                        
    def send_flow_linkdown(self,datapath):
   	self.logger.info("Alternate path being established ")
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser
        cookie = cookie_mask = 0
        table_id = 0
        idle_timeout = 0
        hard_timeout= 0
        priority = 6633 
        buffer_id = ofp.OFP_NO_BUFFER
        dpid = datapath.id
        print dpid
	if dpid==1:					#checking to see if flows have to be modified in switch A or switch D
	    out_port1=2
	    self.logger.info("I am changing A")
  	    self.logger.info("Flow removed from switch A")  #flowmod to switch A, deleting flows from H1 to H2
            matchit = ofp_parser.OFPMatch(in_port=1,ipv4_dst='10.0.1.1',eth_type=0x0800)
    	    actions = [datapath.ofproto_parser.OFPActionSetField(eth_src="fe:16:3e:00:5c:17"),   
                       datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:64:6f"),
                       datapath.ofproto_parser.OFPActionOutput(out_port1)]                                       
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req1 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_DELETE,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req1)
	    out_port2=1                                 #flowmod to switch A, deleting flows from H2 to H1
  	    self.logger.info("Flow removed from switch A")				  
            matchit = ofp_parser.OFPMatch(in_port=2,ipv4_dst='10.0.0.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:29:c7"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:25:ed"),datapath.ofproto_parser.OFPActionOutput(out_port2)]
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req2 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_DELETE,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req2)
            out_port1=3
  	    self.logger.info("Alternate flow for A added")				#Alternate flow for A being added, H1 to H2
            matchit = ofp_parser.OFPMatch(in_port=1,ipv4_dst='10.0.1.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:5a:55"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:39:29"),datapath.ofproto_parser.OFPActionOutput(out_port1)]
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req1 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req1)
	    out_port2=1
  	    self.logger.info("Alternate flow for A added")				#Alternate flow for A being added, H2 to H1
            matchit = ofp_parser.OFPMatch(in_port=3,ipv4_dst='10.0.0.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:29:c7"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:25:ed"),datapath.ofproto_parser.OFPActionOutput(out_port2)]
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req2 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req2)
	elif dpid==4:								#checking to see if flows have to be modified in switch D
	    out_port1=3	
	    self.logger.info("I am changing D")						#flowmod to switch D, deleting flows from H1 to H2
  	    self.logger.info("Flow removed from switch D")
            matchit = ofp_parser.OFPMatch(in_port=1,ipv4_dst='10.0.1.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:ba:e3"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:14:62"),datapath.ofproto_parser.OFPActionOutput(out_port1)]
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req1 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_DELETE,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req1)
	    out_port2=1							#flowmod to switch D, deleting flows from H2 to H1
  	    self.logger.info("Flow removed from switch D")
            matchit = ofp_parser.OFPMatch(in_port=3,ipv4_dst='10.0.0.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:73:9f"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:41:9d"),datapath.ofproto_parser.OFPActionOutput(out_port2)]
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req2 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_DELETE,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req2)
	    out_port1=3
  	    self.logger.info("Alternate flow for D added")			#Alternate flow for D being added, H1 to H2
            matchit = ofp_parser.OFPMatch(in_port=2,ipv4_dst='10.0.1.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:ba:e3"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:14:62"),datapath.ofproto_parser.OFPActionOutput(out_port1)]
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req1 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
	    datapath.send_msg(req1)
	    out_port2=2
  	    self.logger.info("Alternate flow for D added")			#Alternate flow for D being added, H2 to H1
            matchit = ofp_parser.OFPMatch(in_port=3,ipv4_dst='10.0.0.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:47:96"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:54:95"),datapath.ofproto_parser.OFPActionOutput(out_port2)]
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req2 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
	    datapath.send_msg(req2)
  

    def send_flow_linkdownback(self,datapath):
	
	self.logger.info("Alternate path being established ")
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser
        cookie = cookie_mask = 0
        table_id = 0
        idle_timeout = 0
        hard_timeout= 0
        priority = 6633 
        buffer_id = ofp.OFP_NO_BUFFER
        dpid = datapath.id
        print dpid
	if dpid==1:
	    	out_port1=3
  	    	self.logger.info("flow for A deleted")				#Flow for A being deleted, H1 to H2
            	matchit = ofp_parser.OFPMatch(in_port=1,ipv4_dst='10.0.1.1',eth_type=0x0800)
                actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:5a:55"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:39:29"),datapath.ofproto_parser.OFPActionOutput(out_port1)]
            	inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            	req1 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_DELETE,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            	datapath.send_msg(req1)
	    	out_port2=1
  	    	self.logger.info("Flow for A deleted")				#Flow for A being deleted, H2 to H1
            	matchit = ofp_parser.OFPMatch(in_port=3,ipv4_dst='10.0.0.1',eth_type=0x0800)
                actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:29:c7"),datapath.ofproto_parser.OFPActionSetField
                                    (eth_src="fe:16:3e:00:25:ed"),datapath.ofproto_parser.OFPActionOutput(out_port2)]
            	inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            	req2 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_DELETE,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            	datapath.send_msg(req2)
	    	out_port1=2     #flowmod to switch A ,adding flows from H1 to H2
  	    	self.logger.info("Alternate Flow added to switch A")
            	matchit = ofp_parser.OFPMatch(in_port=1,ipv4_dst='10.0.1.1',eth_type=0x0800)
                actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:64:6f"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:5c:17"),datapath.ofproto_parser.OFPActionOutput(out_port1)]            
            	inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            	req1 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            	datapath.send_msg(req1)
	    	out_port2=1
  	    	self.logger.info("Alternate Flow added to switch A")		     #flowmod to switch A, adding flows from H2 to H1
            	matchit = ofp_parser.OFPMatch(in_port=2,ipv4_dst='10.0.0.1',eth_type=0x0800)
                actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:29:c7"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:25:ed"),datapath.ofproto_parser.OFPActionOutput(out_port2)]
            	inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            	req2 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            	datapath.send_msg(req2)
	elif dpid==4:
	    out_port1=3
  	    self.logger.info("flow for D deleted")			#flow for D being deleted, H1 to H2
            matchit = ofp_parser.OFPMatch(in_port=2,ipv4_dst='10.0.1.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:ba:e3"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:14:62"),datapath.ofproto_parser.OFPActionOutput(out_port1)]
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req1 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_DELETE,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
	    datapath.send_msg(req1)
	    out_port2=2
  	    self.logger.info("flow or D deleted")			#flow for D being deleted, H2 to H1
            matchit = ofp_parser.OFPMatch(in_port=3,ipv4_dst='10.0.0.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:47:96"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:54:95"),datapath.ofproto_parser.OFPActionOutput(out_port2)]
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req2 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_DELETE,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
	    datapath.send_msg(req2)

 	    out_port1=3							#flowmod to switch D, adding flows from H1 to H2
  	    self.logger.info("Flow added to switch D")
            matchit = ofp_parser.OFPMatch(in_port=1,ipv4_dst='10.0.1.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:ba:e3"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:14:62"),datapath.ofproto_parser.OFPActionOutput(out_port1)]
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req1 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req1)
	    out_port2=1							#flowmod to switch D, adding flows from H2 to H1
  	    self.logger.info("Flow added from switch D")
            matchit = ofp_parser.OFPMatch(in_port=3,ipv4_dst='10.0.0.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:73:9f"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:41:9d"),datapath.ofproto_parser.OFPActionOutput(out_port2)]
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                         actions)]
            req2 = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
                                   table_id, ofp.OFPFC_ADD,
                                   idle_timeout, hard_timeout,
                                   priority, buffer_id,
                                   ofp.OFPP_ANY, ofp.OFPG_ANY,
                                   ofp.OFPFF_SEND_FLOW_REM,
                                   matchit, inst)
            datapath.send_msg(req2)				
 
    	        


