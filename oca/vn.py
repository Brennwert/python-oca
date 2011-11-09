# -*- coding: UTF-8 -*-
from pool import Pool, PoolElement, Template


class VirtualNetwork(PoolElement):
    METHODS = {
        'info'     : 'vn.info',
        'allocate' : 'vn.allocate',
        'delete'   : 'vn.delete',
        'publish'  : 'vn.publish',
        'chown'    : 'vn.chown',
        'addleases': 'vn.addleases',
        'rmleases' : 'vn.rmleases'
    }

    XML_TYPES = {
            'id'       : int,
            'uid'      : int,
            'gid'      : int,
            'uname'    : str,
            'gname'    : str,
            'name'     : str,
            'type'     : int,
            'bridge'   : str,
            'public'   : bool,
            'total_leases' : int,
            'template' : ['TEMPLATE', Template],
    }

    ELEMENT_NAME = 'VNET'

    @staticmethod
    def allocate(client, template):
        '''
        allocates a new virtual network in OpenNebula

        Arguments

        ``template``
           a string containing the template of the virtual network
        '''
        vn_id = client.call(VirtualNetwork.METHODS['allocate'], template)
        return vn_id

    def __init__(self, xml, client):
        super(VirtualNetwork, self).__init__(xml, client)
        self.id = self['ID'] if self['ID'] else None

    def publish(self):
        '''
        Publishes a virtual network.
        '''
        self.client.call(self.METHODS['publish'], self.id, True)

    def unpublish(self):
        '''
        Unpublishes a virtual network.
        '''
        self.client.call(self.METHODS['publish'], self.id, False)

    def chown(self, uid, gid):
        '''
        Changes the owner/group

        Arguments

        ``uid``
        New owner id. Set to -1 to leave current value
        ``gid``
        New group id. Set to -1 to leave current value
        '''
        self.client.call(self.METHODS['chown'], self.id, uid, gid)

    def __repr__(self):
        return '<oca.VirtualNetwork("%s")>' % self.name


class VirtualNetworkPool(Pool):
    METHODS = {
            'info' : 'vnpool.info',
    }

    def __init__(self, client):
        super(VirtualNetworkPool, self).__init__('VNET_POOL', 'VNET', client)

    def factory(self, xml):
        v = VirtualNetwork(xml, self.client)
        v.convert_types()
        return v

