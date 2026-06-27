# Foundation Layer: Constants & Configurations
DB_NAME = 'crm_engine.db'

# Status Constants
STATUS_NEW = 'New'
STATUS_CONTACTED = 'Contacted'
STATUS_INTERESTED = 'Interested'
STATUS_PROPOSAL = 'Proposal Sent'
STATUS_WON = 'Won'
STATUS_LOST = 'Lost'

VALID_STATUSES = [
    STATUS_NEW, 
    STATUS_CONTACTED, 
    STATUS_INTERESTED, 
    STATUS_PROPOSAL, 
    STATUS_WON, 
    STATUS_LOST
]

# Role Constants
ROLE_ADMIN = 'Admin'
ROLE_SALES = 'Sales'
ROLE_VIEWER = 'Viewer'

PERMISSIONS = {
    ROLE_ADMIN: ['create', 'update', 'delete', 'view', 'restore'],
    ROLE_SALES: ['create', 'view', 'update'],
    ROLE_VIEWER: ['view']
}
