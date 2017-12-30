import json
import copy



#parse request to two part of get operator and set operator
#
#paraments:
#   request       the request from counter
#   unknown_flag  the symbol to identify unknown field
#
#return:
#   get_request   get operator from coutner
#   set_request   set opeartor from counter
def parse_request(request, unknown_flag = -1):
    #             (available flag, value)
    get_request = (False, None)
    set_request = (False, None)
    
    if request == unknown_flag:
        get_request = (True, unknown_flag)
        set_request = (False, None)

    elif type(request) not in (list, dict):
        get_request = (False, None)
        set_request = (True, request)

    elif type(request) == list:
        set_request = []
        for v in request:
            _, sub_set_request = parse_request(v, unknown_flag)
            if sub_set_request[0]:
                set_request.append(sub_set_request[1])
        if len(set_request) > 0:
            set_request = (True, set_request)
        else:
            set_request = (False, None)

    elif type(request) == dict:
        get_request = {}
        set_request = {}
        for k, v in request.items():
            sub_get_request, sub_set_request = parse_request(v, unknown_flag)
            if sub_get_request[0]:
                get_request[k] = sub_get_request[1]
            if sub_set_request[0]:
                set_request[k] = sub_set_request[1]
        if len(get_request.keys()) > 0:
            get_request = (True, get_request)
        else:
            get_request = (False, None)
        set_request = (True, set_request)
        
    return get_request, set_request



def __sync_get_request(self_copy, get_request):
    if type(self_copy) != type(get_request) or type(get_request) not in (dict, ):
        return copy.deepcopy(self_copy)
    elif type(get_request) == dict:
        request = {}
        for k, v in get_request.items():
            if k in self_copy:
                request[k] = __sync_get_request(self_copy[k], v)
        return request

#generate response from get request
#
#paraments:
#   self_copy     the original state table 
#   get_request   get operator from coutner
#
#return:
#   response      the response need to be sent to counter, None means don't need to send anymore
def sync_get_request(self_copy, get_request):
    if get_request[0] is not True:
        return None
    return __sync_get_request(self_copy, get_request[1])


def __sync_set_request(self_copy, set_request):
    if type(self_copy) != type(set_request) or type(set_request) not in (dict,):
        return copy.deepcopy(set_request)
    elif type(set_request) == dict:
        if len(set_request.items()) == 0:
            self_copy = {}
        else:
            self_copy = copy.deepcopy(self_copy)
        for k, v in set_request.items():
            if k in self_copy:
                self_copy[k] = __sync_set_request(self_copy[k], v)
            else:
                self_copy[k] = copy.deepcopy(v)
        return self_copy
    return None

#update original state table from set request
#
#paraments:
#   self_copy     the original state table 
#   set_request   set opeartor from counter
#
#return:
#   state table   new self state table need to be updated
def sync_set_request(self_copy, set_request):
    if set_request[0] is not True:
        return self_copy
    return __sync_set_request(self_copy, set_request[1])




#synchronization of state table between counter and self
#
#paraments:
#   self_copy     self state table
#   request       the request from counter
#   unknown_flag(any)   the symbol to identify unknown field
#
#return:
#   response      the response need to be sent to counter, None means don't need to send anymore
#   self_copy     new self state table need to be updated
def sync_request(self_copy, request, unknown_flag = -1):
    get_request, set_request = parse_request(request, unknown_flag)
    response = sync_get_request(self_copy, get_request)
    self_copy = sync_set_request(self_copy, set_request)
    return response, self_copy



















if __name__ == "__main__":
    # the current state table of this PC   
    state_table = '''
        {
        "ff-ff-ff-ff-ff-ff": {
            "power": 0,
            "push_stream_info": {
                "[屏幕]-[1001]":{
                    "state": 0,
                    "address": ""
                },
                "[教师]-[1001]":{
                    "state": 0,
                    "address": ""
                },
                "[学生]-[1001]":{
                    "state": 0,
                    "address": ""
                }
            },
            "pull_stream_info": {
            },
            "state": {
                "cpu": {
                    "usage": {
                            "2017-12-20 9:54:01":0.2,
                            "2017-12-20 9:54:02":0.37
                        }
                    },
                "memory": {
                    "usage": {
                        "2017-12-20 9:54:01":0.2,
                        "2017-12-20 9:54:02":0.37
                    }
                }
            }
        },
        "type":0
    }    
    '''
    state_table = json.loads(state_table)
    
    print '------------------init state---------------------'
    print json.dumps(state_table, sort_keys=True)

    #wake up PC (update power)
    print '\n\n\n-----------------wake up PC (update power)----------------------'
    request = '''
        {
            "ff-ff-ff-ff-ff-ff":
            {
                "power":1
            }, 
            "type":0
        }
    '''
    request = json.loads(request)
    response, state_table = sync_request(state_table, request)

    print 'reponse : '
    print json.dumps(response, sort_keys=True)
    print 'current state : '
    print json.dumps(state_table, sort_keys=True)


    #query PC state of CPU usage
    print '\n\n\n-----------------query PC state of CPU usage----------------------'
    request = '''
        {
            "ff-ff-ff-ff-ff-ff":
            {
                "state":
                {
                    "cpu":
                    {
                        "usage":-1
                    }
                }
            }, 
            "type":0
        }
    '''
    request = json.loads(request)
    response, state_table = sync_request(state_table, request)

    print 'reponse : '
    print json.dumps(response, sort_keys=True)
    print 'current state : '
    print json.dumps(state_table, sort_keys=True)

    


    #query PC state of CPU usage
    print '\n\n\n-----------------query PC state of CPU usage----------------------'
    request = '''
        {
            "ff-ff-ff-ff-ff-ff":
            {
                "state":
                {
                    "cpu":
                    {
                        "usage":-1
                    }
                }
            }, 
            "type":0
        }
    '''
    request = json.loads(request)
    response, state_table = sync_request(state_table, request)

    print 'reponse : '
    print json.dumps(response, sort_keys=True)
    print 'current state : '
    print json.dumps(state_table, sort_keys=True)

    #query all of PC state
    print '\n\n\n-----------------query all of PC state----------------------'
    request = '''
        {
            "ff-ff-ff-ff-ff-ff":
            {
                "state":-1
            }, 
            "type":0
        }
    '''
    request = json.loads(request)
    response, state_table = sync_request(state_table, request)

    print 'reponse : '
    print json.dumps(response, sort_keys=True)
    print 'current state : '
    print json.dumps(state_table, sort_keys=True)
    

    #set push_address to be "www.baidu.com" and start streaming for [教师]-[1001]
    print '\n\n\n-----------------set push_address to be "www.baidu.com" and start streaming for [教师]-[1001]----------------------'
    request = '''
        {
            "ff-ff-ff-ff-ff-ff":
            {
                "push_stream_info":
                {
                    "[教师]-[1001]":
                    {
                        "state": 1,
                        "address": "www.baidu.com"
                    }
                }
            }, 
            "type":0
        }
    '''
    request = json.loads(request)
    response, state_table = sync_request(state_table, request)

    print 'reponse : '
    print json.dumps(response, sort_keys=True)
    print 'current state : '
    print json.dumps(state_table, sort_keys=True)

    #query all info of push_stream
    print '\n\n\n-----------------query all info of push_stream----------------------'
    request = '''
        {
            "ff-ff-ff-ff-ff-ff":
            {
                "push_stream_info":-1
            }, 
            "type":0
        }
    '''
    request = json.loads(request)
    response, state_table = sync_request(state_table, request)

    print 'reponse : '
    print json.dumps(response, sort_keys=True)
    print 'current state : '
    print json.dumps(state_table, sort_keys=True)



    #set all
    print '\n\n\n--------set all------------------'
    response, state_table = sync_request({}, state_table)

    print 'reponse : '
    print json.dumps(response, sort_keys=True)
    print 'current state : '
    print json.dumps(state_table, sort_keys=True)

    #query all
    print '\n\n\n--------query all------------------'
    response, state_table = sync_request(state_table, -1)

    print 'reponse : '
    print json.dumps(response, sort_keys=True)
    print 'current state : '
    print json.dumps(state_table, sort_keys=True)




