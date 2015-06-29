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
        self.send_flow_mod(datapath) 
        self.logger.info("Flow has been added ")         #flowmod  function used to send in initial flow entries
	
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
    
    def send_group_mod(self, datapath):
        self.logger.info("Group Table has been added ")
    	ofp = datapath.ofproto
    	ofp_parser = datapath.ofproto_parser
        dpid = datapath.id
        if dpid == 1:
    	    port = 2
            port1 = 3
            max_len = 2000
    	    actions = [datapath.ofproto_parser.OFPActionSetField(eth_src="fe:16:3e:00:5c:17"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_dst="fe:16:3e:00:64:6f"),datapath.ofproto_parser.OFPActionOutput(port)]
            actions1 = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:5a:55"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:39:29"),datapath.ofproto_parser.OFPActionOutput(port1)]
            self.logger.info("Actions for A has been added ")
       	    weight = 100
            weight1 = 80
    	    watch_port = 2
    	    watch_group = 0
            watch_port1 = 3
    	    buckets = [ofp_parser.OFPBucket(weight, watch_port, watch_group,
                                    actions),ofp_parser.OFPBucket(weight1, watch_port1, watch_group, actions1)]
         
            self.logger.info("Buckets for A  has been added ")
    	    group_id = 1
            req1 = ofp_parser.OFPGroupMod(datapath, ofp.OFPGC_ADD,
                                 ofp.OFPGT_FF, group_id, buckets)
        
            self.logger.info("Req1 has been added ")
    	    datapath.send_msg(req1)
            self.logger.info("Group message for A has been added ")
       
             

        elif dpid == 4:
            port = 1
            port1 = 2
            max_len = 2000
    	    actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:73:9f"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:41:9d"),datapath.ofproto_parser.OFPActionOutput(port)]
            actions1 = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:47:96"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:54:95"),datapath.ofproto_parser.OFPActionOutput(port1)]
            self.logger.info("Actions for D has been added ")
       	    weight = 100
            weight1 = 80
    	    watch_port = 1
    	    watch_group = 0
            watch_port1 = 2
    	    buckets = [ofp_parser.OFPBucket(weight, watch_port, watch_group,
                                    actions),ofp_parser.OFPBucket(weight1, watch_port1, watch_group, actions1)]
         
            self.logger.info("Buckets for D has been added ")
    	    group_id = 2
            req1 = ofp_parser.OFPGroupMod(datapath, ofp.OFPGC_ADD,
                                 ofp.OFPGT_FF, group_id, buckets)
            self.logger.info("Req1  has been added ")
    	    datapath.send_msg(req1)
            self.logger.info("Group message for D has been added ")           
       
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
            group_id = 1
            
  	    self.logger.info("Flow added to switch A")
            matchit = ofp_parser.OFPMatch(in_port=1,ipv4_dst='10.0.1.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionGroup(group_id)]
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
	    self.logger.info("send_flow_mod has been added")
            self.send_group_mod(datapath)
            
            out_port1=1
	    self.logger.info("Flow added to switch A")
            matchit = ofp_parser.OFPMatch(in_port=2,ipv4_dst='10.0.0.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:29:c7"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:25:ed"),datapath.ofproto_parser.OFPActionOutput(out_port1)]  
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
	    self.logger.info("Flow added to switch B")
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
	elif dpid == 3:								#flowmod to switch C, adding flows from H1 to H2
            out_port1=1
  	    self.logger.info("Flow added to switch C")
            matchit = ofp_parser.OFPMatch(in_port=2,ipv4_dst='10.0.1.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:41:9d"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:73:9f"),datapath.ofproto_parser.OFPActionOutput(out_port1)]
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
	    out_port2=2								#flowmod to switch C, adding flows from H2 to H1
  	    self.logger.info("Flow added to switch C")
            matchit = ofp_parser.OFPMatch(in_port=1,ipv4_dst='10.0.0.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:17:3d"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:24:97"),datapath.ofproto_parser.OFPActionOutput(out_port2)]
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
	
	elif dpid == 4:								#flowmod to switch D, adding flows from H1 to H2
            group_id=2
  	    self.logger.info("Flow added to switch D")
            matchit = ofp_parser.OFPMatch(in_port=3,ipv4_dst='10.0.0.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionGroup(group_id)]
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
	    self.send_group_mod(datapath)

            out_port1=3
	    self.logger.info("Flow added to switch D")
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
	    out_port2=3						    
	    self.logger.info("Flow added to switch D")
            matchit = ofp_parser.OFPMatch(in_port=1,ipv4_dst='10.0.1.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:ba:e3"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:14:62"),datapath.ofproto_parser.OFPActionOutput(out_port2)]   
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
            out_port=1
  	    self.logger.info("Flow added to switch E")
            matchit = ofp_parser.OFPMatch(in_port=2,ipv4_dst='10.0.0.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:39:29"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:5a:55"),datapath.ofproto_parser.OFPActionOutput(out_port)] 
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
  	    self.logger.info("Flow added to switch E")
            matchit = ofp_parser.OFPMatch(in_port=1,ipv4_dst='10.0.1.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:4f:8f"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:3c:fb"),datapath.ofproto_parser.OFPActionOutput(out_port2)] 
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
            out_port=1
  	    self.logger.info("Flow added to switch F")
            matchit = ofp_parser.OFPMatch(in_port=2,ipv4_dst='10.0.1.1',eth_type=0x0800)
            actions = [datapath.ofproto_parser.OFPActionSetField(eth_dst="fe:16:3e:00:54:95"),datapath.ofproto_parser.OFPActionSetField   
                                    (eth_src="fe:16:3e:00:47:96"),datapath.ofproto_parser.OFPActionOutput(out_port)]
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
	
    
   
    	        


